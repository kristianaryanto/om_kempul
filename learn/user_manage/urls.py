from django.urls import path,reverse
from .views import *

app_name = 'login'

urlpatterns = [
        path('signup/', signup, name='signup'),
        path('login/',signin, name='signin'),
        path('signout/', signout, name='signout'),
        path('profile/',profile,name='profile'),
        path('delete_user/',delete_user,name='delete_user'),
        path('create_org/',create_org,name='create_org')
]


