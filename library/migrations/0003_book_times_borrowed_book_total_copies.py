# Generated by Django 5.0.4 on 2024-05-24 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='times_borrowed',
            field=models.PositiveIntegerField(default=0, verbose_name='Times Borrowed'),
        ),
        migrations.AddField(
            model_name='book',
            name='total_copies',
            field=models.PositiveIntegerField(default=0, verbose_name='Total Copies'),
        ),
    ]
