from django.urls import path
from . import views

urlpatterns = [
    path('fetch_claims_data/', views.fetch_claims_data, name='fetch_claims_data'),
    path('generate_graphs/', views.generate_graphs, name='generate_graphs'),
]