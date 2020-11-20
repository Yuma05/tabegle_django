from django.urls import path, include
from rest_framework import routers

from api.views import SearchShop, SearchPlace, SearchCategory, UserShopList, UserShopChange
#
# router = routers.DefaultRouter()
# router.register(r'user-shop', UserShopControl, basename='UserShop')

urlpatterns = [
    path(r'search/shop/', SearchShop.as_view()),
    path(r'search/place/', SearchPlace.as_view()),
    path(r'search/category/', SearchCategory.as_view()),
    path(r'user-shop/', UserShopList.as_view()),
    path(r'user-shop/<int:pk>', UserShopChange.as_view(), name='detail'),
    path(r'dj-rest-auth/', include('dj_rest_auth.urls')),
    path(r'dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))
]
