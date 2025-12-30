from django.db import models

class BotState(models.Model):
    user_id = models.BigIntegerField(unique=True, db_index=True)
    chat_id = models.BigIntegerField(db_index=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    data = models.JSONField(default=dict, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'chat_id']),
        ]

    def __str__(self):
        return f"State for {self.user_id}"
