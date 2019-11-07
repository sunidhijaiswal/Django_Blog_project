from django.urls import path
from . import views


urlpatterns = [
    path('profile/|urlencode', views.profile, name='profile'),
    path('setting/|urlencode', views.setting, name='setting'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('change_password', views.change_password, name="change_password"),
    path('change_picture', views.update_pic, name="change_picture"),
    path('delete_account', views.delete_account, name="delete_account"),
]