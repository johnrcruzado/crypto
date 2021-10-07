from django.urls import path
from main.views import *




urlpatterns = [
    path('', starter_pack, name='home'),
    path('scholar', ScholarView.as_view(), name='scholar'),
    path('payout/<str:pk>/', PayoutView.as_view(), name='payout'),
    path('fight-monster', starter_pack, name='home'),

    path('marketplace', market_place, name='market_place'),
    path('cockpit', cockpit, name='cockpit'),
    path('rooster', my_rooster, name='my_rooster'),
    path('breeding', breeding, name='breeding'),
]