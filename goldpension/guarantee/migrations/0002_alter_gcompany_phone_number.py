# Generated by Django 4.0.5 on 2023-08-17 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guarantee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gcompany',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]