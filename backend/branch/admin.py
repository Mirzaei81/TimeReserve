from django.contrib import admin
from .models import Market,MarketImages,MarketOneTimeSlot,MarketFeature2,MarketFeature1,MarketManagers

admin.site.register(Market)
@admin.register(MarketOneTimeSlot)
class  MarketOneTimeSlotAdmin(admin.ModelAdmin):
	fields=("market1","day_of_week","start_time","end_time","cost_multiplier")
admin.site.register(MarketImages)
admin.site.register(MarketFeature2)
admin.site.register(MarketFeature1)
admin.site.register(MarketManagers)