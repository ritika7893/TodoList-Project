# Generated by Django 5.0.2 on 2024-11-14 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0004_customer_is_active_customer_is_staff_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='todo_name',
            field=models.TextField(max_length=1000),
        ),
    ]
