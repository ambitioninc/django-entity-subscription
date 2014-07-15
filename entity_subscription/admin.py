from django.contrib import admin

from entity_subscription.models import Medium, Source, Subscription, Unsubscribe


class MediumAdmin(admin.ModelAdmin):
    pass


class SourceAdmin(admin.ModelAdmin):
    pass


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('entity', 'source', 'medium')


class UnsubscribeAdmin(admin.ModelAdmin):
    list_display = ('entity', 'source', 'medium')


admin.site.register(Medium, MediumAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Unsubscribe, UnsubscribeAdmin)
