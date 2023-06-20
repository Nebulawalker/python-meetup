from loguru import logger
from django.contrib.auth.models import User

from asgiref.sync import sync_to_async


@sync_to_async
def create_new_user(tg_id, tg_full_name):
    User.objects.get_or_create(username=tg_id, first_name=tg_full_name)
    user = User.objects.get(username=tg_id)
    user.save()

