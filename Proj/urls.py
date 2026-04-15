from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('test/', views.test, name='test'),
    path('concept/<str:id_unique>/', views.concept, name='concept'),
    path('modifier/<str:id_unique>/', views.modifier_objet, name='modifier_objet'),
    path('information/', views.information, name='information'),
    path('cart/', views.cart, name='cart'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('', views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)