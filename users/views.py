from django.shortcuts import render
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import User

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/profile_form.html'
    fields = ['first_name', 'last_name', 'bio', 'profile_picture', 'currency_preference']
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user
