from django.shortcuts import render
from django.views.generic import FormView, View, UpdateView, ListView, DeleteView, DetailView, TemplateView
from .models import User
from .functions import create_code
from .forms import CreateUserForm,LoginUserForm,UpdateUserForm, VerificationUserForm,UpdatePasswordForm 
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
# Create your views here.



class CreateUserView(FormView):
    model = User
    template_name = "users/create_user.html"
    form_class = CreateUserForm
    success_url = reverse_lazy('home_app:login')


    def form_valid(self, form):
        codigo = create_code()
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            genero = form.cleaned_data['genero'],
            foto = form.cleaned_data['foto'],
            codregistro = codigo
        )
        
        #envio de email
        asunto = 'Confirmacion de registro'
        mensaje = 'Tu codigo de verificacion es '+ codigo        
        remitente = 'jacto2024@gmail.com'        
        
        send_mail(asunto, mensaje, remitente, [form.cleaned_data['email'],])
                       
        return HttpResponseRedirect(
            reverse(
                'users_app:verificacion',
                kwargs={'pk':usuario.id}
            )
        )




class LoginUserView(FormView):
    model = User
    form_class = LoginUserForm
    template_name = 'users/login_user.html'
    success_url = reverse_lazy('home_app:home')

    
    def form_valid(self, form):
        
        user = authenticate(
        username = form.cleaned_data['username'],
        password = form.cleaned_data['password']
        )
        login(self.request, user)
        
        return super(LoginUserView, self).form_valid(form)



class LogoutUser(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        
        return HttpResponseRedirect(
            reverse(
                'users_app:login'
                )
        )
           
class ActiveUser(FormView):
    #model = User
    template_name = 'users/active-user.html'
    form_class = VerificationUserForm
    success_url = reverse_lazy('users_app:login')
    
    def get_form_kwargs(self):
        kwargs = super(ActiveUser, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk']
        })
        return kwargs
    
    def form_valid(self, form):
        
        User.objects.filter(
            id = self.kwargs['pk']
        ).update(is_active=True)
        
        return super(ActiveUser, self).form_valid(form)



class UpdatePasswordView(FormView):
    template_name = 'users/update-password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:login')
    login_url = reverse_lazy('users_app:login')
    
    
    def form_valid(self, form):
        
        usuario = self.request.user
        
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data['password1']
        )
        if user:
            new_password = form.cleaned_data['password2']
            user.set_password(new_password)
            user.save()
        
        logout(self.request)        
        
        return super(UpdatePasswordView, self).form_valid(form)



class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/update-user.html'
    form_class = UpdateUserForm
    success_url = reverse_lazy('home_app:home')
    login_url = reverse_lazy('users_app:login')



class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/allusers.html'
    context_object_name = 'allusers'
    login_url = reverse_lazy('users_app:login')
    ordering = 'id'
    paginate_by = 5



class UserAdminUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/update-admin-user.html'
    context_object_name = 'usuario'
    success_url = reverse_lazy('users_app:users_all')
    login_url = reverse_lazy('users_app:login')
    fields = (            
            'nombres',
            'apellidos',
            'genero',
            'email',            
        )
    
    

class UserAdminDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    context_object_name = 'usuario'
    template_name = 'users/delete-user.html'
    success_url = reverse_lazy('users_app:users_all')
    login_url = reverse_lazy('users_app:login')


class UserAdminDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/detail-user.html'
    context_object_name = 'usuario'
    login_url = reverse_lazy('users_app:login')
    
  

class UserDetailView(LoginRequiredMixin, DeleteView):    
    template_name = 'users/user-info.html'
    context_object_name = 'usuario'
    login_url = reverse_lazy('users_app:login')
    
    
    def get_queryset(self):
        
        dato = self.kwargs['pk']
        resultado = User.objects.filter(
            id = dato
        )
        return resultado
    
        
    