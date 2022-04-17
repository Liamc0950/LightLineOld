# Generated by Django 3.2.11 on 2022-03-15 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lightlineapp', '0010_alter_color_colorname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instrument',
            name='color',
        ),
        migrations.AddField(
            model_name='instrument',
            name='color',
            field=models.ManyToManyField(blank=True, to='lightlineapp.Color'),
        ),
    ]