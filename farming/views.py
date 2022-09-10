from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout

from .models import *


# Create your views here.
class IndexView(TemplateView):
	template_name = 'farm/index.html'

class RegistrationUserView(CreateView):
	model = User
	template_name = 'farm/reg.html'
	form_class = UserCreationForm
	success_url = reverse_lazy('farm:index')

	def form_valid(self, form):
		user = form.save()
		p = Profile(
			user = user
		)
		p.save()
		login(self.request, user)
		return HttpResponseRedirect(reverse('farm:index'))

class LoginUserView(LoginView):
	template_name = 'farm/login.html'
	form_class = AuthenticationForm

	def get_success_url(self):
		return reverse('farm:index')


class FarmMoneyView(TemplateView):
	template_name = 'farm/farm.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(*kwargs)
		context['x'] = 1*int(self.request.user.profile.bonus)
		context['user_for_money'] = 0.40*int(self.request.user.profile.bonus)
		context['balance'] = round(self.request.user.profile.balance, 1)
		return context

	def post(self, request):
		if 'farm' in request.POST:
			u = request.user.profile
			u.balance += 0.40 * int(u.bonus)
			u.save()
		return HttpResponseRedirect(reverse('farm:farm'))

def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('farm:index'))