from rest_framework.routers import DefaultRouter
from .views import CustomerList, CustomerDetail, ProductList
from django.conf.urls import url

app_name = "project"

urlpatterns = [
    url(
        r"^customer/$",
        CustomerList.as_view(),
        name="list",
    ),
    url(
        r"^customer/(?P<pk>[0-9]+)/$",
        CustomerDetail,
        name="detail",
    ),
    url(
        r"^products/$",
        ProductList,
        name="detail",
    ),
]