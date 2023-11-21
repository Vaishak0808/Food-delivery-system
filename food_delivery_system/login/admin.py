from django.contrib import admin
from login.models import Role,UserDetails


class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Role,RoleAdmin)

class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ['id','user','get_first_name']
    def get_first_name(self,obj):
        return obj.user.first_name +' '+ obj.user.last_name
admin.site.register(UserDetails,UserDetailsAdmin)