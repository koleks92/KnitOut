# Generated by Django 4.1.7 on 2023-05-15 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knitout', '0007_recipe_dislikes_recipe_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='favorite',
            new_name='favorites',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='difficulty',
            field=models.CharField(choices=[('', 'Choose level'), ('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('experienced', 'Experienced'), ('expert', 'Expert/Grandma')], max_length=64),
        ),
    ]
