import os
from datetime import timedelta

import django
import pytest
from django.core import mail
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone

from .models import Category, Ad, Comment, UserProfile

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'bulletin_board.settings')
django.setup()


@pytest.fixture
def user() -> User:
	"""
	Creates a test user.
	Returns: User: A newly created Django user.
	"""
	return User.objects.create_user(username='maksym', password='12345')


@pytest.fixture
def category() -> Category:
	"""
	Creates a test category.
	Returns: Category: A newly created category instance.
	"""
	return Category.objects.create(name='Test', description='Test category')


@pytest.mark.django_db
def test_active_ads_count(user: User) -> None:
	"""
	Verifies that Category.active_ads_count() returns correct count
	before and after deactivating an ad.
	"""
	category = Category.objects.create(name='Cars', description='Car listings')
	ad = Ad.objects.create(
		title='Selling a car',
		description='Excellent condition',
		price=10000,
		user=user,
		category=category
	)
	assert category.active_ads_count() == 1
	ad.is_active = False
	ad.save()
	assert category.active_ads_count() == 0


@pytest.mark.django_db
def test_short_description(user: User, category: Category) -> None:
	"""
	Verifies that Ad.short_description() returns a string no longer
	than 103 characters.
	"""
	ad = Ad.objects.create(
		title='Selling apartment',
		description='Beautiful sea view. ' * 10,
		price=50000,
		user=user,
		category=category
	)
	assert len(ad.short_description()) <= 103


@pytest.mark.django_db
def test_price_validation(user: User, category: Category) -> None:
	"""Verifies that an ad with a negative price raises a validation error."""
	ad = Ad(
		title='Invalid price',
		description='Test ad',
		price=-100,
		user=user,
		category=category
	)
	with pytest.raises(Exception):
		ad.full_clean()


@pytest.mark.django_db
def test_deactivate_if_expired(user: User, category: Category) -> None:
	"""
	Verifies that Ad.deactivate_if_expired() sets is_active to False
	if the ad is older than 30 days.
	"""
	ad = Ad.objects.create(
		title='Old ad',
		description='Expired listing',
		price=50000,
		user=user,
		category=category
	)
	ad.created_at = timezone.now() - timedelta(days=31)
	ad.save()
	ad.deactivate_if_expired()
	ad.refresh_from_db()
	assert not ad.is_active


@pytest.mark.django_db
def test_comment_creation(user: User) -> None:
	"""Verifies that a comment can be created and linked to an ad."""
	category = Category.objects.create(name='Services',
	                                   description='Service ads')
	ad = Ad.objects.create(
		title='Repair services',
		description='Fast and reliable',
		price=300,
		user=user,
		category=category
	)
	comment = Comment.objects.create(content='Interested in service',
	                                 ad=ad,
	                                 user=user)
	assert ad.comment_count() == 1
	assert comment.content == 'Interested in service'


@pytest.mark.django_db
def test_profile_created() -> None:
	"""
	Verifies that a UserProfile is automatically created when a User is created.
	"""
	user = User.objects.create_user(username='maksym', password='12345')
	profile = UserProfile.objects.get(user=user)
	assert profile is not None
	assert profile.phone == ''


@pytest.mark.django_db
def test_signal_deactivates_expired_ad(user: User, category: Category) -> None:
	"""Verifies that expired ads are deactivated via signal or method logic."""
	ad = Ad.objects.create(
		title='Signal test ad',
		description='Test signal',
		price=100,
		user=user,
		category=category
	)
	ad.created_at = timezone.now() - timedelta(days=31)
	ad.save()
	ad.deactivate_if_expired()
	assert not ad.is_active


@pytest.mark.django_db
def test_signal_does_not_deactivate_recent_ad() -> None:
    """Verifies that ads newer than 30 days remain active."""
    user: User = User.objects.create_user(username='maksym', password='12345')
    category: Category = Category.objects.create(name='Test',
                                                 description='Test category')

    ad: Ad = Ad.objects.create(
        title='Recent Ad',
        description='Fresh ad',
        price=100,
        user=user,
        category=category
    )
    ad.created_at = timezone.now() - timedelta(days=10)
    ad.save()

    ad.refresh_from_db()
    assert ad.is_active

@pytest.mark.django_db
def test_recent_ads(user: User, category: Category) -> None:
	"""Verifies that only ads created within the last 30 days are returned."""
	ad_recent = Ad.objects.create(
		title='Recent ad',
		description='Description',
		price=100,
		user=user,
		category=category,
		created_at=timezone.now() - timedelta(days=10)
	)
	ad_old = Ad.objects.create(
		title='Old ad',
		description='Description',
		price=200,
		user=user,
		category=category
	)
	ad_old.created_at = timezone.now() - timedelta(days=40)
	ad_old.save()
	
	recent_ads = Ad.objects.filter(
		created_at__gte=timezone.now() - timedelta(days=30))
	assert ad_recent in recent_ads
	assert ad_old not in recent_ads


@pytest.mark.django_db
def test_active_ads_in_category(user: User, category: Category) -> None:
	"""Verifies that only active ads are returned for a given category."""
	ad_active = Ad.objects.create(
		title='Active ad',
		description='Description',
		price=100,
		user=user,
		category=category
	)
	ad_inactive = Ad.objects.create(
		title='Inactive ad',
		description='Description',
		price=200,
		user=user,
		category=category,
		is_active=False
	)
	
	active_ads = Ad.objects.filter(category=category, is_active=True)
	assert ad_active in active_ads
	assert ad_inactive not in active_ads


@pytest.mark.django_db
def test_comment_count(user: User, category: Category) -> None:
	"""
	Verifies that comment count annotation returns correct number of comments
	per ad.
	"""
	ad = Ad.objects.create(
		title='Ad with comments',
		description='Description',
		price=100,
		user=user,
		category=category
	)
	Comment.objects.create(content='Comment 1', ad=ad, user=user)
	Comment.objects.create(content='Comment 2', ad=ad, user=user)
	
	ad_with_count = Ad.objects.annotate(comment_count=Count('comment')).get(
		id=ad.id)
	assert ad_with_count.comment_count == 2


@pytest.mark.django_db
def test_user_ads(user: User, category: Category) -> None:
	"""Verifies that all ads created by a specific user are returned."""
	Ad.objects.create(title='Ad 1', description='Description', price=100,
	                  user=user, category=category)
	Ad.objects.create(title='Ad 2', description='Description', price=200,
	                  user=user, category=category)
	Ad.objects.create(title='Ad 3', description='Description', price=300,
	                  user=user, category=category)
	
	user_ads = Ad.objects.filter(user=user)
	assert user_ads.count() == 3
	
	
@pytest.mark.django_db
def test_email_sent_on_ad_creation() -> None:
    """Verifies that an email is sent to the user when a new ad is created."""
    user: User = User.objects.create_user(
        username='maksym',
        password='12345',
        email='max3koz@gmail.com'
    )
    category: Category = Category.objects.create(name='Test',
                                                 description='Test category')

    Ad.objects.create(
        title='New Ad',
        description='Ad description',
        price=100,
        user=user,
        category=category
    )

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == 'Your ad has been posted!'
    assert 'New Ad' in mail.outbox[0].body
    assert mail.outbox[0].to == ['max3koz@gmail.com']
