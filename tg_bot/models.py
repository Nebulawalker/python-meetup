from django.conf import settings
from django.db import models


class Report(models.Model):
    speaker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='докладчик',
        on_delete=models.PROTECT,
        related_name='reports',
    )
    topic = models.CharField(
        verbose_name='тема',
        max_length=100
    )

    starts_at = models.DateTimeField(
        verbose_name='начало',
        db_index=True,
    )

    ends_at = models.DateTimeField(
        verbose_name='окончание',
    )

    is_current = models.BooleanField(
        verbose_name='текущий',
    )

    class Meta:
        verbose_name = 'доклад'
        verbose_name_plural = 'доклады'
