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


#
from django.utils.crypto import salted_hmac


class Community(models.Model):
    name = models.CharField(max_length=64)
    province = models.CharField(max_length=16)
    city = models.CharField(max_length=16)
    area = models.CharField(max_length=16)
    address = models.CharField(max_length=256)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=4)


    class Meta:
        db_table = 'community'


class User(models.Model):
    name = models.CharField(max_length=64)
    nickname = models.CharField(max_length=64)
    pswd = models.CharField(max_length=32)
    community = models.ForeignKey(Community, blank=True, null=True, on_delete=None)
    email = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    yongjin = models.IntegerField()
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
    name = models.CharField(max_length=128)
    checked = models.IntegerField()
    message = models.CharField(max_length=256)
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