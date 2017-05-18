from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'), # Notice the URL has been named
    url(r'^somepage/$', views.SomePageView.as_view(), name='somepage'),
]