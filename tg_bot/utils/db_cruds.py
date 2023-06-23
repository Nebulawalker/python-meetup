from loguru import logger
from users.models import User
from tg_bot.models import Survey, Report
from django.db.utils import IntegrityError

from asgiref.sync import sync_to_async


@sync_to_async
def create_user(**data):
    try:
        User.objects.create_user(username=data['username'], tg_id=data['tg_id'], first_name=data['first_name'],
                                 last_name=data['last_name'])
    except IntegrityError:
        pass
    user = User.objects.get(username=data['username'])
    user.tg_id = data['tg_id']
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.save()


@sync_to_async
def create_survey(username, **data):
    try:
        user = User.objects.get(username=username)
        Survey.objects.create(user=user, birth_date=data['birth_date'], specialization=data['specialization'],
                              stack=data['stack'], hobby=data['hobby'], acquaintance_goal=data['acquaintance_goal'],
                              region=data['region'])
    except KeyError:
        pass


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
    serialized_reports = []
    for report in reports:
        serialized_report = dict(id=report.id, topic=report.topic, speaker=report.speaker, starts_at=report.starts_at,
                                 ends_at=report.ends_at, is_current=report.is_current)
        serialized_reports.append(serialized_report)
    return serialized_reports


@sync_to_async
def get_report(report_id):
    report = Report.objects.get(id=report_id)
    serialized_report = dict(id=report.id, topic=report.topic, speaker=report.speaker, starts_at=report.starts_at,
                             ends_at=report.ends_at, is_current=report.is_current)
    return serialized_report


@sync_to_async
def get_survey(**data):
    def serialize(survey):
        user = User.objects.get(survey=survey)
        serialized_survey = dict(id=survey.id, user=''.join(('@', survey.user.username)), stack=survey.stack, birth_date=survey.birth_date,
                                 specialization=survey.specialization, hobby=survey.hobby, region=survey.region,
                                 acquaintance_goal=survey.acquaintance_goal, first_name=user.first_name,
                                 last_name=user.last_name)
        return serialized_survey

    if data.get('survey_id'):
        survey = Survey.objects.get(id=data['survey_id'])
        return serialize(survey)
    elif data.get('username'):
        try:
            survey = User.objects.get(username=data['username']).survey
            return serialize(survey)
        except User.survey.RelatedObjectDoesNotExist:
            return False
        except User.DoesNotExist:
            return False
    return False


@sync_to_async
def get_surveys():
    surveys = Survey.objects.all().order_by('created_at')
    serialized_surveys = []
    if surveys:
        for survey in surveys:
            serialized_survey = dict(id=survey.id, user=survey.user, stack=survey.stack, birth_date=survey.birth_date,
                                     specialization=survey.specialization, hobby=survey.hobby, region=survey.region,
                                     acquaintance_goal=survey.acquaintance_goal)
            serialized_surveys.append(serialized_survey)
        return serialized_surveys
    else:
        return False
