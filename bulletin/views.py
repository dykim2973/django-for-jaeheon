from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.http import HttpRequest
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.


def index(request: HttpRequest):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 질문의 내용 검색
            Q(author__username__icontains=kw) |  # 질문의 작성자 검색
            Q(answer__author__username__icontains=kw)  # 질문의 작성자의 이름 검색
        ).distinct()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {
        'question_list': page_obj,
        'page': page,
        'kw': kw
    }
    return render(request, 'bulletin/question_list.html', context)


def detail(request: HttpRequest, question_id: int):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'bulletin/question_detail.html', context)


@login_required(login_url='common:login')
def answer_create(request: HttpRequest, question_id: int):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('bulletin:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'bulletin/question_detail.html', context)


@login_required(login_url='common:login')
def question_create(request: HttpRequest):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('bulletin:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'bulletin/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request: HttpRequest, question_id: int):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('bulletin:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modified_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('bulletin:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'bulletin/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('bulletin:detail', question_id=question.id)
    question.delete()
    return redirect('bulletin:index')


@login_required(login_url='common:login')
def answer_modify(request: HttpRequest, answer_id: int):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('bulletin:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modified_date = timezone.now()  # 수정일시 저장
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('bulletin:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'form': form}
    return render(request, 'bulletin/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('bulletin:detail', question_id=answer.question.id)


@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('bulletin:detail', question_id=question.id)


@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(resolve_url('bulletin:detail', question_id=answer.question.id), answer.id))


