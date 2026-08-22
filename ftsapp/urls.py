"""
URL configuration for ftsapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from os import name
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainapp import views
from adminapp.views import *
from userapp.views import *

urlpatterns = [
    path('softproadmin/', admin.site.urls,name="softproadmin"),
    path('', views.Index, name='Index'),
    path('adminlogin/', views.Adminlogin, name='adminlogin'),
    path('userlogin/', views.UserLogin, name='userlogin'),
    path('admindash/', Admindash, name='admindash'),
    path('adminlogout/', AdminLogout, name='adminlogout'),
    path('adddept/', Adddept, name='adddept'),
    path('viewdept/', ViewDept, name='viewdept'),
    path('deletedept/<dept_id>/', DeleteDept, name='deletedept'),
    path('addemp/', AddEmp, name='addemp'),
    path('viewemp/', ViewEmp, name='viewemp'),
    path('deleteemp/<path:empemail>/', DeleteEmp, name='deleteemp'),
    path('changeadminpwd/', ChangeAdminPwd, name='changeadminpwd'),
    path('adminallfiles/', ViewAllFiles, name='adminallfiles'),
    path('adminfiledetails/<fid>/', AdminFileDetails, name='adminfiledetails'),
    path('userdash/', Userdash, name='userdash'),
    path('userlogout/', Userlogout, name='userlogout'),
    path('viewprofile/', ViewProfile, name='viewprofile'),
    path('initiatefile/', InitiateFile, name='initiatefile'),
    path('updateprofile/', UpdateProfile, name='updateprofile'),
    path('viewfiles/', ViewFiles, name='viewfiles'),
    path('receivedfiles/', RecivedFiles, name='recievedfiles'),
    path('changeuserpwd/', ChangeUserPwd, name='changeuserpwd'),
    path('filedetails/<fid>/', FileDetails, name='filedetails'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
