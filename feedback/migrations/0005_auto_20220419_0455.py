# Generated by Django 3.0 on 2022-04-19 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_answer_option_question_submission_survey'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='text',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='option',
            name='isText',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='prompt',
            field=models.CharField(max_length=250),
        ),
    ]
