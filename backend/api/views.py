from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from datetime import date
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    
# ------------------------
# CATEGORY VIEWS
# ------------------------
class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


# ------------------------
# TRANSACTION VIEWS
# ------------------------
class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        
        # Filters
        category = self.request.query_params.get('category')
        type = self.request.query_params.get('type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if category:
            queryset = queryset.filter(category__name=category)
        if type:
            queryset = queryset.filter(type=type.upper())
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset.order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


# ------------------------
# SUMMARY VIEW
# ------------------------
class SummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        transactions = Transaction.objects.filter(user=user)

        total_income = transactions.filter(type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
        total_expense = transactions.filter(type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0
        net_balance = total_income - total_expense

        # Group by category
        category_summary = (
            transactions.filter(type='EXPENSE')
            .values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )

        data = {
            "total_income": total_income,
            "total_expense": total_expense,
            "net_balance": net_balance,
            "category_breakdown": category_summary,
        }
        return Response(data)