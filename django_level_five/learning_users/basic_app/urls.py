from basic_app import views
from django.urls import path

#template tagging
app_name = 'basic_app'

urlpatterns = [
    path('registration/',views.register,name='registration'),
    path('user_login/',views.user_login,name='user_login'),
]