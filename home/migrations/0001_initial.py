# Generated by Django 5.1.3 on 2024-11-19 01:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=155)),
                ('type', models.CharField(default='Chủ đề', max_length=55, null=True)),
                ('type_page', models.IntegerField(default=1)),
                ('user_id', models.IntegerField(null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=255, null=True, unique=True)),
                ('page_id', models.IntegerField()),
                ('content', models.TextField(null=True)),
                ('media', models.JSONField(null=True)),
                ('like', models.CharField(default='0', max_length=50)),
                ('comment', models.CharField(default='0', max_length=50)),
                ('share', models.CharField(default='0', max_length=50)),
                ('up', models.BooleanField(default=False)),
                ('user_id', models.IntegerField(default=0)),
                ('page_up_id', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='home.post')),
            ],
        ),
    ]
