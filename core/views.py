from django.shortcuts import render , redirect , get_object_or_404 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import *
from .forms import *
from django.views.generic.detail import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def Index (request):
    return render(request,'app/Index.html')

def base(request):
    return render(request, 'app/base.html')

def listarProductoAdmin(request):
    productos  = Producto.objects.all()
    contexto = {'productos' : productos}
    return render(request, 'productos/listar.html', contexto)

def agregarProductoAdmin(request):
    mydict = {
        'form': ProductoForm(),
    } 
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto guardado correctamente.")
            return redirect(to= "core:listarProductoAdmin")
        else:
            mydict["form"] = formulario
    return render(request,'productos/agregar.html',context=mydict)


def modificarProductoAdmin(request,id):
    producto = get_object_or_404(Producto, id=id)

    mydict = {
        'form': ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForm(data = request.POST, instance=producto , files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto modificado correctamente")
            return redirect(to= "core:listarProductoAdmin")
    return render(request, 'productos/modificar.html',context=mydict)

def eliminarProductoAdmin(request ,id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente")
    return redirect(to= "core:listarProductoAdmin")


def listaProductosCliente(request):
    productos  = Producto.objects.all()
    contexto = {'productos' : productos}
    return render(request, 'productos/listadoCliente.html', contexto)


#......................................USUARIOS.....................................


def registroCliente(request):
    mydict = {
        'form': UserForm(),
    } 
    if request.method == 'POST':
        formulario = UserForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Usuario registrado correctamente.")
            return redirect(to= "login")
        else:
            mydict["form"] = formulario
    return render(request,'registration/registro.html',context=mydict)

class verProducto(DetailView):
    model = Producto
    template_name = 'productos/vistaProducto.html'

def PRUEBA(request):
    return render(request,"productos/uwu.html")

@login_required
def agregar_al_carrito(request, slug):
    item = get_object_or_404(Producto, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #CHEQUEA SI ES QUE LA ORDEN DEL ITEM YA EXISTE
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Se agregó un nuevo item a su carrito ")
            return redirect(to= "core:verProducto" , slug =slug)
        else:
            order.items.add(order_item)
            messages.info(request, "Este item fue agregado a su carrito.")
            return redirect(to= "core:verProducto" , slug =slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Se ha creado el item en su carrito.")
        return redirect(to= "core:verProducto" , slug =slug)





class carrito_de_compras(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            
            return render(self.request, 'productos/carrito.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "No tienes una orden activa")
            return redirect("core:carritoSinOrden")




def remover_del_carrito(request, slug):
    item = get_object_or_404(Producto, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "El producto fue removido del carrito.")
            return redirect("core:carrito_de_compras")
        else:
            messages.info(request, "El item no está en el carrito.")
            return redirect("core:verProducto", slug=slug)
    else:
        messages.info(request, "No tienes ninguna orden activa.")
        return redirect("core:verProducto", slug=slug)


def carritoSinOrden (request):
    return render(request,'productos/carritoSinOrden.html')


@login_required
def remover_1_item_carrito(request, slug):
    item = get_object_or_404(Producto, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "Se disminuyó la cantidad del producto.")
            return redirect("core:carrito_de_compras")
        else:
            messages.info(request, "Este item no está en tu carrito")
            return redirect("core:verProducto", slug=slug)
    else:
        messages.info(request, "No tienes una orden activa")
        return redirect("core:verProducto", slug=slug)


def agregar_1_item_carrito(request, slug):
    item = get_object_or_404(Producto, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #CHEQUEA SI ES QUE LA ORDEN DEL ITEM YA EXISTE
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Se aumentó la cantidad del producto.")
            return redirect(to= "core:carrito_de_compras")
        else:
            order.items.add(order_item)
            messages.info(request, "Este item fue agregado a su carrito.")
            return redirect(to= "core:carrito_de_compras" )
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Se ha creado el item en su carrito.")
        return redirect(to= "core:carrito_de_compras" )


class realizarPago(View):
    def get(self,request,*args, **kwargs):
        order  = get_object_or_404(Order,user=self.request.user , ordered= False)
        data = {
            'object' : order
        }
        try:
            
            order.ordered = True
            order.save()
            messages.success(request, "La compra ha sido realizada")
            return render (request, 'productos/compraRealizada.html')
        except Order.DoesNotExist:
            return redirect ("core:Index")
            