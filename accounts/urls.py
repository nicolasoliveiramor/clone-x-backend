from django.urls import path
from .views import RegisterView, LoginView, LogoutView, CheckAuthView, UserProfileView, FollowToggleView, FollowersListView, FollowingListView, UsersListView

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

    # Rota para seguir/parar de seguir um usuário
    path('follow/<int:user_id>/', FollowToggleView.as_view(), name='follow-toggle'),

    # Rota para listar os seguidores de um usuário
    path('<int:user_id>/followers/', FollowersListView.as_view(), name='followers-list'),

    # Rota para listar os usuários que um usuário está seguindo
    path('<int:user_id>/following/', FollowingListView.as_view(), name='following-list'),
    path('users/', UsersListView.as_view(), name='users-list'),
]