# Generated by Django 4.1.4 on 2022-12-15 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_quizcontent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizcontent',
            name='percentage_correct',
            field=models.IntegerField(blank=True),
        ),
    ]
