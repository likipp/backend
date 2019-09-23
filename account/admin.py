from django.contrib import admin


from account.models import Departments, User

from guardian.admin import GuardedModelAdmin


class UserAdmin(GuardedModelAdmin):
    list_display = ('username', 'nickname', 'dep', 'is_staff')
    search_fields = ('username',)
    filter_horizontal = ('user_permissions', 'groups',)


class DepartmentsAdmin(GuardedModelAdmin):
    list_display = ('name', 'type',)


admin.site.register(Departments, DepartmentsAdmin)
admin.site.register(User, UserAdmin)
