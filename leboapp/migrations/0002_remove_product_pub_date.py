# Generated by Django 4.1.7 on 2023-03-30 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leboapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='pub_date',
        ),
    ]
