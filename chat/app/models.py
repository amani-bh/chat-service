from django.db import models


class User(models.Model):
    user_id = models.PositiveIntegerField()
    user_name = models.CharField(max_length=255)
    user_image = models.URLField()


class Conversation(models.Model):
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_first_user')
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_second_user')


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.CharField(max_length=1200)
    is_read = models.BooleanField(default=False)
    seen_at=models.DateTimeField(null=True, blank=True)
    attachment=models.URLField(blank=True)
    attachment_type=models.CharField(max_length=255,default="image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('created_at',)



