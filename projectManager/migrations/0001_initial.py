# Generated by Django 4.0.3 on 2022-04-17 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lastUpdate', models.DateTimeField(auto_now=True)),
                ('showName', models.CharField(max_length=64)),
                ('showNameShort', models.CharField(default='', max_length=32)),
                ('active', models.BooleanField(default=False)),
                ('lightingDesigner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='landing.profile')),
            ],
        ),
    ]