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
        default_permissions = ()
        permissions = (
            ('add_departments', '添加部门'),
            ('change_departments', '修改部门'),
            ('delete_departments', '删除部门'),
            ('view_departments', '查看部门')
        )

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
    avatar = models.ImageField(default='avatar/default.jpg', upload_to='avatar/%Y%m%d/')

    class Meta:
        verbose_name_plural = verbose_name = '用户'
        ordering = ["id", 'username']
        # 设置default_permissions列表为空时,在makemigrations操作时,不会创建('add', 'change', 'delete', 'view')英文名称
        default_permissions = ()
        permissions = (
            ('add_user', '新增用户'),
            ('change_user', '修改用户'),
            ('delete_user', '删除用户'),
            ('view_user', '查看用户')
        )

    def __str__(self):
        return self.username


# class Permission(models.Model):
#     class Meta:
#         permissions = (
#             ('add_user', '新增用户'),
#             ('change_user', '修改用户'),
#             ('delete_user', '删除用户'),
#             ('view_user', '查看用户'),
#             ('add_departments', '添加部门'),
#             ('change_departments', '修改部门'),
#             ('delete_departments', '删除部门'),
#             ('view_departments', '查看部门')
#         )
