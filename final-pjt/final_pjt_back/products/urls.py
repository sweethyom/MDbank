from . import views
from django.urls import path


urlpatterns = [
    path('save_product/', views.save_product),      # 예적금 데이터 저장
    path('productlist/', views.productlist),
    path('exchange_rate/', views.exchange_rate),
    path('asset_type/', views.asset_type),  # 자산관리 유형검사
    # path('rate_comparison/', views.rate_comparison) # 금리 비교
    path('save-exchange-rates/', views.save_exchange_rates, name='save_exchange_rates'),
    path('request-currency/', views.request_currency, name='request_currency'),
    path('recommend/', views.recommend),
]
