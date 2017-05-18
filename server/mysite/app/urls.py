from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'), # Notice the URL has been named
    url(r'^about/$', views.SomePageView.as_view(), name='somepage'),
]