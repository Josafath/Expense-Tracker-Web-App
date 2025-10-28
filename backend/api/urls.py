from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    # Auth (JWT)
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Categories
    path('categories/', views.CategoryListCreateView.as_view(), name='category_list_create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),

    # Transactions
    path('transactions/', views.TransactionListCreateView.as_view(), name='transaction_list_create'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction_detail'),

    # Summary
    path('summary/', views.SummaryView.as_view(), name='summary'),
]
