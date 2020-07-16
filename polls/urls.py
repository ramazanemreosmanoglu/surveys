from django.conf.urls import url
from . import views

app_name = "polls"

urlpatterns = [
    url(r"^add/$", views.add, name="add"),
    url(r"^(?P<slug>[\w-]+)/$", views.DetailView.as_view(), name="detail"),
    url(r'/', views.index, name="surveys"),
]
