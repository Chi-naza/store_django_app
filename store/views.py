from django.db.models.aggregates import Count
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView # for class based views
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer



class ProductListCreate(ListCreateAPIView):
    # For Search Filtering & For Sorting (orderingFilter)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["amount", "last_updated"]

    # For Pagination - to this list only
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Product.objects.all()

    def get_serializer_class(self):
        return ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}
    
   


class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
            return Product.objects.all()
    
    def get_serializer_class(self):
        return ProductSerializer

    # Overriding the main delete method gives you full control over the response
    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        
        if product.orderitems.count() > 0:
            # Returns standard JSON with a 400 Status code instantly
            return Response(
                {"error": f"{product.title} cannot be deleted because it has been ordered"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        prod_query = Product.objects.all()
        serializer = ProductSerializer(prod_query, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        # deserializing
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        


@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        if product.orderitems.count() > 0:
            return Response({"error": f"{product.title} cannot be deleted because it has been ordered"})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(["GET", "POST"])
def collection_list(request):
    if request.method == "GET":
        collec_query = Collection.objects.all()
        serializer = CollectionSerializer(collec_query, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        # deserializing
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(["GET", "PUT", "DELETE"])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)

    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        if collection.product.count() > 0:
            return Response({"error": f"{collection.title} cannot be deleted because it has been attached to product(s)"})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
