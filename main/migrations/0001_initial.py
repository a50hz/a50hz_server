# Generated by Django 3.1.6 on 2021-02-06 10:01

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Extent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=428)),
                ('lat1', models.DecimalField(decimal_places=17, max_digits=19, null=True)),
                ('lat2', models.DecimalField(decimal_places=17, max_digits=19, null=True)),
                ('lng1', models.DecimalField(decimal_places=18, max_digits=20, null=True)),
                ('lng2', models.DecimalField(decimal_places=18, max_digits=20, null=True)),
                ('zoom', models.DecimalField(decimal_places=5, max_digits=7, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DecimalField(decimal_places=2, max_digits=7)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=8)),
                ('date_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 2, 6, 10, 1, 50, 769464, tzinfo=utc))),
                ('type', models.CharField(max_length=50)),
                ('interpolation_type', models.CharField(max_length=50)),
                ('Extent', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.extent')),
            ],
        ),
    ]
