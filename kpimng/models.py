from django.db import models
from django.utils import timezone

from account.models import Departments,User


class KPI(models.Model):
    STATUS = {
        ('using', '使用中'),
        ('unused', '未使用')
    }
    name = models.CharField('名称', max_length=100)
    unit = models.CharField('单位', max_length=32)
    in_time = models.CharField('录入时间', max_length=32)
    mo_time = models.CharField('修改时间', max_length=32)
    status = models.CharField('状态', max_length=32, default='unused', choices=STATUS)

    class Meta:
        verbose_name_plural = verbose_name = "KPI"
        ordering = ["id", "name"]

    def __str__(self):
        return self.name


class GroupKPI(models.Model):
    STATUS = {
        ('using', '使用中'),
        ('unused', '未使用')
    }
    dep = models.ForeignKey(Departments, on_delete=models.CASCADE,
                            verbose_name='所属部门', null=True, blank=True, related_name='group_dep')
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, verbose_name='KPI', related_name='group_kpi')
    u_limit = models.FloatField('上限值', max_length=10)
    l_limit = models.FloatField('下限值', max_length=10)
    t_value = models.FloatField('目标值', max_length=10)
    status = models.CharField('状态', max_length=32, default='unused', choices=STATUS)

    class Meta:
        verbose_name_plural = verbose_name = "部门KPI"
        ordering = ["id", "dep"]

    def __str__(self):
        return '{}_{}'.format(self.dep, self.kpi)


class KpiInput(models.Model):
    r_value = models.FloatField('实际值', max_length=10)
    month = models.DateField('月份')
    add_time = models.DateTimeField('录入时间', auto_now_add=True)
    update_time = models.DateTimeField('最后修改时间', auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='录入人',
                             null=True, blank=True, related_name='input_user')
    groupkpi = models.ForeignKey(GroupKPI, on_delete=models.CASCADE, verbose_name='部门KPI',
                                 null=True, blank=True, related_name='input_group')

    class Meta:
        verbose_name_plural = verbose_name = "KPI数据输入"
        ordering = ["id"]
