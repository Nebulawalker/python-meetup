# Generated by Django 4.2.2 on 2023-06-25 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0005_donation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ChatState',
        ),
    ]