# Generated by Django 4.1.6 on 2023-04-24 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_badge_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]