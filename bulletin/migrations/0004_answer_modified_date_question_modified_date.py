# Generated by Django 4.1.7 on 2023-03-19 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0003_answer_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='modified_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='modified_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
