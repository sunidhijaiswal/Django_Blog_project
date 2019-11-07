from django import forms
from .models import Post, Comment, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    # profile = forms.ImageField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        print(User.objects.filter(email=email).count())
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(u'This email address is already registered.')
        return email

    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        # fields = ('name', 'email', 'contact', 'dob', 'gender', 'pic')