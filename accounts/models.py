from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin

# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("user's must have an email address")
        if not username:
            raise ValueError("user's must have an username")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            )
        user.set_password(password)
        user.save(using=self._db)

        return user

    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True

        user.set_password(password)
        user.save(using=self._db)

        return user



class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin    

    def has_module_perms(self, app_label):
        return True


#address table
class Profile(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False, default='fname')
    lname = models.CharField(max_length=150, null=False, default='lname')
    phone = models.BigIntegerField(null=False, default='99999999')
    email = models.EmailField(max_length=150, null=False, default='example@gmail.com')
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    pincode = models.PositiveIntegerField(null=False, default=000000)
    country = models.CharField(max_length=150, null=False)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'Address'

    def __str__(self):
        return self.user.username
    
