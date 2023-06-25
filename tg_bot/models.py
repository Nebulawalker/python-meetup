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


class ChatState(models.Model):

    chat_id = models.IntegerField(
        'идентификатор чата',
        primary_key=True,
    )
    state = models.CharField(
        'состояние',
        max_length=100,
    )

    created_at = models.DateTimeField(
        verbose_name='создан в',
        auto_now_add=True,
        db_index=True,
    )

    modified_at = models.DateTimeField(
        verbose_name='изменен в',
        auto_now=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'состояние чата'
        verbose_name_plural = 'состояния чатов'

    def __str__(self):
        return f'Состояние чата {self.chat_id}: {self.state}'


class Survey(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name='пользователь',
        on_delete=models.PROTECT,
        related_name='survey',
        unique=True,
    )

    birth_date = models.DateField(
        verbose_name='дата рождения',
    )

    specialization = models.CharField(
        verbose_name='специализация',
        max_length=100,
    )

    stack = models.CharField(
        verbose_name='стек',
        max_length=100,
    )

    hobby = models.CharField(
        verbose_name='хобби',
        max_length=100,
    )

    acquaintance_goal = models.CharField(
        verbose_name='цель знакомства',
        max_length=100,
    )

    region = models.CharField(
        verbose_name='регион',
        max_length=100,
    )

    created_at = models.DateTimeField(
        verbose_name='создана в',
        auto_now_add=True,
        db_index=True,
    )

    modified_at = models.DateTimeField(
        verbose_name='изменена в',
        auto_now=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'анкета'
        verbose_name_plural = 'анкеты'

    def __str__(self):
        return f'Анкета {self.user}: {self.specialization}'


class Donation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='пользователь',
        on_delete=models.PROTECT,
        related_name='donations',
    )

    amount = models.DecimalField(
        verbose_name='сумма',
        max_digits=19,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        verbose_name='создана в',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'донат'
        verbose_name_plural = 'донаты'

    def __str__(self):
        return f'Донат {self.id} на сумму {self.amount}'
