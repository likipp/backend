from django.db import models


class Basemodel(models.Model):
    name = models.CharField(default='', null=True, blank=True, max_length=128, verbose_name='名字')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    def __str__(self):
        return self.name
