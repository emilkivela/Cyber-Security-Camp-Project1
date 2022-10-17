from django.urls import path

from .views import homepageView, signinView, transferView, confirmView, transactionView

urlpatterns = [
    path('', homepageView, name='index'),
    path('signin/', signinView, name="signin"),
    path('transfer/', transferView, name='transfer'),
    path('confirm/', confirmView, name='confirm'),
    path('transactions/', transactionView, name='transactions')
]