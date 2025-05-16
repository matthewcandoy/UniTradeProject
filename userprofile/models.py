from django.contrib.auth.models import User
from django.db import models

class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    is_vendor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class Payment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[('paid', 'Paid'), ('failed', 'Failed')])

    def __str__(self):
        return f"Payment {self.id} - {self.status}"