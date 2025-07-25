from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.utils import timezone
from rest_framework.authtoken.models import Token


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    RegistrationDate = models.DateTimeField(auto_now_add=True)

    last_login_date = models.DateTimeField(_("last login"), blank=True, null=True)
    
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    otp_max_tries = models.IntegerField(default=0)

    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_superuser = models.BooleanField(
        "Superuser status",
        default=False,
        help_text="Designates that this user has all permissions without explicitly assigning them.",
    )
    is_active = models.BooleanField(
        "active",
        default=False,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    
    # إضافة حقل groups بشكل صريح
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="custom_user_set",
        related_query_name="user",
    )

    # إضافة حقل user_permissions بشكل صريح
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="custom_user_set",
        related_query_name="user",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    @property
    def get_token(self):
        token, created = Token.objects.get_or_create(user=self)
        return token.key

    
    def generate_otp(self):
        import random
        self.otp = str(random.randint(100000, 999999))
        self.otp_expiry = timezone.now() + timedelta(minutes=5)  # OTP valid for 5 minutes
        self.otp_max_tries = 0
        self.save()

    def verify_otp(self, otp, remove_otp=False):
        if self.otp_max_tries > 3:
            return False, "Maximum OTP tries exceeded."
        
        if self.otp == otp and timezone.now() < self.otp_expiry:
            print('hiii')
            if remove_otp:
                self.otp = None
                self.otp_expiry = None
                self.otp_max_tries = 0
                self.save()
            return True, "OTP verified successfully."

        self.otp_max_tries += 1
        self.save()
        return False, "Invalid or expired OTP."

    def has_perm(self, perm, obj=None):
        """
        التحقق مما إذا كان المستخدم لديه صلاحية محددة
        """
        # المشرف لديه جميع الصلاحيات
        if self.is_superuser:
            return True
            
        if not self.is_active:
            return False
            
        # Check if user has this permission directly
        if self.user_permissions.filter(codename=perm.split('.')[-1]).exists():
            return True
            
        # Check if any of user's groups has this permission
        return self.groups.filter(permissions__codename=perm.split('.')[-1]).exists()

    def has_module_perms(self, app_label):
        """
        التحقق مما إذا كان المستخدم لديه صلاحيات على تطبيق معين
        """
        # المشرف لديه جميع الصلاحيات
        if self.is_superuser:
            return True
            
        if not self.is_active:
            return False
            
        # Check if user has any permissions in this app
        return self.user_permissions.filter(content_type__app_label=app_label).exists() or \
               self.groups.filter(permissions__content_type__app_label=app_label).exists()
    
