# Generated by Django 4.2.6 on 2024-09-09 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calcetto', '0003_developer_total_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='total_match',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='developer',
            name='win_match',
            field=models.IntegerField(default=0),
        ),
    ]