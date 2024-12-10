from django.db import models
from rest_framework.exceptions import ValidationError
import uuid

class User(models.Model):
    userID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=24, unique=True)
    password = models.CharField(max_length=16)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.username

class Order(models.Model):
    orderID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userID = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
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
    def __str__(self):
        return f"Order {self.id} by {self.userID.username}"
    
    def clean(self):
        if self.status == self.PENDING:
            pending_orders = Order.objects.filter(user=self.user, status=self.PENDING)
            if self.pk is None and pending_orders.exists():
                raise ValidationError("You can only have one pending order at a time.")
            elif self.pk is not None and pending_orders.exclude(pk=self.pk).exists():
                raise ValidationError("You can only have one pending order at a time.")
        super().clean()

    def checkout(self, *args, **kwargs):
        if self.status == 'PENDING':
            self.status = 'PROCESSED'
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f"Order {self.orderID} - {self.status} - {self.userID.username}"

class CartItem(models.Model):
    cartItemID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='cart_items')
    productName = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.productName} in Order ID: {self.orderID.orderID}"