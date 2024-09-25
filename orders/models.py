from django.db import models

class Bnb(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Room(models.Model):
    bnb = models.ForeignKey(Bnb, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Order(models.Model):
    CURRENCY_CHOICES = [
        ('TWD', 'Taiwan Dollar'),
        ('USD', 'US Dollar'),
        ('JPY', 'Japanese Yen'),
    ]
    
    bnb = models.ForeignKey(Bnb, on_delete=models.CASCADE, related_name='orders')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='orders')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    amount = models.PositiveIntegerField()
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} for {self.room.name} ({self.bnb.name})"
