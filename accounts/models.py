from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,firstName,lastName,userName,email,password,phone):

        if not email:
            raise ValueError('User must have an email')
        if not userName:
            raise ValueError('Username must not be empty')
        if not phone:
            raise ValueError('Phone Number should not be empty')
        
        user = self.model(
            firstName=firstName,
            lastName = lastName,
            userName=userName,
            email=self.normalize_email(email),
            phone=phone
        )
        user.set_password(password)
        user.save(using =self._db)
        return user

    def create_superuser(self,firstName,lastName,userName,email,password,phone):
        user = self.create_user(
            firstName=firstName,
            lastName=lastName,
            userName=userName,
            email=email,
            phone=phone,
            password=password
        )
        user.is_admin = True
        user.is_superadmin = True
        user.is_staff = True
        user.is_active = True
        user.save(using =self._db)
        return user


class User(AbstractBaseUser):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    userName = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone = models.CharField(max_length=13)
    password = models.CharField(max_length=50)

    #required fields 
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login  = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['userName','firstName','lastName','phone']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True

