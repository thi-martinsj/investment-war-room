# Generated by Django 4.0.6 on 2022-07-18 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assets',
            name='ticker',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
