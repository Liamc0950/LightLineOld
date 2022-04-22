# Generated by Django 4.0.4 on 2022-04-22 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projectManager', '0001_initial'),
        ('database', '0001_initial'),
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkNote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lastUpdate', models.DateTimeField(auto_now=True)),
                ('noteText', models.CharField(max_length=256)),
                ('home_group', models.CharField(max_length=5)),
                ('channelList', models.CharField(max_length=5)),
                ('changeFieldSelection', models.CharField(choices=[('Instrument Type', 'INSTRUMENT_TYPE'), ('Position', 'POSITION'), ('Unit Number', 'UNIT_NUMBER'), ('Accessory', 'ACCESSORY'), ('Color', 'COLOR'), ('Gobo', 'GOBO'), ('Gobo Size', 'GOBO_SIZE'), ('Purpose', 'PURPOSE'), ('Dimmer', 'DIMMER'), ('Circuit', 'CIRCUIT'), ('Breakout', 'BREAKOUT'), ('Dimmer Phase', 'DIMMER_PHASE'), ('Address', 'ADDRESS'), ('Universe', 'UNIVERSE'), ('Channel', 'CHANNEL')], default='INSTRUMENT_TYPE', max_length=16)),
                ('newUnitNumber', models.IntegerField()),
                ('newGoboSize', models.CharField(blank=True, max_length=8, null=True)),
                ('newPurpose', models.CharField(max_length=128)),
                ('newDimmer', models.IntegerField(blank=True, null=True)),
                ('newDimmerPhase', models.CharField(blank=True, max_length=8, null=True)),
                ('newAddress', models.IntegerField(blank=True, null=True)),
                ('newUniverse', models.IntegerField(blank=True, null=True)),
                ('newChannel', models.IntegerField(blank=True, null=True)),
                ('assignedTo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignedTo', to='landing.profile')),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='createdBy', to='landing.profile')),
                ('lastUpdatedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lastUpdatedBy', to='landing.profile')),
                ('newAccessory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.accessory')),
                ('newBreakout', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.breakout')),
                ('newCircuit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.circuit')),
                ('newColor', models.ManyToManyField(blank=True, related_name='newColors', to='database.color')),
                ('newGobo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.gobo')),
                ('newInstrumentType', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.instrumenttype')),
                ('newPosition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.position')),
                ('project', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='projectManager.project')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]