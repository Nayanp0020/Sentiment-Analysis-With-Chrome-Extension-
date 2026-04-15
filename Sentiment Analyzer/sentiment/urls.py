from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_sentiment, name='home'),
    path('predict/', views.predict_sentiment, name='predict'),
    path('api/sentiment/', views.analyze_sentiment, name='analyze_sentiment'),
]
