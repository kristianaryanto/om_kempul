from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('recent/',views.recent),
    path('sklear/',views.sklear),
    path('tensorflow/',views.tensorflow),
    path('mlflow',views.mloflow),
    path('input',views.input)
]