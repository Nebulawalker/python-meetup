# Generated by Django 4.2.2 on 2023-06-21 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tg_bot', '0003_chatstate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(verbose_name='дата рождения')),
                ('specialization', models.CharField(max_length=100, verbose_name='специализация')),
                ('stack', models.CharField(max_length=100, verbose_name='стек')),
                ('hobby', models.CharField(max_length=100, verbose_name='хобби')),
                ('acquaintance_goal', models.CharField(max_length=100, verbose_name='цель знакомства')),
                ('region', models.CharField(max_length=100, verbose_name='регион')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='создана в')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='изменена в')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='survey', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'анкета',
                'verbose_name_plural': 'анкеты',
            },
        ),
    ]
