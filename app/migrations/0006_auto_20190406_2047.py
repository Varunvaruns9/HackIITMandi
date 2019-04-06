# Generated by Django 2.2 on 2019-04-06 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20190406_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bloodgroup',
            field=models.IntegerField(blank=True, choices=[(1, 'O'), (2, 'A'), (3, 'B'), (4, 'AB')], default=1, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='rh',
            field=models.IntegerField(blank=True, choices=[(1, '+'), (2, '-')], default=1, null=True),
        ),
    ]