# Generated by Django 4.1.6 on 2023-02-13 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_watcheditem_delete_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_poster_url',
            field=models.URLField(default='None'),
            preserve_default=False,
        ),
    ]