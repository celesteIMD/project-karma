# Generated by Django 5.1.7 on 2025-03-20 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myRoom', '0025_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='../images/pfp.png', null='true', upload_to='profile_pics'),
        ),
    ]
