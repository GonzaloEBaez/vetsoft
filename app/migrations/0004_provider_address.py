# Generated by Django 5.0.4 on 2024-05-23 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='address',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
