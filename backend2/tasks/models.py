from django.db import models

class Task(models.Model):
    user_id = models.IntegerField()  # from Node JWT
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    effort = models.IntegerField()
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)
