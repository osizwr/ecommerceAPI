from django.db import models
from rest_framework.exceptions import ValidationError
import uuid

class User(models.Model):
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=24, unique=True)
    password = models.CharField(max_length=16)
    email = models.EmailField(unique=True, unique=True)

    def __str__(self):
        return self.username

class Order(models.Model):
    orderId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userfk = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    PENDING = 'PENDING'
    PROCESSED = 'PROCESSED'
    CANCELLED = 'CANCELLED'
    status = models.CharField(max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('PROCESSED', 'Processed'),
            ('CANCELLED', 'Cancelled')
        ],
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.status == self.PENDING:
            pending_orders = Order.objects.filter(user=self.user, status=self.PENDING)
            if self.pk is None and pending_orders.exists():
                raise ValidationError("A user can only have one pending order at a time.")
            elif self.pk is not None and pending_orders.exclude(pk=self.pk).exists():
                raise ValidationError("A user can only have one pending order at a time.")
        super().clean()

    def checkout(self, *args, **kwargs):
        if self.status == 'PENDING':
            self.status = 'PROCESSED'
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f"Order {self.orderId} - {self.status} - {self.userfk.username}"

class CartItem(models.Model):
    cartItemId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orderfk = models.ForeignKey(Order, on_delete=models.CASCADE)
    productName = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.productName} in Order ID: {self.orderfk.orderId}"