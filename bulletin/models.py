from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Question(models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    voter = models.ManyToManyField(User, related_name='voter_question')
    modified_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    voter = models.ManyToManyField(User, related_name='voter_answer')
    modified_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField()
