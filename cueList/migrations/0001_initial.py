# Generated by Django 4.0.3 on 2022-04-17 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projectManager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lastUpdate', models.DateTimeField(auto_now=True)),
                ('cueLabel', models.CharField(blank=True, default='', max_length=100)),
                ('pageNumber', models.IntegerField(default=1)),
                ('eosCueNumber', models.IntegerField(default=1)),
                ('cueTime', models.IntegerField(default=5)),
                ('cueDescription', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CueList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('listName', models.CharField(max_length=64)),
                ('cueListNumber', models.IntegerField(default=1)),
                ('active', models.BooleanField(default=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectManager.project')),
            ],
        ),
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lastUpdate', models.DateTimeField(auto_now=True)),
                ('headerTitle', models.CharField(blank=True, default='', max_length=100)),
                ('cue', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cueList.cue')),
                ('cueList', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cueList.cuelist')),
            ],
        ),
        migrations.AddField(
            model_name='cue',
            name='cueList',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cueList.cuelist'),
        ),
    ]
