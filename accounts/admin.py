from django.contrib import admin
from . models import MyUser
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _




class MyUserTypeFilter(SimpleListFilter):
    title=_('user type')
    parameter_name='user_type'
    
    def lookups(self, request, model_admin):
        return (
            ('patient',_('patient')),
            ('doctor',_('doctor')),
            ('admin',_('admin')),
        )
    
    
    def queryset(self, request, queryset):
        if self.value()=='patient':
            return queryset.filter(user_type='patient')
        if self.value()=='doctor':
            return queryset.filter(user_type='doctor')
        if self.value()=='admin':
            return queryset.filter(user_type='admin')
        return queryset
    
    
    
    
    
    
class MyuserAdmin(admin.ModelAdmin):
    fields=('full_name', 'user_type','date_joined')
    list_filter=(MyUserTypeFilter,)
    search_fields=('full_name',)
    
    
    
admin.site.register(MyUser,MyuserAdmin)