from django.db import models
from django.utils import timezone

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    email = models.EmailField()

class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    direction = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Table(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    person_capacity = models.IntegerField()

class TablesRestaurant(models.Model):
    id = models.AutoField(primary_key=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    cost_per_unit = models.IntegerField()
    all_restaurants = models.BooleanField()

class ProductsRestaurant(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class Waiter(models.Model):
    OPCIONES_CHOICES = [
        ('MG', 'MANAGER'),
        ('AT', 'ADMINTABLES'),
        ('EX', 'EXTRA')
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    charge = models.CharField(max_length=50, choices=OPCIONES_CHOICES)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    waiter = models.ForeignKey(Waiter, on_delete=models.CASCADE)
    table_restaurant = models.ForeignKey(TablesRestaurant, on_delete=models.CASCADE)

class ProductsOrder(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    tip_percent = models.DecimalField(max_digits=5, decimal_places=2)
    final_cost = models.DecimalField(max_digits=5, decimal_places=2)

class TipWaiter(models.Model):
    id = models.AutoField(primary_key=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    waiter = models.ForeignKey(Waiter, on_delete=models.CASCADE)
    paid = models.BooleanField()

class WaiterShift(models.Model):
    id = models.AutoField(primary_key=True)
    waiter = models.ForeignKey(Waiter, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date