from django.contrib import admin
from .models import Person,Meeting,TownHall,StudentDay,Panel,Location
from .models import OrgsList,MemberAtLarge,PanelMember,HTMLBlock
from .models import Award, Resource, ResourcePage

admin.site.site_header = 'CONNECT Database'

class PanelMemberInline(admin.TabularInline):
    model = PanelMember
    extra = 1

class PanelAdmin(admin.ModelAdmin):
    list_display=('title','description',)
    inlines = (PanelMemberInline,)

# Register your models here.
admin.site.register(Award)
admin.site.register(Person)
admin.site.register(Meeting)
admin.site.register(TownHall)
admin.site.register(StudentDay)
admin.site.register(Location)
admin.site.register(OrgsList)
admin.site.register(MemberAtLarge)
admin.site.register(Panel,PanelAdmin)
admin.site.register(HTMLBlock)
admin.site.register(Resource)
admin.site.register(ResourcePage)

