from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Application(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    desired_role = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.desired_role}"

class PracticeRecord(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    question_text = models.TextField()
    batch_number  = models.PositiveSmallIntegerField()
    answer_text = models.TextField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    is_scored = models.BooleanField(default=False)
    feedback = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True, help_text="When the user first answered")

    class Meta:
        ordering = ["batch_number", "id"]

    def __str__(self):
        return f"[Batch {self.batch_number}] {self.answer_text}…"

