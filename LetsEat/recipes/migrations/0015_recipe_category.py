# Generated by Django 5.0 on 2023-12-12 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_remove_recipe_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='category',
            field=models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('salad', 'Salad'), ('smoothie', 'Smoothie'), ('sweet', 'Sweet')], default='sweet', max_length=64),
        ),
    ]
