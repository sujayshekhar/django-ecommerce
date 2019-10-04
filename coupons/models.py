from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Coupon(models.Model):
    code = models.CharField(unique=True, max_length=50)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return self.code
