# Generated by Django 3.0.7 on 2021-02-09 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_contact_emaillist'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.DeleteModel(
            name='EmailList',
        ),
    ]