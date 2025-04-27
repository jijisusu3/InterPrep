from django.contrib import admin

# Register your models here.
from .models import Application, PracticeRecord

admin.site.register(Application)
admin.site.register(PracticeRecord)