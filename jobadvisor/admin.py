"""JobAdvisor admin panel."""
from django.contrib import admin
from django.contrib.auth.models import Group

from fcm_django.models import FCMDevice

admin.site.site_header = "JobAdvisor"
admin.site.site_title = "JobAdvisor"
admin.site.index_title = "Administration"
admin.site.unregister(Group)
admin.site.unregister(FCMDevice)
