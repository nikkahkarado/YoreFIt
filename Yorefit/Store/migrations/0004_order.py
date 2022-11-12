# Generated by Django 4.1.1 on 2022-10-08 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_rename_productimages_productimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=50)),
                ('l_name', models.CharField(max_length=50)),
                ('address', models.TextField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('zip', models.IntegerField()),
                ('contact', models.IntegerField()),
                ('email', models.CharField(max_length=100)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('delivery', models.CharField(max_length=10)),
                ('payment', models.CharField(max_length=10)),
            ],
        ),
    ]
