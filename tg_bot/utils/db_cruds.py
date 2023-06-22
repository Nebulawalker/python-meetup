from loguru import logger
from users.models import User
from tg_bot.models import Survey, Report
from django.db.utils import IntegrityError


from asgiref.sync import sync_to_async


@sync_to_async
def create_user(username, tg_id):
    try:
        User.objects.create_user(username=username)
    except IntegrityError:
        pass
    user = User.objects.get(username=username)
    user.tg_id = tg_id
    user.save()


@sync_to_async
def create_survey(username, **data):
    user = User.objects.get(username=username)
    Survey.objects.create(user=user, birth_date=data['birth_date'], specialization=data['specialization'],
                          stack=data['stack'], hobby=data['hobby'], acquaintance_goal=data['acquaintance_goal'],
                          region=data['region'])

@sync_to_async
def is_user_reporter(tg_id):
    try:
        if User.objects.get(tg_id=tg_id).reports.last():
            return True
        else:
            return False
    except User.DoesNotExist:
        return False

@sync_to_async
def get_reports():
    reports = Report.objects.all().order_by('ends_at')
    if reports:
        serialized_reports = []
        for report in reports:
            serialized_report = dict(id=report.id, topic=report.topic, speaker=report.speaker, starts_at=report.starts_at,
                                     ends_at=report.ends_at)
            serialized_reports.append(serialized_report)
        return serialized_reports
    else:
        return False

@sync_to_async
def get_report(report_id):
    report = Report.objects.get(id=report_id)
    if report:
        serialized_report = dict(id=report.id, topic=report.topic, speaker=report.speaker, starts_at=report.starts_at,
                                 ends_at=report.ends_at, is_current=report.is_current)
        return serialized_report
    else:
        return 'доклад отсутствует'
