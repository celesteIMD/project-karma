# Generated by Django 5.1.3 on 2025-02-27 18:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('myRoom', '0008_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='building',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='room',
        ),
        migrations.AddField(
            model_name='review',
            name='tags',
            field=models.ManyToManyField(blank=True, to='myRoom.tag'),
        ),
        migrations.CreateModel(
            name='TaggedItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myRoom.tag')),
            ],
        ),
    ]
