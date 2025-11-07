from ekartApp.models import Cart, Products,Order



def Cart_count(request):
    if request.user.is_authenticated:
        cart_count=Cart.objects.filter(user=request.user,status='in-cart').count()
    else:
        cart_count=0
    return {'cart_count':cart_count}


def Order_count(request):
    if request.user.is_authenticated:
        order_count=Order.objects.filter(user=request.user,status='order-placed').count()
    else:
        order_count=0
    return {'order_count':order_count}
