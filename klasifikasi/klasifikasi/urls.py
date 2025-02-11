"""
URL configuration for klasifikasi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from administrator import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.v_login, name='login'),
    path('login/submit/', views.login, name='proses_login'),
    path('logout/', views.logout, name='logout'),
    path('ind-nanas', views.inputdatananas, name='inputdatananas'),
    path('ind-gejala', views.inputdatagejala, name='inputdatagejala'),
    path('ind-penyakit', views.inputdatapenyakit, name='inputdatapenyakit'),
    path('proses-mpl', views.prosesmpl, name='prosesmpl'),
    path('hasil-klasifikasi', views.hasilklasifikasi, name='hasilklasifikasi'),
    path('riwayat-klasifikasi', views.riwayatklasifikasi, name='riwayatklasifikasi'),
    path('import/', views.import_data_nanas, name='import_data_nanas'),
    path('kosongkan/', views.kosongkan_data_nanas, name='kosongkan_data_nanas'),
    path('simpan-klasifikasi/', views.simpan_klasifikasi, name='simpan_klasifikasi'),
    path('refresh-datalatih/', views.refresh_datalatih, name='refresh_datalatih'),

]

# Tambahkan URL untuk media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)