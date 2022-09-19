

from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path


urlpatterns = [
    path('signup',views.signup , name='signup'),
    
    path('configMail',views.configMail , name='configMail'),
    path('login', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),   
    path('confirm_change/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.confirm_change, name='confirm_change'),         
    path('deleteUser/<str:pk>/', views.deleteUser, name='deleteUser'),
    path('getconfig', views.getconfig, name='getconfig'),
    path('UserProfile', views.UserProfile, name='UserProfile'),
    path('custombutton', views.custombutton, name='custombutton'),
    path('Vcard_view', views.Vcard_view, name='Vcard_view'),
    path('get_vcardOthers/<str:pk>/', views.get_vcardOthers, name='get_vcardOthers'),
    path('get_platforms', views.get_platforms, name='get_platforms'),
    path('get_platform_ById/<str:pk>/', views.get_platform_ById, name='get_platform_ById'),
    path('social', views.social, name='social'),
    path('social_arrange', views.social_arrange, name='social_arrange'),
    path('direct', views.editIsDirectOn, name='editIsDirectOn'),
    path('favoriteUser', views.favoriteUser, name='favoriteUser'),
    path('get_socialOthers/<str:pk>/', views.get_socialOthers, name='get_socialOthers'),
    path('get_profileOthers/<str:pk>/', views.get_profileOthers, name='get_profileOthers'),
    path('change-password', views.ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


