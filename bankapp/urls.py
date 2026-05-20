from django.urls import path
from . import views

urlpatterns = [
    path('open-account/', views.OpenAccount.as_view(), name='open-account'),
    path('bank-profile/', views.ProfileView.as_view(), name='bankapp-profile'),
    path('bank-transfer/', views.TransferView.as_view(), name='bank-transfer')
]