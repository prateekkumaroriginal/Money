# Generated by Django 5.0 on 2023-12-07 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='quantity',
            new_name='amount',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='price',
        ),
    ]
