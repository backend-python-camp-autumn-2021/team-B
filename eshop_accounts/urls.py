from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



app_name = 'eshop_accounts'
urlpatterns = [
	# in
	path('login/', views.UserLogin.as_view(), name='login'),
	# out
	# path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('logout/', views.log_out, name='logout'),
	# signin
	path('signup/',views.SignUp.as_view(), name='signup'),
	# rest
	path('reset/', views.UserPassReset.as_view(), name='reset_pass'),
	path('reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
	path('confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
	path('confirm/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    # profile
	path('user', views.user_account_main_page,name='user'),
    path('user/edit',views.edit_user_profile,name='edit')
	
]