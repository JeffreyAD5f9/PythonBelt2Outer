from django.conf.urls import url
from . import views
urlpatterns = [
url(r'^$', views.index),
url(r'^register$', views.register),
url(r'^gotoTripManager$', views.gotoTripManager),
url(r'^gotoAddTrip$', views.gotoAddTrip),
url(r'^login$', views.login),
url(r'^logout$', views.logout),
url(r'^tripCreate$', views.tripCreate),
url(r'^remove/(?P<destRemove>\d+)$', views.remove),
url(r'^viewDestination/(?P<destination>\d+)$', views.viewDestination),
url(r'^joinTrip/(?P<trip>\d+)$', views.joinTrip)

]
