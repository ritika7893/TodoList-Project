# Generated by Django 5.0.2 on 2024-11-18 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0008_delete_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='todo_name',
            field=models.TextField(max_length=255),
        ),
    ]
