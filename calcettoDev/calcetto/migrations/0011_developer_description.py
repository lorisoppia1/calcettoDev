# Generated by Django 4.2.6 on 2025-01-01 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calcetto', '0010_developer_total_match_singolo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
