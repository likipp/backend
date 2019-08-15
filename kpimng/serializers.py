from rest_framework import serializers

from .models import KPI, GroupKPI, KpiInput


class KPISerializers(serializers.ModelSerializer):
    """
        KPI序列化
    """
    def to_representation(self, instance):
        ret = super(KPISerializers, self).to_representation(instance)
        status = instance.status
        status_name = instance.get_status_display()
        ret['status'] = {
            'id': status,
            'name': status_name
        }
        return ret

    class Meta:
        model = KPI
        fields = '__all__'


class GroupKPISerializers(serializers.ModelSerializer):
    """
        部门KPI序列化
    """
    def to_representation(self, instance):
        status = instance.status
        status_name = instance.get_status_display()
        dep_instance = instance.dep
        kpi_instance = instance.kpi
        ret = super(GroupKPISerializers, self).to_representation(instance)
        ret["status"] = {
            "id": status,
            "name": status_name
        }
        ret["dep"] = {
            "id": dep_instance.id,
            "name": dep_instance.name
        }
        ret["kpi"] = {
            "id": kpi_instance.id,
            "name": kpi_instance.name
        }
        return ret

    class Meta:
        model = GroupKPI
        fields = '__all__'


class KpiInputSerializers(serializers.ModelSerializer):

    def to_representation(self, instance):
        user = instance.user.id
        user_name = instance.user.nickname
        groupkpi = instance.groupkpi
        status = groupkpi.status
        ret = super(KpiInputSerializers, self).to_representation(instance)
        ret["status"] = {
            "id": status,
            "name": groupkpi.get_status_display()
        }
        ret["dep"] = {
            "id": groupkpi.dep.id,
            "name": groupkpi.dep.name
        }
        ret["kpi"] = {
            "id": groupkpi.kpi.id,
            "name": groupkpi.kpi.name
        }
        ret["user"] = {
            "id": user,
            "name": user_name
        }
        ret["t_value"] = groupkpi.t_value
        ret["l_limit"] = groupkpi.l_limit
        return ret

    class Meta:
        model = KpiInput
        fields = '__all__'
