# Generated by Django 2.2.3 on 2019-08-17 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_main', '0004_auto_20190817_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Technology', 'Technology'), ('Food', 'Food'), ('Health', 'Health'), ('Meetups', 'Meetups'), ('Cooking', 'Cooking')], max_length=20),
        ),
    ]
