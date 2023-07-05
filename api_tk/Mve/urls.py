from django.urls import path
from Mve.views import Mvl,MvDetail

urlpatterns = [
    path('', Mvl.as_view()),
    path('<str:pk>', MvDetail.as_view())
]