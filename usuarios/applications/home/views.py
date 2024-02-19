from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class IndexHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/index.html'
    login_url = reverse_lazy('users_app:login')
