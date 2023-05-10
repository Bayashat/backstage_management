from django.urls import path
from .views_dir import depart, staff, admin, account, order, user

app_name = 'api'

urlpatterns = [
    #       1) Department management
    path('depart/list/', depart.depart_list, name='depart_list'),  # Show list of Departments
    path('depart/add/', depart.depart_add, name='depart_add'),  # Add Department
    path('depart/delete/', depart.depart_delete, name='depart_delete'),   # Delete Department

    path('depart/<int:nid>/edit/', depart.depart_edit, name='depart_edit'),  # Edit Department

    #       2) Staff management
    path('staff/list/', staff.staff_list, name='staff_list'),   # Employee List
    path('staff/add/', staff.staff_add, name='staff_add'),   # Add Staff
    path('staff/<int:nid>/edit/', staff.staff_edit, name='staff_edit'),   # Edit Staff info
    path('staff/<int:nid>/delete/', staff.staff_delete, name='staff_delete'),  # Delete Staff info

    #       3) Administrator's management
    path('', admin.admin_list, name='admin_list'),  # Admin List
    path('Admin/add/', admin.admin_add, name='admin_add'),  # Add Admin
    path('Admin/<int:nid>/edit/', admin.admin_edit, name='admin_edit'),    # Edit Admin Info
    path('Admin/<int:nid>/delete/', admin.admin_delete, name='admin_delete'),   # Delete Admin
    path('Admin/<int:nid>/reset/', admin.admin_reset, name='admin_reset'),  # 4.4) Reset Admin Password

    #       4) Account Management
    path('login/', account.login, name='login'),
    path('logout/', account.logout, name='logout'),
    path('image/code/', account.image_code, name='image_code'),

    #       5) User Management
    path('user/list/', user.user_list, name='user_list'),   # User List
    path('user/add/', user.user_add, name='user_add'),   # Add User
    path('user/<int:nid>/edit/', user.user_edit, name='user_edit'),   # Edit User info
    path('user/<int:nid>/delete/', user.user_delete, name='user_delete'),  # Delete User info

    #       5) Order Management
    path('order/list/', order.order_list, name='order_list'),  # Order List
    path('order/add/', order.order_add, name='order_add'),  # Add Order
    path('order/delete/', order.order_delete, name='order_delete'),  # Delete Order
    path('order/detail/', order.order_detail, name='order_delete'),  # Order detail info
    path('order/edit/', order.order_edit, name='order_edit'),  # Edit Order
]
