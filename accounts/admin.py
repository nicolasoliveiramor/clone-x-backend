from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Configuração personalizada do admin para o modelo User."""

    # Campos exibidos na lista de usuários
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'profile_picture_preview')

    # Campos pelos quais é possível filtrar
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')

    # Campos pelos quais é possível pesquisar
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Ordenação padrão
    ordering = ('-date_joined',)

    # Campos somente leitura
    readonly_fields = ('date_joined', 'last_login', 'profile_picture_preview')

    # Configuração dos fieldsets (organização dos campos no formulário)
    fieldsets = (
        # Informações básicas
        ('Informações Pessoais', {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),

        # Foto de perfil e bio
        ('Foto de Perfil e Bio', {
            'fields': ('profile_picture', 'profile_picture_preview', 'bio'),
            'classes': ('collapse',) #Seção colapsável
        }),

        # Permissões
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),

        # Datas importantes
        ('Datas Importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    # Configuração para criação de novos usuários
    add_fieldsets = (
        ('Criar Novo Usuário', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    def profile_picture_preview(self, obj):
        """Exibe uma prévia da foto de perfil no admin."""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.profile_picture.url
            )
        return 'Sem foto'

    profile_picture_preview.short_description = 'Foto de Perfil'




