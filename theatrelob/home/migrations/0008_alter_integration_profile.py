# Generated by Django 4.1.6 on 2023-03-25 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_integration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='integration',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.profile'),
        ),
    ]
