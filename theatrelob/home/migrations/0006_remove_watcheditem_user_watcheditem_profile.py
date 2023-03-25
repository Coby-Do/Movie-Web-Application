# Generated by Django 4.1.6 on 2023-02-17 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_movie_actor_alter_movie_country_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watcheditem',
            name='user',
        ),
        migrations.AddField(
            model_name='watcheditem',
            name='profile',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='home.profile'),
            preserve_default=False,
        ),
    ]
