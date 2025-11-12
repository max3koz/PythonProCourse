from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomView, CustomModelViewSet

router = DefaultRouter()
router.register(r'custommodel', CustomModelViewSet)

urlpatterns = [
	path('', CustomView.as_view(), name='core-home'),
	path('api/', include(router.urls)),
]
