# Generated by Django 5.1.3 on 2025-02-28 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myRoom', '0011_review_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='room',
            name='rating',
        ),
    ]
