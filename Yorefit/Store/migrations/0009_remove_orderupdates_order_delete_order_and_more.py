# Generated by Django 4.1.1 on 2022-10-10 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0008_orderupdates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderupdates',
            name='order',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderUpdates',
        ),
    ]
