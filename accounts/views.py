from rest_framework import generics, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from rest_framework import generics
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserSerializer, ChangePasswordSerializer
from .models import User, Follow
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    """View para registro de novos usuários."""
    permission_classes = [AllowAny] # Qualquer pessoa pode se registrar

    def post(self, request):
        """Registra um novo usuário."""
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Usuário criado com sucesso!',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """View para login de usuários."""
    permission_classes = [AllowAny] # Qualquer pessoa pode tentar fazer login

    def post(self, request):
        """Autentica um usuário."""
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user) # Cria a sessão do usuário

            # Retorna perfil completo (inclui profile_picture, bio, contadores, etc.)
            from .serializers import UserProfileSerializer
            profile = UserProfileSerializer(user).data

            return Response({
                'message': 'Login realizado com sucesso!',
                'user': profile
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    """View para logout de usuários."""
    permission_classes = [IsAuthenticated] # Apenas usuários logados podem fazer logout

    def post(self, request):
        """Desloga o usuário."""
        logout(request) # Encerra a sessão do usuário
        return Response({
            'message': 'Logout realizado com sucesso!'
        }, status=status.HTTP_200_OK)

@method_decorator(ensure_csrf_cookie, name='get')
class CsrfTokenView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = get_token(request)
        return Response({'csrfToken': token}, status=status.HTTP_200_OK)

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'user_id'

@method_decorator(ensure_csrf_cookie, name='get')
class UserProfileView(APIView):
    """View para visualizar e editar o perfil do usuário."""
    permission_classes = [IsAuthenticated]
    # Aceita JSON, form-urlencoded e multipart (upload)
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        """Retorna os dados do perfil do usuário logado."""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Atualiza os dados do perfil do usuário logado."""
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True, # Permite atualizações parciais
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Perfil atualizado com sucesso!',
                'user': serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Perfil atualizado com sucesso!',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View adicional para verificar se o usuário está logado
# Garante emitir cookie CSRF em GET de check-auth
@method_decorator(ensure_csrf_cookie, name='get')
class CheckAuthView(APIView):
    """View para verificar se o usuário está autenticado."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retorna informações do usuário se estiver logado."""
        serializer = UserProfileSerializer(request.user)
        return Response({
            'authenticated': True,
            'user': serializer.data, 
        }, status=status.HTTP_200_OK)

class FollowToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, id=user_id)
        if target == request.user:
            return Response({'detail': 'Você não pode seguir a si mesmo.'}, status=status.HTTP_400_BAD_REQUEST)
        obj, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if created:
            return Response({'detail': 'Agora você está seguindo este usuário.'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Você já segue este usuário.'}, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        target = get_object_or_404(User, id=user_id)
        deleted, _ = Follow.objects.filter(follower=request.user, following=target).delete()
        if deleted:
            return Response({'detail': 'Você deixou de seguir este usuário.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Você não seguia este usuário.'}, status=status.HTTP_404_NOT_FOUND)

class FollowersListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return User.objects.filter(following__following_id=user_id).order_by('-date_joined')

class FollowingListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return User.objects.filter(followers__follower_id=user_id).order_by('-date_joined')

class UsersListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['date_joined']

    def get_queryset(self):
        qs = User.objects.all().order_by('-date_joined')
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated:
            qs = qs.exclude(id=user.id)
        return qs

class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            update_session_auth_hash(request, user)
            return Response({'detail': 'Senha alterada com sucesso.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)