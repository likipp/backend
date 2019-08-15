from django_filters import rest_framework as filters

from .models import Departments, User


class DepartmentsFilter(filters.FilterSet):
    """
    Departments搜索类
    """
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Departments
        fields = ['name']


class UserFilter(filters.FilterSet):
    """
    用户搜索类
    """
    username = filters.CharFilter(lookup_expr="icontains", field_name="username")
    nickname = filters.CharFilter(lookup_expr="icontains", field_name="nickname")
    dep = filters.ModelChoiceFilter(queryset=Departments.objects.all())

    class Meta:
        model = User
        fields = ['username', 'nickname', 'dep']
