from django.db import models
from django.db.models.signals import pre_save
from service.models import JobPost
from webapp.utils import unique_order_id_generator
from billing.models import BillingProfile

ORDER_STATUS_CHOICES = (
    ('created','Created'),
    ('paid','Paid'),
    ('refunded','Refunded'),
)
class Order(models.Model):
    billing_profile = models.ForeignKey(
        BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.CharField(max_length=120, blank=True)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id


# Generating order id
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender=Order)
# Generating order total
