# Generated by Django 5.0.4 on 2024-05-25 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_merge_20240524_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='birthday',
            field=models.DateField(),
        ),
    ]