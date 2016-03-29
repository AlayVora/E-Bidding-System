from django.db import models
from django.conf import settings
from datetime import datetime, timedelta


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    card_no = models.CharField(max_length=16, null=True)
    exp_date = models.DateField(null=True)
    cvv = models.CharField(max_length=3, null=True)
    bids = models.PositiveSmallIntegerField(default=0)

class CATEGORY(models.Model):
    category_name = models.CharField(max_length=200)


class PRODUCT(models.Model):
    product_name = models.CharField(max_length=100)
    product_desc = models.CharField(max_length=200)
    price = models.IntegerField()
    product_path = models.CharField(max_length=200)
    category_id = models.ForeignKey(CATEGORY)
    owner = models.IntegerField()
    status = models.PositiveSmallIntegerField(default=1)  # 1 ==> product available, 0 ==> product sold
    expdatetime=models.DateTimeField(default=datetime.now()+timedelta(minutes=60))


class SOLD(models.Model):
    product_id = models.IntegerField()
    bid_value = models.IntegerField()
    old_owner = models.IntegerField()
    new_owner = models.IntegerField()

class BIDFORYOU(models.Model):
    product_id = models.IntegerField()
    bid_value = models.IntegerField()
    bidder_id = models.IntegerField()
    


class TRANSACT(models.Model):
    product = models.ForeignKey(PRODUCT)
    bidder_id = models.IntegerField()
    bid_value = models.IntegerField(default=1)



