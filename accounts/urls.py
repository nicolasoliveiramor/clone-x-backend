from django.urls import path
from .views import RegisterView, LoginView, LogoutView, CheckAuthView, UserProfileView

app_name = 'accounts'

urlpatterns = [
    # Rota para o registro de usuários
    path('register/', RegisterView.as_view(), name='register'),

    # Rota para login
    path('login/', LoginView.as_view(), name='login'),

    # Rota para logout
    path('logout/', LogoutView.as_view(), name='logout'),

    # Rota para perfil do usuário (GET para visualizar, PUT para editar)
    path('profile/', UserProfileView.as_view(), name='profile'),

    # Rota para verificar se o usuário está autenticado
    path('check-auth/', CheckAuthView.as_view(), name='check_auth'),
]