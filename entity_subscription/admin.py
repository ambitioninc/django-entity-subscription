from django.contrib import admin

from entity_subscription.models import Medium, Source, Subscription


class MediumAdmin(admin.ModelAdmin):
    pass


class SourceAdmin(admin.ModelAdmin):
    pass


class SubscriptionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Medium, MediumAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
