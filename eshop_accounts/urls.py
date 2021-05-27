from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .api import api
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token


app_name = 'eshop_accounts'
urlpatterns = [
	# login
	path('login/', views.UserLogin.as_view(), name='login'),
	# out
	# path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('logout/', views.log_out, name='logout'),
	# signin
	path('signup/',views.SignUpCustomer.as_view(), name='signup'),
	path('signupsuplier/',views.SignUpSuplier.as_view(), name='signupsuplier'),
	# rest
	path('reset/', views.UserPassReset.as_view(), name='reset_pass'),
	path('reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
	path('confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
	path('confirm/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    # profile
    path('user/edit/<int:pk>/',views.UpdateCustomerView.as_view(),name='edit'),
	path('user-profile', views.CustomerProfileView.as_view(),name='user_profile'),
	path('create-product/', views.CreateProductView.as_view(), name='create_product'),
	path('profile/', views.SuplierProfileView.as_view(), name='supplier_profile'),
	# email
	path('email-verification/<int:user_uuid>/<str:user_email>/', views.verify, name='email_verify'),
	# api
	# login
	path('login-api/',obtain_jwt_token,name='login_api'),
	path('api-token-refresh/', refresh_jwt_token),
	# out
	path('logout-api/', api.LogoutApi.as_view(), name='logout_api'),
	# email
	path('email-verify-api/<int:user_uuid>/<str:user_email>/', api.EmailVerifyApiView.as_view(), name='email_verify_api'),

	# signup
	path('signup-api/',api.SignupCreate.as_view(),name='signup_api'),
	path('signupcustomer-api/',api.SignupCreateCustomer.as_view(),name='signupcustomer_api'),
	path('signupsuplier-api/',api.SignupCreateSuplier.as_view(),name='signupsuplier_api'),
	path('create-supplier-product/', api.SuplierCreateProduct.as_view(), name='create_supplier_product'),

	# profile
	path('customer-profile-api/',api.CustomerProfileView.as_view(),name='customer_profile_api'),
	path('suplier-profileView-api/',api.SuplierProfileView.as_view(),name='suplier_profileView_api'),
	
    # update
	path('update-customer-api/',api.UpdateCustomerProfile.as_view(),name='update_customer_api'),
	# path('CustomerProfile-api/',api.CustomerProfileView.as_view(),name='CustomerProfile_api'),



	
]