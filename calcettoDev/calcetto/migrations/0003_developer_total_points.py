# Generated by Django 4.2.6 on 2024-09-09 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calcetto', '0002_developer_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='total_points',
            field=models.IntegerField(default=0),
        ),
    ]
