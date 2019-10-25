from collections import OrderedDict

from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from .models import Departments, User

from kpimng.models import GroupKPI, KPI


class DepartmentsSerializer(serializers.ModelSerializer):
    """
    部门序列化
    """
    def to_representation(self, instance):
        ret = super(DepartmentsSerializer, self).to_representation(instance)
        type = instance.type
        type_name = instance.get_type_display()
        member_set = instance.deps.all()
        member = [{'id': user.id, 'username': user.username, 'nickname': user.nickname} for user in member_set]
        kpi_set = GroupKPI.objects.filter(dep=instance).all()
        # 返回部门已经有了的KPI列表与还未分配的KPI列表.方便前端穿梭框过滤掉已经分配了的KPI
        have_kpi = [{'id': kpi.kpi.id, 'name': kpi.kpi.name} for kpi in kpi_set]
        # 使用__in方法调用列表中的条件实现批量过滤,对象必须是一个列表
        prep_kpi = [{'id': index.id, 'name': index.name} for index in KPI.objects.exclude(
            name__in=[a.kpi.name for a in kpi_set]).all()]
        ret['prep_kpi'] = prep_kpi
        ret['have_kpi'] = have_kpi
        ret['member'] = member
        ret['type'] = {
            'id': type,
            'name': type_name
        }
        if instance.parent:
            ret['parent'] = {
                'id': instance.parent.id,
                'name': instance.parent.name
            }
        else:
            ret['parent'] = ''
        return ret

    class Meta:
        model = Departments
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化
    """

    def to_representation(self, instance):
        # 返回的是当前登录用户名
        # print(self.context['request'].user, 6)
        groups = []
        user_permissions = []
        ret = super(UserSerializer, self).to_representation(instance)
        dep_instance = instance.dep
        groups_instance = instance.groups.all()
        permissions_instance = instance.user_permissions.all()
        if groups_instance:
            for group in groups_instance:
                groups.append({"id": group.id, "name": group.name})
            ret["groups"] = groups
        else:
            ret['groups'] = {}
        if permissions_instance:
            for permission in permissions_instance:
                user_permissions.append({"id": permission.id, "name": permission.name})
            ret['user_permissions'] = user_permissions
        else:
            ret['user_permissions'] = {}
        # ret["permissions"] = instance.user_permissions.all()
        if instance == 'AnonymousUser' or dep_instance is None:
            ret['dep'] = {}
        else:
            ret['dep'] = {'id': dep_instance.id, 'name': dep_instance.name}
        return ret

    # def check_permission(self, validated_data):
    #     print(self.context['request'].user.is_superuser, 8)
    #     print(validated_data, 7)
    #     return 11111

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def update(self, instance, validated_data):
        print(instance, instance.password)
        if instance.password == validated_data['password']:
            validated_data.pop('password')
        else:
            instance.set_password(validated_data['password'])
        return super(UserSerializer, self).update(instance, validated_data)

    class Meta:
        model = User
        # 带出所有model字段
        # fields = "__all__"
        # 带出除了user_permissions以外的所有字段
        # exclude = ['user_permissions', 'email']
        fields = ["id", "is_superuser", "is_staff", "is_active", "role", "dep",
                  "groups", "nickname", "username", "password", "user_permissions", "avatar"]


class GroupSerializer(serializers.ModelSerializer):
    """
    组序列化
    """
    class Meta:
        model = Group
        exclude = ['permissions']

    def to_representation(self, instance):
        group_permissions = []
        ret = super(GroupSerializer, self).to_representation(instance)
        if not isinstance(instance, OrderedDict):
            member_set = instance.user_set.all()
            permissions_instance = instance.permissions.all()
            members = [{'id': user.id, 'name': user.username, 'nickname': user.nickname}
                       for user in member_set]
            ret['members'] = members
            for permission in permissions_instance:
                group_permissions.append({'id': permission.id, 'name': permission.name})
            ret['group_permissions'] = group_permissions
        return ret

    def update(self, instance, validated_data):
        pass


class PersonalCenterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password']
