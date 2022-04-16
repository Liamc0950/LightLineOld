# Generated by Django 3.2.11 on 2022-03-14 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lightlineapp', '0008_alter_instrumenttype_load'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrumenttype',
            name='beamAngle',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='instrumenttype',
            name='fieldAngle',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='instrumenttype',
            name='weight',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='instrumenttype',
            name='zoomAble',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='instrumenttype',
            name='zoomAngleMax',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='instrumenttype',
            name='zoomAngleMin',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
