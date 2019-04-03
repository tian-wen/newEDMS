# Generated by Django 2.1 on 2019-03-15 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EDMS_backend', '0004_auto_20190305_2330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expertgroup',
            name='user',
        ),
        migrations.AddField(
            model_name='paperinfo',
            name='category',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paperinfo',
            name='citation',
            field=models.IntegerField(blank=True, db_index=True, max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='paperinfo',
            name='data1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='paperinfo',
            name='data2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='paperinfo',
            name='data3',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='paperinfo',
            name='data4',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='paperinfo',
            name='data5',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='ExpertGroup',
        ),
    ]
