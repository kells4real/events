# Generated by Django 2.2.5 on 2019-09-20 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20190920_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]
