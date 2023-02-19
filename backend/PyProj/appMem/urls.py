from django.urls import path
from . import views

urlpatterns = [
    path('getDataImage/', views.getImage),
    path('setCookie/', views.sendCookie)
]
