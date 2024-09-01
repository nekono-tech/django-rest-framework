# Generated by Django 5.1 on 2024-09-01 08:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('youtube', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('video_id', models.CharField(max_length=20, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('published_at', models.DateTimeField()),
                ('thumbnail_default_url', models.URLField(blank=True, max_length=255, null=True)),
                ('thumbnail_medium_url', models.URLField(blank=True, max_length=255, null=True)),
                ('thumbnail_standard_url', models.URLField(blank=True, max_length=255, null=True)),
                ('thumbnail_high_url', models.URLField(blank=True, max_length=255, null=True)),
                ('thumbnail_maxres_url', models.URLField(blank=True, max_length=255, null=True)),
                ('youtube', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='youtube.youtube')),
            ],
            options={
                'db_table': 'videos',
            },
        ),
    ]
