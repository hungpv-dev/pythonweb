# Generated by Django 5.1.3 on 2024-11-19 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField(null=True)),
                ('link', models.CharField(max_length=155)),
                ('cookie', models.JSONField(null=True)),
            ],
        ),
    ]
