from django.urls import path
from .views import *
urlpatterns=[
    path('api/',prod.as_view(),name="prod"),
    path('comp/',comp.as_view(),name="comp")
]