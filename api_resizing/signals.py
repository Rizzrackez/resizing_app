from django.db.models.signals import pre_delete
from django.dispatch import receiver
from api_resizing.models import Picture
from resizing_app import settings
import os


@receiver(pre_delete, sender=Picture)
def my_handler(sender, instance, **kwargs):
    """Удаления картинки из дериктории с изображениями (в DEBUG=True режиме)"""
    if settings.DEBUG:
        try:
            os.remove(instance.picture.path)
        except:
            pass



