from django.contrib import admin

# Register your models here.
from .models import Application, PracticeQuestionSet, PracticeAnswer

admin.site.register(Application)
admin.site.register(PracticeQuestionSet)
admin.site.register(PracticeAnswer)