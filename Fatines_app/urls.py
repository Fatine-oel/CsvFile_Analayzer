from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include  # Ajoute l'importation de 'include'
from gestion_fichiers import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Cette ligne est pour la vue 'home'
    path('gestion_fichiers/', include('gestion_fichiers.urls')),  # Inclut les urls de ton app 'gestion_fichiers'
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
