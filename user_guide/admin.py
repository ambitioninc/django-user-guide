from django.conf import settings

from user_guide.models import Guide, GuideInfo

if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib import admin

    class GuideAdmin(admin.ModelAdmin):
        list_display = ('guide_name', 'guide_tag', 'guide_importance', 'creation_time')

    class GuideInfoAdmin(admin.ModelAdmin):
        list_display = ('user', 'guide_name', 'is_finished', 'finished_time')

        def guide_name(self, obj):
            return obj.guide.guide_name

    admin.site.register(Guide, GuideAdmin)
    admin.site.register(GuideInfo, GuideInfoAdmin)
