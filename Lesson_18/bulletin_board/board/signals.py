from datetime import timedelta

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Ad


@receiver(post_save, sender=Ad)
def check_ad_expiry(sender, instance, **kwargs):
	instance.deactivate_if_expired()


@receiver(post_save, sender=Ad)
def auto_deactivate_expired_ad(sender, instance: Ad, **kwargs) -> None:
	"""Automatically deactivates ads older than 30 days upon save."""
	if instance.is_active and timezone.now() > instance.created_at + timedelta(
			days=30):
		instance.is_active = False
		instance.save()


@receiver(post_save, sender=Ad)
def send_ad_creation_email(sender, instance: Ad, created: bool,
                           **kwargs) -> None:
	"""Sends an email to the user when a new ad is created."""
	if created:
		subject = 'Your ad has been posted!'
		message = (f"Hi {instance.user.username},\n\nYour ad '{instance.title}' "
		           f"has been successfully created.")
		recipient_list = [instance.user.email]
		send_mail(subject, message, None, recipient_list)
