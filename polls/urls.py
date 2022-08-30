

from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path


urlpatterns = [
    path('signup',views.signup , name='signup'),
    path('login', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),   
    path('confirm_change/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.confirm_change, name='confirm_change'),         
    path('deleteUser/<str:pk>/', views.deleteUser, name='deleteUser'),
    path('getconfig', views.getconfig, name='getconfig'),
    path('updateUserProfile', views.updateUserProfile, name='updateUserProfile'),
    path('getUserProfile', views.getUserProfile, name='getUserProfile'),

    path('change-password/<int:pk>/', views.ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

