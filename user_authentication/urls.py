''' Login Authentication Views '''
from django.urls import path
from .views import   Login, CreateUser, VerifyUserToken, UpdateUser

urlpatterns = [
    path('signin/', Login.as_view(), name='signin'),
    path('signup/', CreateUser.as_view(), name='signup'),
    path('update/<int:user_id>/', UpdateUser.as_view(),
         name='update_user'),
    # path('list/', UserListViews.as_view(), name='user_list'),
    path('tokenverify/', VerifyUserToken.as_view(), name='verify_token'),
   
]