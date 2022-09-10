from django.urls import path

from .views import *


app_name = 'farm'

urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path('registration/', RegistrationUserView.as_view(), name='reg'),
	path('login/', LoginUserView.as_view(), name='login'),
	path('logout/', logout_user, name='logout'),
	path('farm/', FarmMoneyView.as_view(), name='farm')
]