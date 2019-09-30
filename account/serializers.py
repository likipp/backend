from collections import OrderedDict

from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from .models import Departments, User


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
        ret['member'] = member
        ret['type'] = {
            'id': type,
            'name': type_name
        }
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
        print(validated_data, 8777, instance)
        instance.set_password(validated_data['password'])
        validated_data.pop('password')
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
        ret = super(GroupSerializer, self).to_representation(instance)
        if not isinstance(instance, OrderedDict):
            member_set = instance.user_set.all()
            members = [{'id': user.id, 'name': user.username, 'nickname': user.nickname}
                       for user in member_set]
            ret['members'] = members
        return ret

    def update(self, instance, validated_data):
        pass
