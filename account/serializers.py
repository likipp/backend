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
        ret = super(UserSerializer, self).to_representation(instance)
        dep_instance = instance.dep
        ret['dep'] = {'id': dep_instance.id, 'name': dep_instance.name}
        return ret

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def update(self, instance, validated_data):
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
                  "groups", "nickname", "username", "password"]
