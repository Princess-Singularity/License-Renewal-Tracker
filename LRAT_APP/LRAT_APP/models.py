from django.db import models
from django.contrib.auth.models import User

class UserDashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_logins = models.IntegerField(default=0)
    last_login_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

