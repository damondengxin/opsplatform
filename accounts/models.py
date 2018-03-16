
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.


class RoleList(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class PermissionList(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=255)
    role = models.ForeignKey(RoleList,  on_delete=True)

    def __str__(self):
        return '%s(%s)' % (self.name, self.url)


class UserManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password,**extra_fields):
        user = self.create_user(email,
            username=username,
            password=password,
            **extra_fields
        )

        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserInfo(AbstractBaseUser):
    username = models.CharField("用户名", max_length=40, unique=True, db_index=True)
    email = models.EmailField("邮箱", max_length=255)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    nickname = models.CharField("姓名", max_length=64, null=True,)
    role = models.ManyToManyField(RoleList, verbose_name="角色", blank=True)
    department = models.CharField("部门", max_length=80, null=True, blank=True)
    position = models.CharField("职位", max_length=80, null=True, blank=True)
    reg_time = models.DateTimeField('注册时间', auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser