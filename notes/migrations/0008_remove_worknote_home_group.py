# Generated by Django 4.0.4 on 2022-04-22 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0007_alter_worknote_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worknote',
            name='home_group',
        ),
    ]