# Generated by Django 4.2.6 on 2023-10-12 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0002_alter_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(null=True, upload_to='ProDScNet/images/', verbose_name='Image'),
        ),
    ]