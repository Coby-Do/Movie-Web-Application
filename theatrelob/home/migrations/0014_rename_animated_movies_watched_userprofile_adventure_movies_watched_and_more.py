# Generated by Django 4.1.6 on 2023-04-17 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_watcheditem_genres'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='animated_movies_watched',
            new_name='adventure_movies_watched',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='documentaries_watched',
            new_name='animation_movies_watched',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='crime_movies_watched',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='documentary_movies_watched',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='drama_movies_watched',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='family_movies_watched',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='fantasy_movies_watched',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='history_movies_watched',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='horror_movies_watched',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='music_movies_watched',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mystery_movies_watched',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='science_fiction_movies_watched',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='thriller_movies_watched',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='tv_movie_movies_watched',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='war_movies_watched',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='western_movies_watched',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
