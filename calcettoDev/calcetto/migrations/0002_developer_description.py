# Generated by Django 4.2.6 on 2024-09-09 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calcetto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='description',
            field=models.CharField(default='', max_length=255),
        ),
    ]
