# Generated by Django 5.1.6 on 2025-03-10 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_commet_ratinganswer_comment_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='commet',
            new_name='comment',
        ),
    ]
