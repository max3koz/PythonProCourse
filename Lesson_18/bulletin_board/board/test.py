from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Ad, Category, Comment, UserProfile


class AdTestCase(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='maksym',
		                                     password='12345')
		self.category = Category.objects.create(name='Test',
		                                        description='Test category')
	
	def test_active_ads_count(self):
		category = Category.objects.create(name='Cars',
		                                   description='Car listings')
		ad = Ad.objects.create(
			title='Selling a car',
			description='Excellent condition',
			price=10000,
			user=self.user,
			category=category
		)
		self.assertEqual(category.active_ads_count(), 1)
	
	def test_inactive_ads_count(self):
		category = Category.objects.create(name='Cars',
		                                   description='Car listings')
		ad = Ad.objects.create(
			title='Selling a car',
			description='Excellent condition',
			price=10000,
			user=self.user,
			category=category
		)
		self.assertEqual(category.active_ads_count(), 1)
		
		ad.is_active = False
		ad.save()
		self.assertEqual(category.active_ads_count(), 0)
	
	def test_short_description(self):
		ad = Ad.objects.create(
			title='Selling apartment',
			description='Beautiful sea view. ' * 10,
			price=50000,
			user=self.user,
			category=self.category
		)
		self.assertLessEqual(len(ad.short_description()), 103)
	
	def test_price_validation(self):
		ad = Ad(
			title='Invalid price',
			description='Test ad',
			price=-100,
			user=self.user,
			category=self.category
		)
		with self.assertRaises(Exception):
			ad.full_clean()
	
	def test_deactivate_if_expired(self):
		ad = Ad.objects.create(
			title='Old ad',
			description='Expired listing',
			price=50000,
			user=self.user,
			category=self.category
		)
		ad.created_at = timezone.now() - timedelta(days=31)
		ad.save()
		ad.deactivate_if_expired()
		ad.refresh_from_db()
		self.assertFalse(ad.is_active)
	
	def test_comment_creation(self):
		ad = Ad.objects.create(
			title='Repair services',
			description='Fast and reliable',
			price=300,
			user=self.user,
			category=self.category
		)
		comment = Comment.objects.create(
			content='Interested in service',
			ad=ad,
			user=self.user
		)
		self.assertEqual(ad.comment_count(), 1)
		self.assertEqual(comment.content, 'Interested in service')
	
	def test_profile_created(self):
		user = User.objects.create_user(username='newuser', password='12345')
		profile = UserProfile.objects.get(user=user)
		self.assertIsNotNone(profile)
		self.assertEqual(profile.phone, '')
	
	def test_signal_deactivates_expired_ad(self):
		ad = Ad.objects.create(
			title='Signal test ad',
			description='Test signal',
			price=100,
			user=self.user,
			category=self.category
		)
		ad.created_at = timezone.now() - timedelta(days=31)
		ad.save()
		ad.deactivate_if_expired()
		ad.refresh_from_db()
		self.assertFalse(ad.is_active)
	
	def test_signal_does_not_deactivate_recent_ad(self):
		ad = Ad.objects.create(
			title='Recent Ad',
			description='Fresh ad',
			price=100,
			user=self.user,
			category=self.category
		)
		ad.created_at = timezone.now() - timedelta(days=10)
		ad.save()
		ad.refresh_from_db()
		self.assertTrue(ad.is_active)
	
	def test_recent_ads(self):
		ad_recent = Ad.objects.create(
			title='Recent ad',
			description='Description',
			price=100,
			user=self.user,
			category=self.category,
			created_at=timezone.now() - timedelta(days=10)
		)
		ad_old = Ad.objects.create(
			title='Old ad',
			description='Description',
			price=200,
			user=self.user,
			category=self.category
		)
		ad_old.created_at = timezone.now() - timedelta(days=40)
		ad_old.save()
		
		recent_ads = Ad.objects.filter(
			created_at__gte=timezone.now() - timedelta(days=30)
		)
		self.assertIn(ad_recent, recent_ads)
		self.assertNotIn(ad_old, recent_ads)
