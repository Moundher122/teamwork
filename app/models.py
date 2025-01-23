from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
# Create your models here.
class file(models.Model):
    name=models.CharField(max_length=100)
    file=models.FileField(upload_to='files/')
    date=models.DateField(auto_now_add=True)
    admin=models.ForeignKey("User", verbose_name=("admins"), on_delete=models.DO_NOTHING,null=True)

    def __str__(self):
        return self.name
    

class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    files=models.ManyToManyField("file",verbose_name=("files"),null=1)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = MyAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):      
        return self.email
    class Meta:
        permissiom:{
            ('can_view','Can view '),
            ('can_change','Can change'),
        }
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
