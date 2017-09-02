from django.contrib import admin

# Register your models here.
from .models import Concern
from .models import SupportPersonnel
from .models import NotifyRelationship

class ConcernAdmin(admin.ModelAdmin):
	list_display = ('name', 'enabled', 'z_index', 'get_Parent_Name', 'has_child')
	fields = ('name', 'enabled', 'z_index', 'parent_id')
	ordering = ('id', 'z_index',)
	
class SupportPersonnelAdmin(admin.ModelAdmin):
	list_display = ('name', 'uid', 'phoneNo', 'email', 'isActive')
	ordering = ('name','-isActive',)
	
class NotifyRelationshipAdmin(admin.ModelAdmin):
	list_display = ('id', 'concern', 'supportPersonnel')
	fields = ('concern', 'supportPersonnel')
	ordering = ('id',)
	
admin.site.register(Concern, ConcernAdmin)
admin.site.register(SupportPersonnel, SupportPersonnelAdmin)
admin.site.register(NotifyRelationship, NotifyRelationshipAdmin)
