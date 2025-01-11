from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Page d'accueil
    path('upload/', views.upload_file, name='upload_file'),  # Formulaire de téléchargement de fichier
    path('view_data/', views.view_data, name='view_data'),  # Nouvelle page pour afficher les données
     path('stat_analysis/', views.stat_analysis, name='stat_analysis'),
    path('visualisation/', views.visualisation, name='visualisation'),
]
