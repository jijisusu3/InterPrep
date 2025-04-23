from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
# Create your models here.

class Application(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    desired_role = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    batch_number = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.user.username} → {self.desired_role}"

class PracticeQuestionSet(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    text = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    batch_number  = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["batch_number", "id"]

    def __str__(self):
        return f"[Batch {self.batch_number}] {self.text[:50]}…"

class PracticeAnswer(models.Model):
    question_set = models.ForeignKey(PracticeQuestionSet, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question_index = models.PositiveIntegerField()
    answer_text    = models.TextField()
    score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    submitted_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Answer by {self.user.username} on Q{self.question.id}"
    
