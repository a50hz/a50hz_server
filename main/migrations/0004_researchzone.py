# Generated by Django 3.1.6 on 2021-03-05 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210227_1854'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResearchZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=428)),
                ('lat1', models.DecimalField(decimal_places=17, max_digits=19, null=True)),
                ('lng1', models.DecimalField(decimal_places=18, max_digits=20, null=True)),
                ('lat2', models.DecimalField(decimal_places=17, max_digits=19, null=True)),
                ('lng2', models.DecimalField(decimal_places=18, max_digits=20, null=True)),
            ],
        ),
    ]
