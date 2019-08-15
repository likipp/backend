from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework import viewsets, mixins
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, AuthenticationFailed
# from django_filters import rest_framework as filters

from .models import Departments, User
from .serializers import DepartmentsSerializer, UserSerializer
from .filters import DepartmentsFilter, UserFilter
from rest_framework.permissions import IsAuthenticated
# from django_filters.rest_framework import DjangoFilterBackend


class DepartmentsViewset(viewsets.ModelViewSet):
    """
    retrieve:
            返回指定部门信息
    list:
            返回部门列表
    update:
            更新部门信息
    destroy:
            删除部门记录
    create:
            创建部门记录
    partial_update:
            更新记录部分字段
    """
    queryset = Departments.objects.all().order_by("id")
    serializer_class = DepartmentsSerializer
    # filter_fields = ("name",)
    filterset_class = DepartmentsFilter
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    # permission_classes = (IsAuthenticated,)


class UserViewset(viewsets.ModelViewSet):
    """
        retrieve:
                返回指定用户信息
        list:
                返回用户列表
        update:
                更新用户信息
        destroy:
                删除用户记录
        create:
                创建用户记录
        partial_update:
                更新记录部分字段
    """
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter
    # filter_fields = ("name",)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    """
        设置dep__name取到User ForeignKey Departments的名字，并且在filters文件中定义好ModelChoiceFilter
    """
    search_fields = ['username', 'nickname', 'dep__name']


