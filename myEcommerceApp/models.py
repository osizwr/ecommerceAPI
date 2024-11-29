from django.db import models
import uuid


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

class User(models.Model):
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

class Order(models.Model):
    orderId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userfk = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Processed', 'Processed'),
            ('Cancelled', 'Cancelled')
        ],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        cons = [models.UniqueConstraint(fields=['user', 'status'], condition=models.Q(status='Pending'), name='uniquePendingOrder')]

    def __str__(self):
        return f"Order ID: {self.orderId} - {self.status}"

class CartItem(models.Model):
    cartItemId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orderfk = models.ForeignKey(Order, on_delete=models.CASCADE)
    productName = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.productName} in Order ID: {self.orderfk.orderId}"
