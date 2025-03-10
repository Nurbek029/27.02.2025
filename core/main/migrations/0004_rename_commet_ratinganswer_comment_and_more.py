# Generated by Django 5.1.6 on 2025-03-10 15:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_product_main_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ratinganswer',
            old_name='commet',
            new_name='comment',
        ),
        migrations.AlterField(
            model_name='ratinganswer',
            name='rating',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_answers', to='main.rating', verbose_name='Отзыв'),
        ),
    ]
