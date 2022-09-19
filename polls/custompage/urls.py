from django.urls import path
from polls.custompage  import views  as views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('title_edit', views.title_edit, name='title_edit'),
    path('header_edit', views.header_edit, name='header_edit'),
    path('html_edit', views.html_edit, name='html_edit'),
    path('form_edit', views.form_edit, name='form_edit'),
    path('feed_edit', views.feed_edit, name='feed_edit'),
    path('link_edit', views.link_edit, name='link_edit'),
    path('product_edit', views.product_edit, name='product_edit'),
    
]