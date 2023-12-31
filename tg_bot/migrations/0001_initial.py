# Generated by Django 4.2.2 on 2023-06-21 11:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100, verbose_name='тема')),
                ('starts_at', models.DateTimeField(db_index=True, verbose_name='начало')),
                ('ends_at', models.DateTimeField(verbose_name='окончание')),
                ('is_current', models.BooleanField(verbose_name='текущий')),
                ('speaker', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reports', to=settings.AUTH_USER_MODEL, verbose_name='докладчик')),
            ],
            options={
                'verbose_name': 'доклад',
                'verbose_name_plural': 'доклады',
            },
        ),
    ]
