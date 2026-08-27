from django.urls import path
from . import views

urlpatterns = [
    path("products/list/", views.ProductListCreate.as_view()),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDestroy.as_view(), name='product-retrive-update-delete'),
    path("collections/list/", views.collection_list),
    path("collections/detail/<int:pk>/", views.collection_detail),
]
