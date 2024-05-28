from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': '请输入用户名...'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': '输入密码...需要复杂一点'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': '请确认密码...'})
