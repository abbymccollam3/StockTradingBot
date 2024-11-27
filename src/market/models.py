from django.db import models

from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager

from . import tasks

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=120)
    ticker = models.CharField(max_length=20, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True) 
    active = models.BooleanField(default=True) 
    timestamp = models.DateTimeField(auto_now_add=True)
    updates = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.ticker = f"{self.ticker}".upper()
        super().save(*args, **kwargs)
        tasks.sync_company_stock_quotes.delay(self.pk)

# defining database 

# stock market tickers can change

class StockQuote(models.Model):

    """
    'open_price': result['o'],
    'close_price': result['c'],
    'high_price': result['h'],
    'low_price': result['l'],
    'number_of_trades': result['n'],
    'volume': result['v'],
    'volume_weighted_average': result['vw'],
    'time': utc_timestamp,
    """

    company = models.ForeignKey(
        Company,
        on_delete = models.CASCADE, # what do we do when a company is deleted
        related_name="stock_quotes"
    )
    open_price = models.DecimalField(max_digits=10, decimal_places=4)
    close_price = models.DecimalField(max_digits=10, decimal_places=4)
    high_price = models.DecimalField(max_digits=10, decimal_places=4)
    low_price = models.DecimalField(max_digits=10, decimal_places=4)
    number_of_trades = models.BigIntegerField(blank=True, null=True)
    volume = models.BigIntegerField()
    volume_weighted_average = models.DecimalField(max_digits=10, decimal_places=4)
    raw_timestamp = models.CharField(max_length = 120, null = True, blank = True)
    time = TimescaleDateTimeField(interval="1 week")

    objects = models.Manager()
    timescale = TimescaleManager()

    # makes sure objects are unique
    class Meta:
        unique_together = [('company', 'time')]
