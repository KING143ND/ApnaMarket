# Generated by Django 3.2 on 2023-05-15 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.IntegerField(max_length=13, null=True),
        ),
    ]
