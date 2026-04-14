from django.urls import path
# from .views import login, retrieve_password, report_dashboard, user_management,toggle_user_status
from . import views
app_name = 'main'  # 可选，命名空间

urlpatterns = [
    path('login/', views.login, name='login'),
    path('retrieve_password/', views.retrieve_password, name='retrieve_password'),
    path('dashboard/', views.report_dashboard, name='report_dashboard'),
    path('user_management/', views.user_management, name='user_management'),
    path('toggle_user_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('get_profile/', views.get_profile),
    path('administrator_update_profile/', views.administrator_update_profile),
    path('report/', views.operator_report),
    path('user_info/', views.operator_user_info_api),
    
]