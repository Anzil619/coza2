# Generated by Django 4.2 on 2023-05-24 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.IntegerField(),
        ),
    ]
