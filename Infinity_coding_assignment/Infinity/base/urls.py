from django.urls import path
from django.http import HttpResponse
from . import views


urlpatterns = [
    path('', views.login, name="login"),
    path('signup/', views.signup, name="signup"),  
    path('home/', views.home, name="home"),  
    path('add_plan/', views.add_plan, name="add_plan"),  
    path('viewPlan/', views.viewPlan, name="viewPlan"),  
    path('logout/', views.logout, name="logout"),  

]
    
    
    
