from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    path('download/csv/', views.download_csv, name='download_csv'),
    path('download/pdf/', views.download_pdf, name='download_pdf'),
    path('transaction_list/', views.transaction_list, name='transaction_list'),
    path('stats/', views.stats_view, name='stats'),
    path('download-report/', views.generate_report, name='download_report'),


]
