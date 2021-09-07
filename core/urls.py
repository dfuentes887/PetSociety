from django.urls import path
from core.views import *


app_name = 'core'

urlpatterns = [
    path('', Index  , name= "Index"),
    path('PRUEBA', PRUEBA  , name= "PRUEBA"),
    path('listadoProductoAdmin' , listarProductoAdmin , name= "listarProductoAdmin"),
    path('agregarProductoAdmin' , agregarProductoAdmin , name= "agregarProductoAdmin"),
    path('modificarProductoAdmin/<id>' , modificarProductoAdmin , name= "modificarProductoAdmin"),
    path('eliminarProductoAdmin/<id>' , eliminarProductoAdmin , name= "eliminarProductoAdmin"),
    path('lista-productos' , listaProductosCliente , name= "listaProductosCliente"),
    path('productos/<slug>' , verProducto.as_view() , name= "verProducto"),
    path('agregar-al-carrito/<slug>' , agregar_al_carrito, name= "add_to_cart"),
    path('carrito' , carrito_de_compras.as_view(), name= "carrito_de_compras"),
    path('remover-del-carrito/<slug>/', remover_del_carrito, name='remover_del_carrito'),
    path('remover-1-item/<slug>/', remover_1_item_carrito, name='remover_1_item_carrito'),
    path('agregar-1-item-al-carrito/<slug>' , agregar_1_item_carrito, name= "agregar_1_item_carrito"),
    path('carrito-vacio' , carritoSinOrden, name= "carritoSinOrden"),
    path('pago-realizado', realizarPago.as_view(), name = "realizarPago"),




    #USUARIO
    path('accounts/register' , registroCliente , name= "registroCliente"),
]
