# Generated by Django 2.2.5 on 2019-09-25 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20190920_2247'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name_plural': 'Events'},
        ),
        migrations.AlterModelOptions(
            name='tickettype',
            options={'verbose_name': 'Ticket', 'verbose_name_plural': 'Tickets'},
        ),
        migrations.DeleteModel(
            name='Date',
        ),
    ]
