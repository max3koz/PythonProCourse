from datetime import timedelta
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class UserProfile(models.Model):
    """
    Extended profile model linked to Django's built-in User.
    Fields:
        user (User): One-to-one relationship with the User model.
        phone (str): Optional phone number.
        address (str): Optional address.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} Profile"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance: User,
                                  created: bool, **kwargs) -> None:
    """
    Signal handler to create or update UserProfile when a User is saved.
    Args:
        sender: The model class (User).
        instance: The actual instance being saved.
        created: Boolean indicating if the instance was newly created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()


class Category(models.Model):
    """
    Represents a category for ads.
    Fields:
        name (str): Unique name of the category.
        description (str): Description of the category.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def active_ads_count(self) -> int:
        """
        Returns the number of active ads in this category.
        Returns: int: Count of active ads.
        """
        return self.ad_set.filter(is_active=True).count()

    def __str__(self) -> str:
        return self.name


class Ad(models.Model):
    """
    Represents an advertisement posted by a user.
    Fields:
        title (str): Title of the ad.
        description (str): Full description.
        price (Decimal): Price of the item/service.
        created_at (datetime): Timestamp when the ad was created.
        updated_at (datetime): Timestamp when the ad was last updated.
        is_active (bool): Whether the ad is currently active.
        user (User): The user who posted the ad.
        category (Category): The category the ad belongs to.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def short_description(self) -> str:
        """
        Returns a shortened version of the description (max 100 characters).
        Returns: str: Truncated description with ellipsis if needed.
        """
        return self.description[:100] + "..." \
	        if len(self.description) > 100 else self.description

    def deactivate_if_expired(self) -> None:
        """Deactivates the ad if it is older than 30 days."""
        if (self.is_active and
		        timezone.now() > self.created_at + timedelta(days=30)):
            self.is_active = False
            self.save()
        
    def comment_count(self) -> int:
	    """Returns the number of comments associated with this ad."""
	    return self.comment_set.count()

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """
    Represents a comment left by a user on an ad.
    Fields:
        content (str): The comment text.
        created_at (datetime): Timestamp when the comment was created.
        ad (Ad): The ad being commented on.
        user (User): The user who wrote the comment.
    """
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Comment by {self.user.username} on {self.ad.title}"
