# Generated by Django 5.1.5 on 2025-03-20 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myRoom', '0023_merge_20250319_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null='true', upload_to='profile_pics'),
        ),
    ]
