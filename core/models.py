from django.db import models
from django.db.models.fields import IntegerField
from django.forms.fields import ImageField
from django.shortcuts import reverse
from django.conf import settings

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    descripcion = models.CharField (max_length=50)
    descuento = models.IntegerField(null=True , blank=True)
    img = models.ImageField(upload_to= "productos", null= False)
    slug = models.SlugField()



    def __str__(self):
        return self.nombre

    def calculo_descto(self):
        return self.precio - (self.descuento * self.precio / 100) 

    def ver_producto(self):
        return reverse("core:productos", kwargs={
            'slug': self.slug
        })
    def agregar_carrito(self):
        return reverse("core:add_to_cart", kwargs={
            'slug': self.slug
        })

    def remover_carrito(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    item = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.nombre}"

    def precio_total_por_item(self):
        return self.quantity * self.item.precio

    def precio_total_por_item_descuento(self):
        return self.quantity * (self.item.precio - (self.item.descuento * self.item.precio / 100) )

    def total_ahorrado(self):
        return self.precio_total_por_item() - self.precio_total_por_item_descuento()

    
    def precio_final_descuento(self):
        return self.precio_total_por_item_descuento()

    def precio_final(self):
        if self.item.descuento:
            return self.precio_total_por_item_descuento()
        return self.precio_total_por_item()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

    def total_pago (self):
        total = 0
        for order_producto in self.items.all():
            total += order_producto.precio_final()
        return total

    def total_descuento (self):
        total = 0
        for order_producto in self.items.all():
            total += order_producto.precio_final_descuento()
        return total