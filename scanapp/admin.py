from django.contrib import admin

# Import models from scanapp.models
from scanapp.models import ScanInfo
from scanapp.models import UserInfo
from scanapp.models import URLScanInfo
from scanapp.models import LocalScanInfo
from scanapp.models import CodeInfo
from scanapp.models import ScanResult
from scanapp.models import ScanFileInfo
from scanapp.models import License
from scanapp.models import MatchedRule
from scanapp.models import MatchedRuleLicenses
from scanapp.models import Copyright
from scanapp.models import CopyrightHolders
from scanapp.models import CopyrightStatements
from scanapp.models import CopyrightAuthor
from scanapp.models import Package
from scanapp.models import ScanError

# Register models from scancode.models
admin.site.register(ScanInfo)
admin.site.register(UserInfo)
admin.site.register(URLScanInfo)
admin.site.register(LocalScanInfo)
admin.site.register(CodeInfo)
admin.site.register(ScanResult)
admin.site.register(ScanFileInfo)
admin.site.register(License)
admin.site.register(MatchedRule)
admin.site.register(MatchedRuleLicenses)
admin.site.register(Copyright)
admin.site.register(CopyrightHolders)
admin.site.register(CopyrightStatements)
admin.site.register(CopyrightAuthor)
admin.site.register(Package)
admin.site.register(ScanError)
