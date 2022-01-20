# Generated by Django 4.0.1 on 2022-01-20 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_trip_country_remove_trip_full_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='duration',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='trip',
            name='resort',
            field=models.ForeignKey(help_text='Курорт', on_delete=django.db.models.deletion.CASCADE, to='main.resort'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='start_date',
            field=models.DateField(),
        ),
    ]