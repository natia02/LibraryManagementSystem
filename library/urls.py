from django.urls import path, include
from rest_framework.routers import DefaultRouter

from library.views import (UserRegistrationView, LogoutView,
                           BookViewSet, BookReservationViewSet,
                           CustomLoginView)
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'reservations', BookReservationViewSet, basename='reservation')


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls))
]
