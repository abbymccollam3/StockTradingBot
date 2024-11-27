import zoneinfo
from django.contrib import admin

# Register your models here.
from .models import StockQuote, Company

admin.site.register(Company)

# this adds data to Django and allows you to see the stock quotes that are currently available
class StockQuoteAdmin(admin.ModelAdmin):
    list_display=['company__ticker', 'close_price', 'localized_time']
    list_filter = ['company__ticker', 'time']

    def localized_time(self, obj):
        tz_name = "US/Eastern"
        user_tz = zoneinfo.ZoneInfo(tz_name)
        local_time = obj.time.astimezone(user_tz)
        return local_time.strftime("%b %d, %Y, %I:%M %p (%Z)")

    # class Meta:
    #     model = StockQuote

admin.site.register(StockQuote, StockQuoteAdmin)