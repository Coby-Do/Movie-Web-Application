# Generated by Django 4.1.6 on 2023-02-14 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_movie_movie_poster_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='tmdb_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]