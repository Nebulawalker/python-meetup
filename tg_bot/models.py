from django.conf import settings
from django.db import models
from django.utils.timezone import now, localtime


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

    def __str__(self):
        return (
            f'{self.topic} '
            f'({localtime(self.starts_at).strftime("%d.%m.%Y %H:%M")})'
        )


class Issue(models.Model):
    NEW = 'NEW'
    UNDER_CONSIDERATION = 'CON'
    CLOSED = 'CLO'
    STATUS_CHOICES = [
        (NEW, 'Новый'),
        (UNDER_CONSIDERATION, 'На рассмотрении'),
        (CLOSED, 'Закрыт'),
    ]

    from_whom = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='от кого',
        on_delete=models.PROTECT,
        related_name='issues_from',
    )

    report = models.ForeignKey(
        'Report',
        verbose_name='доклад',
        on_delete=models.PROTECT,
        related_name='issues',
    )

    question = models.TextField(
        verbose_name='текст вопроса'
    )

    answer = models.TextField(
        verbose_name='ответ',
        blank=True,
        null=True,
    )

    asked_at = models.DateTimeField(
        verbose_name='задан',
        default=now
    )

    status = models.CharField(
        verbose_name='Статус',
        max_length=3,
        choices=STATUS_CHOICES,
        default=NEW,
        db_index=True,
    )

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return self.question
