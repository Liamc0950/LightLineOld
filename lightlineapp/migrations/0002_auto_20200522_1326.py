# Generated by Django 3.0.5 on 2020-05-22 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lightlineapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharenode',
            name='profile',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='lightlineapp.Profile'),
        ),
    ]