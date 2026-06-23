from django.urls import path
from . import views

urlpatterns = [
    # Giving 'name=home' to the document list ensures templates can render safely
    path('', views.document_list, name='home'), 
    path('list/', views.document_list, name='document_list'),
    path('upload/', views.document_upload, name='document_upload'),
    path('<int:pk>/', views.document_detail, name='document_detail'),
    
    # Manager Action Pathway
    path('<int:pk>/review/', views.review_document, name='review_document'),
]