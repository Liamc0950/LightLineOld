# Generated by Django 3.0.5 on 2020-04-15 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lightlineapp', '0002_auto_20200415_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
