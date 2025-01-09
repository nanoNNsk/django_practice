from django.urls import path,include
from .api import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('router',Bookviewset,basename='router')

urlpatterns = [
    path('',include(router.urls))
    
]