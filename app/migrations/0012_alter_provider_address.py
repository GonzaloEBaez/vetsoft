# Generated by Django 5.0.4 on 2024-06-01 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_merge_0009_provider_address_0010_alter_pet_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='address',
            field=models.CharField(max_length=100),
        ),
    ]