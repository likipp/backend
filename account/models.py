from django.db import models
from django.contrib.auth.models import AbstractUser


class Departments(models.Model):
    TYPES = (
        ('group', '集团公司'),
        ('sale', '销售片区'),
    )
    name = models.CharField("部门名称", max_length=32)
    type = models.CharField(max_length=32, default='sale', verbose_name='类型', choices=TYPES)

    class Meta:
        verbose_name_plural = verbose_name = '部门'
        ordering = ["id", "name"]

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLES = (
        ('administrator', '管理员'),
        ('user', '普通用户'),
    )
    role = models.CharField(max_length=32, default='user', choices=ROLES, verbose_name='角色')
    nickname = models.CharField(max_length=30, blank=True, null=True, verbose_name='姓名')
    dep = models.ForeignKey(Departments, on_delete=models.CASCADE,
                            verbose_name='所属部门', null=True, blank=True, related_name='deps')

    class Meta:
        verbose_name_plural = verbose_name = '用户'
        ordering = ["id", 'username']

    def __str__(self):
        return self.username
