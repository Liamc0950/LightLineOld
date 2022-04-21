# Generated by Django 4.0.3 on 2022-04-17 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lightlineapp', '0013_alter_gobo_goboname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='colorFlag',
        ),
        migrations.RemoveField(
            model_name='action',
            name='cue',
        ),
        migrations.RemoveField(
            model_name='action',
            name='focus',
        ),
        migrations.RemoveField(
            model_name='action',
            name='operator',
        ),
        migrations.RemoveField(
            model_name='action',
            name='shotType',
        ),
        migrations.DeleteModel(
            name='CableType',
        ),
        migrations.RemoveField(
            model_name='circuit',
            name='breakout',
        ),
        migrations.RemoveField(
            model_name='colorflag',
            name='color1',
        ),
        migrations.RemoveField(
            model_name='colorflag',
            name='project',
        ),
        migrations.RemoveField(
            model_name='cue',
            name='cueList',
        ),
        migrations.RemoveField(
            model_name='cuelist',
            name='project',
        ),
        migrations.RemoveField(
            model_name='focus',
            name='project',
        ),
        migrations.RemoveField(
            model_name='followspot',
            name='project',
        ),
        migrations.RemoveField(
            model_name='header',
            name='cue',
        ),
        migrations.RemoveField(
            model_name='header',
            name='cueList',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='accessory',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='breakout',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='cable',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='circuit',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='color',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='focusChart',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='focusNote',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='gobo',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='instrumentType',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='position',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='project',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='workNote',
        ),
        migrations.RemoveField(
            model_name='instrumenttype',
            name='project',
        ),
        migrations.RemoveField(
            model_name='operator',
            name='followspotType',
        ),
        migrations.RemoveField(
            model_name='operator',
            name='project',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='project',
            name='lightingDesigner',
        ),
        migrations.RemoveField(
            model_name='shot',
            name='project',
        ),
        migrations.DeleteModel(
            name='Accessory',
        ),
        migrations.DeleteModel(
            name='Action',
        ),
        migrations.DeleteModel(
            name='Breakout',
        ),
        migrations.DeleteModel(
            name='Cable',
        ),
        migrations.DeleteModel(
            name='Circuit',
        ),
        migrations.DeleteModel(
            name='Color',
        ),
        migrations.DeleteModel(
            name='ColorFlag',
        ),
        migrations.DeleteModel(
            name='Cue',
        ),
        migrations.DeleteModel(
            name='CueList',
        ),
        migrations.DeleteModel(
            name='Focus',
        ),
        migrations.DeleteModel(
            name='FocusChart',
        ),
        migrations.DeleteModel(
            name='FocusNote',
        ),
        migrations.DeleteModel(
            name='Followspot',
        ),
        migrations.DeleteModel(
            name='Gobo',
        ),
        migrations.DeleteModel(
            name='Header',
        ),
        migrations.DeleteModel(
            name='Instrument',
        ),
        migrations.DeleteModel(
            name='InstrumentType',
        ),
        migrations.DeleteModel(
            name='Operator',
        ),
        migrations.DeleteModel(
            name='Position',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='Shot',
        ),
        migrations.DeleteModel(
            name='WorkNote',
        ),
    ]
