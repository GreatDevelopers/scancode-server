from __future__ import unicode_literals

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class ScanInfo(models.Model):
    def __str__(self):
        return self.scan_type

    # types of scans that can be applied
    scan_types = (
        ('URL', 'URL'),
        ('Local Scan', 'localscan'),
    )

    scan_type = models.CharField(max_length=20, choices=scan_types, default='URL')


class UserInfo(models.Model):
    def __str__(self):
        return self.user.username

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scan_info = models.ForeignKey(ScanInfo)


class URLScanInfo(models.Model):
    def __str__(self):
        return self.URL

    scan_info = models.ForeignKey(ScanInfo)
    URL = models.URLField(max_length=2000)


class LocalScanInfo(models.Model):
    def __str__(self):
        return self.folder_name

    scan_info = models.ForeignKey(ScanInfo)
    folder_name = models.CharField(max_length=200)


class CodeInfo(models.Model):
    def __str__(self):
        return self.total_code_files

    scan_info = models.ForeignKey(ScanInfo)
    total_code_files = models.IntegerField(null=True, blank=True)
    code_size = models.IntegerField(null=True, blank=True, default=0)


# ScanResult will store the most basic results of the scan
# Single result for each scan
class ScanResult(models.Model):
    def __str__(self):
        return self.total_errors

    code_info = models.ForeignKey(CodeInfo)
    scanned_json_result = JSONField()
    scanned_html_result = models.CharField(max_length=10000)
    scancode_notice = models.CharField(max_length=2000)
    scancode_version = models.CharField(max_length=200)
    files_count = models.IntegerField(null=True, blank=True, default=0)
    total_errors = models.IntegerField(null=True, blank=True, default=0)
    scan_time = models.IntegerField(null=True, blank=True, default=0)


# Single result for each file being scanned
class ScanFileInfo(models.Model):
    def __str__(self):
        return self.file_path

    scan_result = models.ForeignKey(ScanResult)
    file_path = models.CharField(max_length=400)


# Multiple or no result for each file
class License(models.Model):
    def __str__(self):
        return self.key

    scan_file_info = models.ForeignKey(ScanFileInfo)
    category = models.CharField(max_length=1000)
    start_line = models.IntegerField()
    spdx_url = models.URLField(max_length=2000)
    text_url = models.URLField(max_length=2000)
    spdx_license_key = models.CharField(max_length=200)
    homepage_url = models.URLField(max_length=2000)
    score = models.IntegerField()
    end_line = models.IntegerField()
    key = models.CharField(max_length=200)
    owner = models.CharField(max_length=500)
    dejacode_url = models.URLField(max_length=2000)


class MatchedRule(models.Model):
    def __str__(self):
        return self.license_choice

    license = models.ForeignKey(License)
    license_choice = models.BooleanField()
    identifier = models.CharField(max_length=200)


class MatchedRuleLicenses(models.Model):
    def __str__(self):
        return self.license

    matched_rule = models.ForeignKey(MatchedRule)
    license = models.CharField(max_length=200)

class Copyright(models.Model):
    def __str__(self):
        return self.start_line

    scan_file_info = models.ForeignKey(ScanFileInfo)
    start_line = models.IntegerField()
    end_line = models.IntegerField()


class CopyrightHolders(models.Model):
    def __str__(self):
        return self.holder

    copyright = models.ForeignKey(Copyright)
    holder = models.CharField(max_length=400)


class CopyrightStatements(models.Model):
    def __str__(self):
        return self.statement

    copyright = models.ForeignKey(Copyright)
    statement = models.CharField(max_length=500)


class CopyrightAuthor(models.Model):
    def __str__(self):
        return self.author

    copyright = models.ForeignKey(Copyright)
    author = models.CharField(max_length=200)


class Package(models.Model):
    def __str__(self):
        return self.package

    scan_file_info = models.ForeignKey(ScanFileInfo)
    package = models.CharField(max_length=1000)


class ScanError(models.Model):
    def __str__(self):
        return self.scan_error

    scan_file_info = models.ForeignKey(ScanFileInfo)
    scan_error = models.CharField(max_length=1000)

class CeleryScan(models.Model):
    scan_id = models.AutoField(primary_key = True)
    scan_results = models.CharField(max_length = 20000, null=True, blank=True)
    is_complete = models.BooleanField(default = False)

    def __str__(self):
        return str(self.scan_id)
