# Generated by Django 2.2.5 on 2019-09-19 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20190918_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='date',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]