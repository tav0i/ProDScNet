# Generated by Django 4.2.6 on 2023-10-11 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_rename_datecompleted_task_date_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_completed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
