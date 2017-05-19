from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'), # Notice the URL has been named
    url(r'^my_account/$', views.MyAccountView.as_view(), name='my_account'),
    url(r'^my_groups/$', views.MyGroupsView.as_view(), name='my_groups'),
]