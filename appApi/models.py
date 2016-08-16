# coding:utf-8
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desidered behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
import hashlib

from django.db import models


from django.utils.crypto import salted_hmac


class Community(models.Model):

    community_status = (
        ('A', '有效'),
        ('D', '已删除')
    )

    name = models.CharField(max_length=64)
    province = models.CharField(max_length=16)
    city = models.CharField(max_length=16)
    area = models.CharField(max_length=16)
    address = models.CharField(max_length=256)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=4, choices=community_status)

    class Meta:
        db_table = 'community'


class User(models.Model):
    name = models.CharField(max_length=64)
    nickname = models.CharField(max_length=64)
    pswd = models.CharField(max_length=32)
    community = models.ForeignKey(Community, blank=True, null=True, on_delete=None)
    email = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    sex = models.IntegerField()
    signature = models.CharField(max_length=128)
    create_time = models.DateTimeField(auto_now_add=True)
    addfrom = models.CharField(max_length=16)
    last_login_time = models.DateTimeField()
    status = models.CharField(max_length=4)
    faceimg_s = models.CharField(max_length=64)

    def is_authenticated(self):
        return True

    def hashed_password(self, password=None):
        if not password:
            return self.pswd
        else:
            salt = "srx_"+ password
            return hashlib.md5(salt).hexdigest().upper()

    def check_password(self, password):
        if self.hashed_password(password) == self.pswd:
            return True
        return False

    def get_session_auth_hash(self):
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.pswd).hexdigest()

    class Meta:
        db_table = 'user'


class Smsmessage(models.Model):
    phone = models.CharField(max_length=16)
    content = models.CharField(max_length=256)
    source = models.CharField(max_length=32, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=4)

    class Meta:
        db_table = 'smsmessage'

class Config(models.Model):
    android_version = models.CharField(max_length=128)
    android_url = models.CharField(max_length=128)
    android_notes = models.CharField(max_length=128)
    android_radio = models.IntegerField()

    class Meta:
        db_table = 'config'


class Category(models.Model):
    name = models.CharField(max_length=32)
    sname = models.CharField(max_length=64, null=True, blank=True)
    logo = models.CharField(max_length=64, null=True, blank=True)
    rank = models.IntegerField(default=1)
    status = models.CharField(max_length=2, default='A')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'category'


class Good(models.Model):
    cate = models.ForeignKey(Category, on_delete=None)
    community = models.ForeignKey(Community, on_delete=None)
    name = models.CharField(max_length=16)
    sname = models.CharField(max_length=64, null=True, blank=True)
    des = models.TextField(null=True, blank=True)
    logo = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    sale_price = models.DecimalField(max_digits=9, decimal_places=2)
    spec = models.CharField(max_length=128, verbose_name=u'规格JSON', null=True, blank=True)
    rank = models.IntegerField(default=1)
    status = models.CharField(max_length=2, default='A')
    create_time = models.DateTimeField(auto_now_add=True)
    inventory = models.IntegerField(verbose_name=u'库存数')

    class Meta:
        db_table = 'goods'


class CartItem(models.Model):

    cart_item_status = (
        ('A', '有效'),
        ('D', '已删除'),
        ('E', '已过期'),
    )
    user = models.ForeignKey(User, on_delete=None, related_name='cart')
    good = models.ForeignKey(Good, on_delete=None)
    num = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    change_time = models.DateTimeField(null=True, blank=True)
    join_price = models.DecimalField()
    status = models.CharField(max_length=2, default='A', choices=cart_item_status)

    class Meta:
        db_table = 'cart'


class Order(models.Model):
    logic_id = models.CharField(max_length=32)
    title = models.CharField(max_length=128)
    orderprice = models.DecimalField(max_digits=9, decimal_places=2)
    payprice = models.DecimalField(max_digits=9, decimal_places=2)
    kindcount = models.IntegerField()
    count = models.IntegerField()
    community = models.ForeignKey(Community, on_delete=None)
    sellernote = models.CharField(max_length=256)
    adddateline = models.IntegerField()
    orderstatus = models.IntegerField()
    paystatus = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=None)
    buyer = models.ForeignKey(User, on_delete=None)
    buyernote = models.CharField(max_length=256)
    buyername = models.CharField(max_length=64)
    buyerphone = models.CharField(max_length=11)
    buyeraddress = models.CharField(max_length=128)


    class Meta:
        db_table = 'order'



