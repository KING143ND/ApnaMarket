# Generated by Django 3.2 on 2023-05-25 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0012_auto_20230525_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(default='Unknown', max_length=255),
        ),
    ]
