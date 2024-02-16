from django.urls import path
from mainApp import views

urlpatterns = [
    path('login/', views.loginpage),
    path('logout/', views.logoutpage),
    path('', views.indexpage),
    path('visitor/', views.visitorpage),
    path('add-receptionist/', views.addReceptionist),
    path('viewRecptionist/', views.view_Receptionist),
    path('add-new-visitor/', views.addnewVisitor),
    path('buisenessVisit/', views.BusinessVisit),
    path('personalVisitor/', views.personalVisit),
    path('job-visit/', views.jobVisit),
    path('view-profile/', views.viewProfile),
    path('delete-visitor/<int:id>/', views.removeVisitorPage),
    path('delete-recep/<int:id>/', views.removeRecepPage),
    path('update-recep/<int:id>/', views.updateRecepPage),
    path('update-visitor/<int:id>/', views.updateVisitorPage),
]