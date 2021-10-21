# Generated by Django 3.0.7 on 2021-10-21 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20210209_0804'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPosting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('link', models.URLField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('pubdate', models.DateField(null=True)),
            ],
        ),
    ]
