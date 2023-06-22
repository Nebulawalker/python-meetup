from users.models import User
from tg_bot.models import Report


def identify_user(tg_id):
    try:
        if User.objects.get(tg_id=tg_id).reports.last():
            return 'reporter'
        else:
            return 'hearer'
    except User.DoesNotExist:
        return 'hearer'


def get_reports():
    reports = Report.objects.all().order_by('ends_at')
    serialized_reports = []
    for report in reports:
        serialized_report = dict(id=report.id, topic=report.topic, speaker=report.speaker, starts_at=report.starts_at,
                                 ends_at=report.ends_at)
        serialized_reports.append(serialized_report)
    return serialized_reports


def get_report(report_id):
    report = Report.objects.get(id=report_id)
    serialized_report = dict(id=report.id, topic=report.topic, speaker=report.speaker, starts_at=report.starts_at,
                             ends_at=report.ends_at, is_current=report.is_current)
    return serialized_report
