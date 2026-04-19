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
    path('customers/', views.customer_list_api),
    path('create_customer/', views.create_customer_api),
    path("customers/<int:customer_id>/", views.customer_detail),
    path("edit-customers/<int:customer_id>/", views.edit_customer),
    path("delete-customers/<int:customer_id>/", views.delete_customer),
    path("ports/", views.port_list_api),
    path("create_port/", views.create_port_api),
    path("edit-ports/<int:port_id>/", views.port_detail),
    path("delete-port/<int:port_id>/", views.delete_port),
    path("cargos/", views.cargo_list),
    path("delete-cargo/<int:id>/", views.delete_cargo),
    path("create_cargo/", views.create_cargo_api),
    path('edit-cargo/<int:cargo_id>/', views.edit_cargo),
    path('operator_update_profile/', views.operator_update_profile),
    path('operator_get_profile/', views.operator_get_profile),
    path("orders/", views.orders_list),
    path("create_order/", views.create_order_api),
    path("order/<int:order_id>/", views.get_order_detail),
    path("order/update/<int:order_id>/", views.update_order_api),
    path("delete_order/<int:order_id>/", views.delete_order_api),
]