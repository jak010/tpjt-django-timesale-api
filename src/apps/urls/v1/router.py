from django.urls import path

from apps.views.v1 import product_view

urlpatterns = [
    path('products', product_view.ProductView.as_view()),
]
