from django.db import models

class BotUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Question(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='questions/', null=True, blank=True)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
    ])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.text[:50]

class TestAttempt(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.score}/{self.total_questions}"

class AttemptDetail(models.Model):
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='details')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=1, null=True, blank=True)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.attempt.user.full_name} - {self.question.id} ({self.is_correct})"

class BotState(models.Model):
    """
    Stores FSM state for Aiogram persistence.
    Replaces Redis for 'free' robust error handling.
    """
    user_id = models.BigIntegerField(unique=True, db_index=True)
    chat_id = models.BigIntegerField(db_index=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    data = models.JSONField(default=dict, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'chat_id']),
        ]
