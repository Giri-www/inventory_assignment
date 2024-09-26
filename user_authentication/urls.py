''' Login Authentication Views '''
from django.urls import path
from .views import   Login, CreateUser, VerifyUserToken

urlpatterns = [
    path('signin/', Login.as_view(), name='signin'),
    path('signup/', CreateUser.as_view(), name='signup'),
    path('tokenverify/', VerifyUserToken.as_view(), name='verify_token'),
   
]