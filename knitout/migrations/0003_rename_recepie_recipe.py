# Generated by Django 4.1.7 on 2023-05-08 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knitout', '0002_recepie'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Recepie',
            new_name='Recipe',
        ),
    ]