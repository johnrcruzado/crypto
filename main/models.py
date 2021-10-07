from django.conf import settings
from django.db import models
from django.utils import timezone
import os
from datetime import datetime

class Scholar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ronin_address = models.CharField(max_length=200)
    name =  models.CharField(max_length=200)
    manager_share = models.IntegerField(default=0)
    scholar_share = models.IntegerField(null=True,blank=True,default=0)
    updated_on = models.DateTimeField(null=True,blank=True)
    last_claim_amount = models.FloatField(default=0)
    last_claim_timestamp = models.DateTimeField(null=True)
    ronin_slp = models.IntegerField(default=0)
    total_slp  = models.IntegerField(default=0)
    in_game_slp = models.IntegerField(default=0)
    slp_success = models.BooleanField(blank=True, null=True)
    mmr = models.DateTimeField(blank=True, null=True)
    total_matches = models.IntegerField(default=0)
    ign = models.CharField(max_length=200)
    game_stats_success = models.BooleanField(blank=True, null=True)
    last_update = models.DateField(default=timezone.now)

    def get_days(self) -> object:
        print(self.last_claim_timestamp)
        last_date = datetime.strptime(self.last_claim_timestamp, '%Y-%m-%d %H:%M:%S')
        days = datetime.now() - last_date
        return days.days

    def get_average(self):
        days_ = self.get_days()
        if days_:
            averange = self.total_slp / days_
        else:
            averange = self.total_slp
        return round(averange)

    def get_manager_fee(self):
        manager_fee = self.total_slp * (self.manager_share / 100)
        return int(manager_fee) , self.manager_share

    def get_scholar_fee(self):
        scholar_fee = self.total_slp * (self.scholar_share / 100)
        return int(scholar_fee) , self.scholar_share

    def get_rate(self):
        crypto_obj = Crypto.objects.get(symbol="SLPUSDT")
        return crypto_obj.price


class Crypto(models.Model):
    symbol = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    last_update = models.DateField(default=timezone.now)


class Invoice(models.Model):
    scholar = models.ForeignKey(Scholar, on_delete=models.CASCADE)
    ronin_address = models.CharField(max_length=200)
    manager_fee = models.FloatField(default=0)
    scholar_fee = models.FloatField(null=True,blank=True,default=0)
    total_fee = models.FloatField(null=True,blank=True,default=0)
    manager_slp = models.FloatField(default=0)
    scholar_slp = models.FloatField(null=True, blank=True, default=0)
    total_slp = models.FloatField(null=True, blank=True, default=0)
    rate  = models.FloatField(default=0)
    gas_fee = models.FloatField(default=0)
    last_update = models.DateField(default=timezone.now)


class Rooster(models.Model):
    user = models.CharField(max_length=200,null=True,blank=True)
    info = models.CharField(max_length=200)
