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
            name='Accessory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('accessoryName', models.CharField(max_length=32, unique=True)),
                ('weight', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Breakout',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('circuitLabel', models.CharField(max_length=32, unique=True)),
                ('service', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Cable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cableLabel', models.CharField(max_length=32, unique=True)),
                ('cableType', models.CharField(max_length=16, unique=True)),
                ('cableLength', models.IntegerField()),
                ('weight', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CableType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cableTypeName', models.CharField(max_length=32, unique=True)),
                ('weightPerFoot', models.IntegerField()),
                ('ampRating', models.IntegerField()),
                ('power', models.BooleanField(default=False)),
                ('data', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Circuit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('circuitLabel', models.CharField(max_length=32, unique=True)),
                ('service', models.IntegerField()),
                ('breakout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.breakout')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lastUpdate', models.DateTimeField(auto_now=True)),
                ('colorName', models.CharField(max_length=32)),
                ('colorCode', models.CharField(max_length=16, unique=True)),
                ('colorHex', models.CharField(default='0xFFFFFFFF', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='FocusChart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('chartLabel', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='FocusNote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('noteLabel', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Gobo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lastUpdate', models.DateTimeField(auto_now=True)),
                ('goboName', models.CharField(max_length=32)),
                ('goboCode', models.CharField(max_length=16, unique=True)),
                ('imageUrl', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('positionName', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkNote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('noteLabel', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='InstrumentType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('typeName', models.CharField(max_length=64)),
                ('load', models.IntegerField(blank=True, null=True)),
                ('beamAngle', models.IntegerField(blank=True, null=True)),
                ('fieldAngle', models.IntegerField(blank=True, null=True)),
                ('zoomAngleMin', models.IntegerField(blank=True, null=True)),
                ('zoomAngleMax', models.IntegerField(blank=True, null=True)),
                ('zoomAble', models.BooleanField(blank=True, default=False, null=True)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectManager.project')),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('unitNumber', models.IntegerField()),
                ('goboSize', models.CharField(blank=True, max_length=8, null=True)),
                ('purpose', models.CharField(max_length=128)),
                ('dimmer', models.IntegerField(blank=True, null=True)),
                ('dimmerPhase', models.CharField(blank=True, max_length=8, null=True)),
                ('address', models.IntegerField(blank=True, null=True)),
                ('universe', models.IntegerField(blank=True, null=True)),
                ('channel', models.IntegerField(blank=True, null=True)),
                ('accessory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.accessory')),
                ('breakout', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.breakout')),
                ('cable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.cable')),
                ('circuit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.circuit')),
                ('color', models.ManyToManyField(blank=True, related_name='colors', to='database.color')),
                ('focusChart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.focuschart')),
                ('focusNote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.focusnote')),
                ('gobo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.gobo')),
                ('instrumentType', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.instrumenttype')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.position')),
                ('project', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='projectManager.project')),
                ('workNote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.worknote')),
            ],
        ),
    ]
