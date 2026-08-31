from django.urls import path
from . import views

urlpatterns = [
    path("products/list/", views.ProductListCreate.as_view()),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDestroy.as_view(), name='product-retrive-update-delete'),
    path("collections/list/", views.collection_list),
    path("collections/<int:pk>/", views.collection_detail),
    path("cart/create/", views.CartCreateView.as_view()),
    path("cart/<str:pk>/", views.CartFetchUpdateDeleteView.as_view()),
    path("cart/<str:cart_pk>/items/", views.ListOrCreateOrUpdateCartItemViews.as_view()),
    path("cart/<str:cart_pk>/items/<int:pk>/", views.ListOrCreateOrUpdateCartItemViews.as_view()),
]
