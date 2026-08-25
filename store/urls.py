from django.urls import path
from . import views

urlpatterns = [
    path("products/list/", views.product_list),
    path("products/detail/<int:pk>/", views.product_detail),
    path("collections/list/", views.collection_list),
    path("collections/detail/<int:pk>/", views.collection_detail),
]
