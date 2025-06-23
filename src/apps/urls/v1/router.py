from django.urls import path

from apps.views.v1 import product_view, timesale_view

urlpatterns = [
    path('products', product_view.ProductView.as_view()),
    path('timesales', timesale_view.TimeSaleView.as_view(), name='timesales'),
    path('timesales/ongoing', timesale_view.TimeSaleOngoingView.as_view(), name='timesales-ongoing'),
    path('timesales/<int:timesale_id>', timesale_view.TimeSaleDetailView.as_view(), name='timesales-detail'),
    path('timesales/<int:timesale_id>/purchase', timesale_view.TimeSaleOrderView.as_view(), name='timesales-order'),
]
