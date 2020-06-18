"""
Aa test url conf in which the django admin is pointing to admin

"""
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
]
