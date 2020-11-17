from django.conf.urls import url
from . import views
from django.urls import reverse_lazy


app_name = 'unazap'

urlpatterns = [
    # url(r'^testevalidatenew$', views.testevalidatenew, name='testevalidatenew'),
    url(r'^testevalidatenew$', views.testevalidatenew.as_view(), name='testevalidatenew'),
]
