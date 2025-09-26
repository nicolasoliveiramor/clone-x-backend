from pickle import TRUE
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('O email é obrigatório'))
        if not username:
            raise ValueError(_('O nome de usuário é obrigatório'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser precisa ter is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser precisa ter is_superuser=True.'))
        
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(_('endereço de email'), unique=True)
    username = models.CharField(_('nome de usuário'), max_length=30, unique=True)
    first_name = models.CharField(_('nome'), max_length=30)
    last_name = models.CharField(_('sobrenome'), max_length=30)
    profile_picture = models.ImageField(_('foto de perfil'), upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(_('biografia'), max_length=500, blank=True)
    date_joined = models.DateTimeField(_('data de registro'), auto_now_add=True)
    is_active = models.BooleanField(_('ativo'), default=True)
    is_staff = models.BooleanField(_('equipe'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('usuário')
        verbose_name_plural = _('usuários')

    def __str__(self):
        return self.username