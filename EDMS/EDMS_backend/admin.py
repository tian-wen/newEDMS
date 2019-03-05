from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserFav, MyUser, BasicInfo


class BasicInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'theme_list']

# Register your models here.
class MyUserInline(admin.StackedInline):
    model = MyUser
    can_delete = False
    verbose_name = "自定义用户"


class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInline,)


class UserFavAdmin(admin.ModelAdmin):
    list_display = ['user', 'expert_id']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserFav, UserFavAdmin)
admin.site.register(BasicInfo, BasicInfoAdmin)
