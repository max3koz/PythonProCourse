from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Ad


@receiver(post_save, sender=Ad)
def check_ad_expiry(sender, instance, **kwargs):
	instance.deactivate_if_expired()
