from django.contrib import admin

from api.models import Department, EmployeeInfo, Admin
# Register your models here.


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('title', )


@admin.register(EmployeeInfo)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'age', 'gender', 'entry_time', 'depart')


@admin.register(Admin)
class Administrator(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username')

