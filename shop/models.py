from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=800, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveBigIntegerField(default=1)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product/%y/%m/%d')

    def __str__(self):
        return self.name
    def average(self):
        ratings = self.ratings.all()
        if ratings.count() > 0:
            return sum([rating.rating for rating in ratings])/ratings.count()
        return 0


    

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product','user')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    

class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_total_item(self):
        return sum(item.quantity for item in self.items.all())
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE , related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_cost(self):
        return self.product.price*self.quantity

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending','Pending'),
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Deliverey','Deliverey'),
        ('Canceled','Canceled')
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
    default='pending')
    note = models.TextField(max_length=50)
    paid = models.BooleanField(default=True)
    transaction = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id}"
    
    class Meta:
        ordering = ['-created']

    def get_total_cost(self):
        sum(item.get_cost() for item in self.items.all())
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_cost(self):
        return self.product.price*self.quantity


