# Generated by Django 4.0.4 on 2022-04-22 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_images'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='lastUpdate',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
