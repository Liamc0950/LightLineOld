# Generated by Django 3.2.11 on 2022-03-14 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lightlineapp', '0009_auto_20220314_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='colorName',
            field=models.CharField(max_length=32),
        ),
    ]