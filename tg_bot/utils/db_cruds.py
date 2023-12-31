from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from tg_bot.models import Issue, Report, Survey, Donation, Watcher, Count
from users.models import User


@sync_to_async
def create_user(**data):
    try:
        User.objects.create_user(
            username=data['username'],
            tg_id=data['tg_id'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
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
        Survey.objects.create(
            user=user,
            birth_date=data['birth_date'],
            specialization=data['specialization'],
            stack=data['stack'],
            hobby=data['hobby'],
            acquaintance_goal=data['acquaintance_goal'],
            region=data['region']
        )
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
        serialized_report = dict(
            id=report.id,
            topic=report.topic,
            speaker=report.speaker,
            starts_at=report.starts_at,
            ends_at=report.ends_at,
            is_current=report.is_current
        )
        serialized_reports.append(serialized_report)
    return serialized_reports


@sync_to_async
def get_report(report_id):
    report = Report.objects.get(id=report_id)
    serialized_report = dict(
        id=report.id,
        topic=report.topic,
        speaker=report.speaker,
        starts_at=report.starts_at,
        ends_at=report.ends_at,
        is_current=report.is_current
    )
    return serialized_report


@sync_to_async
def get_survey(**data):
    def serialize(survey):
        user = User.objects.get(survey=survey)
        serialized_survey = dict(
            id=survey.id,
            user=''.join(('@', survey.user.username)),
            stack=survey.stack,
            birth_date=survey.birth_date,
            specialization=survey.specialization,
            hobby=survey.hobby,
            region=survey.region,
            acquaintance_goal=survey.acquaintance_goal,
            first_name=user.first_name,
            last_name=user.last_name
        )
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
            serialized_survey = dict(
                id=survey.id,
                user=survey.user,
                stack=survey.stack,
                birth_date=survey.birth_date,
                specialization=survey.specialization,
                hobby=survey.hobby,
                region=survey.region,
                acquaintance_goal=survey.acquaintance_goal
            )
            serialized_surveys.append(serialized_survey)
        return serialized_surveys
    else:
        return False


@sync_to_async
def is_user(tg_id):
    try:
        User.objects.get(tg_id=tg_id)
        return True
    except User.DoesNotExist:
        return False


@sync_to_async
def send_message(**data):
    from_whom = User.objects.get(username=data['from_whom_username'])
    report = Report.objects.get(id=data['report_id'])
    chat_id = User.objects.get(reports=report).tg_id
    message = data['message']
    issue = Issue.objects.update_or_create(
        report=report, from_whom=from_whom, defaults={'question': message})
    issue_id = issue[0].id
    return chat_id, issue_id


@sync_to_async
def send_answer(**data):
    issue = Issue.objects.get(id=data['issue_id'])
    from_whom = issue.from_whom
    chat_id = from_whom.tg_id
    message = data['message']
    issue.answer = message
    issue.save()
    return chat_id


async def save_donation(tg_id: int, username: str, amount: int):
    user_model = get_user_model()
    user = None
    users = user_model.objects.filter(username=username)
    if await users.aexists():
        user = await users.afirst()

    if not user:
        users = user_model.objects.filter(tg_id=tg_id)
        if await users.aexists():
            user = await users.afirst()

    if not user:
        user = await user_model.objects.acreate(username=username, tg_id=tg_id)

    await Donation.objects.acreate(user=user, amount=amount)


@sync_to_async
def get_broadcast_list():
    users = User.objects.all()
    print(users)
    broadcast_list = [user.tg_id for user in users if user.tg_id]
    return broadcast_list


@sync_to_async
def get_watcher():
    number_watchers = len(Watcher.objects.all())
    try:
        control_number = Count.objects.last().current_number
    except AttributeError:
        control_number=Count.objects.create(current_number=0).current_number
    if number_watchers == control_number:
        return False
    else:
        report = Watcher.objects.last().report
        topic = report.topic
        speaker = report.speaker
        is_current = report.is_current
        if is_current:
            status = 'начался'
        else:
            status = 'закончился'
        return topic, speaker, status


@sync_to_async
def change_count():
    count = Count.objects.last()
    count.current_number += 1
    count.save()
