from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet
from .views import initiate_payment, verify_payment

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns = [
    # example:
    path('', views.home, name='home'),  # or whatever views you have
]

urlpatterns = [
    path('initiate-payment/', initiate_payment, name='initiate-payment'),
    path('verify-payment/', verify_payment, name='verify-payment'),
]
