from django.urls import path
from adminApp import views


urlpatterns = [
    path('admin/home',views.AdminHomeView.as_view(),name='admin_home'),
   
    path('admin/user-list',views.AdminUserListView.as_view(),name='admin_user_list'),
    path('admin/edit-user/<int:id>', views.AdminEditUserView.as_view(), name='admin_edit_user'),
    path('admin/delete-user/<int:id>', views.AdminDeleteUserView.as_view(), name='admin_delete_user'),


    path('admin/order-list',views.AdminOrderListView.as_view(),name='admin_order_list'),
    path('admin/pending-order-list',views.AdminPendingOrderListView.as_view(),name='admin_pending_order_list'),
    path('admin/update-order/<int:id>', views.OrderUpdateView.as_view(), name='update_order'),
    path('admin/delete-order/<int:id>', views.OrderDeleteView.as_view(), name='delete_order'),

    path('admin/product-list',views.AdminProductListView.as_view(),name='admin_product_list'),
    path('admin/delete-product/<int:pk>', views.AdminDeleteProductView.as_view(), name='admin_delete_product'),
    path('admin/create-product', views.AdminCreateProductView.as_view(), name='admin_create_product'),
    path('admin/edit-product/<int:id>', views.EditProductView.as_view(), name='admin_edit_product'),


    path('admin/category-list',views.AdminCategoryListView.as_view(),name='admin_category_list'),
    path('admin/create-category', views.CategoryCreateView.as_view(), name='admin_create_category'),
    path('admin/edit-category/<int:pk>', views.CategoryUpdateView.as_view(), name='admin_edit_category'),
    path('admin/delete-category/<int:pk>', views.CategoryDeleteView.as_view(), name='admin_delete_category'),

]
