# Generated by Django 4.2.6 on 2023-10-24 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0003_alter_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
    ]
