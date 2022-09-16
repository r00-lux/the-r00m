from django.contrib import admin
from profiles import models

admin.site.register(models.Profile)
admin.site.register(models.ProfileFeedItem)

print('Intentional error')