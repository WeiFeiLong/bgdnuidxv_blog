# Generated by Django 2.2.11 on 2020-04-16 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0010_auto_20200416_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='status',
        ),
    ]
