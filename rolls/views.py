from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth import get_user_model, login, authenticate

from .models import Roll


User = get_user_model()


class HomeView(TemplateView):
    template_name = 'rolls/list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            ctx['rolls'] = Roll.objects.filter(user=self.request.user)

        return ctx


class RollListView(ListView):
    template_name = 'rolls/list.html'
    model = Roll

    def get_queryset(self, **kwargs):
        query_set = super().get_queryset(**kwargs)  # Roll.objects.all()

        user_id = self.kwargs.get('pk')

        query_set = query_set.filter(user_id=user_id)

        return query_set



class DetailView(TemplateView):
    template_name = 'rolls/detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        roll_id = self.kwargs['awesome']

        ctx['roll'] = Roll.objects.get(pk=roll_id)

        return ctx


# Create your views here.
class CreateView(TemplateView):
    template_name = 'rolls/create.html'

    def post(self, request, *args, **kwargs):
        title = self.request.POST.get('title')
        year_made = self.request.POST.get('year_made')

        roll = Roll()
        roll.title = title
        roll.year_made = year_made
        roll.user = self.request.user
        roll.save()

        return HttpResponseRedirect(reverse('rolls:index'))


# Create your views here.
class SignupView(TemplateView):
    template_name = 'registration/signup.html'

    def post(self, request, *args, **kwargs):
        # sign up user
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        password2 = self.request.POST.get('password2')

        # If the password fields don't match send the user back
        if password != password2:
            return HttpResponseRedirect(reverse('rolls:signup'))

        # If the username already exists, send the user back
        user = User.objects.filter(username=username)

        if user.count() > 0:
            return HttpResponseRedirect(reverse('rolls:signup'))

        # save user database record using fancy hashing on password
        User.objects.create_user(username=username, password=password)

        # Authenticate the user checks provided password against the hash
        user = authenticate(username=username, password=password)

        # Login the user (does the session table/cookie stuff)
        login(self.request, user)

        return HttpResponseRedirect(reverse('rolls:index'))
