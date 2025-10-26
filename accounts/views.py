from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django import forms
from .models import User


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'address']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Đăng ký thành công! Chào mừng bạn đến với Cửa Hàng Trái Cây.')
        return redirect(self.success_url)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/profile.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'address']
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        """Lấy đối tượng user hiện tại"""
        return self.request.user
    
    def get_form(self, form_class=None):
        """Thêm Bootstrap classes cho form fields"""
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            field.widget.attrs['class'] = 'form-control'
        return form
    
    def get_context_data(self, **kwargs):
        """Thêm thống kê đơn hàng vào context"""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['completed_orders'] = user.orders.filter(status='completed').count()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Cập nhật hồ sơ thành công!')
        return super().form_valid(form)
