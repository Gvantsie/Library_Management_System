# Generated by Django 5.0.4 on 2024-05-26 20:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_reservation_due_date_reservation_return_date_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booktransaction',
            options={'verbose_name': 'Book Transaction', 'verbose_name_plural': 'Book Transactions'},
        ),
        migrations.AlterField(
            model_name='booktransaction',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='library.book'),
        ),
        migrations.AlterField(
            model_name='booktransaction',
            name='borrowed_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Borrowed At'),
        ),
        migrations.AlterField(
            model_name='booktransaction',
            name='returned_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Returned At'),
        ),
        migrations.AlterField(
            model_name='booktransaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('books_read', models.IntegerField(default=0, verbose_name='Books Read')),
                ('books_reserved', models.IntegerField(default=0, verbose_name='Books Reserved')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User Statistics',
                'verbose_name_plural': 'User Statistics',
            },
        ),
    ]