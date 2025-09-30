from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from .models import User

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

            return Response({
                'message': 'Login realizado com sucesso!',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
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

class UserProfileView(APIView):
    """View para visualizar e editar o perfil do usuário."""
    permission_classes = [IsAuthenticated] # Apenas usuários logados podem acessar
    
    def get(self, request):
        """Retorna os dados do perfil do usuário logado."""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(csrf_exempt)
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

# View adicional para verificar se o usuário está logado
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