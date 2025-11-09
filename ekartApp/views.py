from django.shortcuts import render,redirect
from django.views.generic import View, TemplateView,DetailView,FormView,CreateView,ListView,DeleteView
from ekartApp.models import Products, Category,Cart,Order
from ekartApp.forms import RegisterForm,LoginForm,CartForm,OrderForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail,settings
from django.utils.decorators import method_decorator
from ekartApp.decorators import login_required


import razorpay
from django.views.decorators.csrf import csrf_exempt
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))



# Create your views here.
class HomeView(TemplateView):
    template_name="index.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['products']=Products.objects.all()
        context['categories']=Category.objects.all()
        return context
    def get(self, request, *args, **kwargs):
        user=request.user
        if user.is_authenticated:
            if user.is_superuser and not request.GET.get('view_store'):
                return redirect('admin_home')
        return super().get(request, *args, **kwargs)
    

class ProductDetailView(DetailView):
    template_name='detail1.html'
    pk_url_kwarg='id'
    model=Products
    context_object_name='product'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['related_products']=Products.objects.filter(category=context['product'].category).exclude(id=context['product'].id)[:6]
        return context







@method_decorator(login_required,name='dispatch')
class AddToCartView(View):
    # template_name = 'addtocart.html'
    # # success_url = reverse_lazy('home_view')

    # def get_context_data(self, **kwargs):
    #     context= super().get_context_data(**kwargs)
    #     context['product']=Products.objects.get(id=kwargs.get('id'))
    #     context['form']=CartForm()
    #     return context

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            product=Products.objects.get(id=kwargs.get('id'))
            user=request.user
            quantity=request.GET.get('quantity', 1)
            # try:
            #     quantity = int(quantity)
            #     if quantity <= 0:
            #         quantity = 1
            # except ValueError:
            #     quantity = 1
            quantity = int(quantity)
            if quantity <= 0:
                quantity = 1
            incart=Cart.objects.filter(product=product,user=user,status='in-cart').first()
            if incart:
                incart.quantity+=quantity
                incart.save()
                messages.success(self.request,'Product quantity updated in cart')
            else:
                Cart.objects.create(product=product,quantity=quantity,user=user)
                messages.success(self.request,'Product added to cart')
            return redirect('cart_list')
        else:
            messages.warning(self.request,'Please login to add product to cart')
            return redirect('login')

    # def post(self, request, **kwargs):
    #     if request.user.is_authenticated:
    #         form=CartForm(request.POST)
    #         if form.is_valid():
    #             # kk=Cart.objects.get(id='2')
    #             # kk.delete()
    #             product=Products.objects.get(id=kwargs.get('id'))
    #             user=request.user
    #             quantity=form.cleaned_data.get('quantity')
    #             incart=Cart.objects.filter(product=product,user=user,status='in-cart').first()
    #             if incart:
    #                 incart.quantity+=int(quantity)
    #                 incart.save()
    #                 messages.success(self.request,'Product quantity updated in cart')

    #             else:
    #                 Cart.objects.create(product=product,quantity=quantity,user=user)
    #                 messages.success(self.request,'Product added to cart')
    #             return redirect('home_view')
    #         else:
    #             messages.error(self.request,'Failed to add product to cart')
    #             return redirect('detail_view',id=kwargs.get('id'))
    #     else:
    #         messages.warning(self.request,'Please login to add product to cart')
    #         return redirect('login')

@method_decorator(login_required,name='dispatch')
class CartListView(ListView):
    template_name='cartlist.html'
    model=Cart
    context_object_name='carts'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user,status='in-cart')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carts = context['carts']
        total = 0
        for cart in carts:
            cart.total = cart.product.price * cart.quantity
            total += cart.total
        context['grand_total'] = total
        return context


@method_decorator(login_required,name='dispatch')
class CartDeleteView(DeleteView):
    def get(self,request,**kwargs):
        item=Cart.objects.get(id=kwargs.get('id'))
        item.delete()
        messages.success(self.request,'Item removed from cart')
        return redirect('cart_list')
    




@method_decorator(login_required,name='dispatch')
class PlaceOrderView(TemplateView):
    template_name='placeorder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carts = Cart.objects.filter(user=self.request.user, status='in-cart')
        total = 0
        for cart in carts:
            cart.total = cart.product.price * cart.quantity
            total += cart.total
        context['carts'] = carts
        context['grand_total'] = total
        context['form'] = OrderForm()
        return context

    def post(self, request, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            carts = Cart.objects.filter(user=request.user, status='in-cart')
            total = sum(cart.product.price * cart.quantity for cart in carts)
            amount = int(total * 100)  # Amount in paise
            payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
            # Store shipping info in session for later use
            request.session['shipping_address'] = form.cleaned_data['shipping_address']
            request.session['contact_number'] = form.cleaned_data['contact_number']
            request.session['order_type'] = 'cart'
            return render(request, 'payment.html', {
                'payment': payment,
                'amount': amount,
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'carts': carts,
                'grand_total': total,
                'shipping_address': form.cleaned_data['shipping_address'],
                'contact_number': form.cleaned_data['contact_number']
            })
        else:
            messages.error(request, 'Failed to place order. Please check the form.')
            return self.get(request, **kwargs)




@method_decorator(login_required,name='dispatch')
class OrderListView(ListView):
    template_name='orderlist.html'
    model=Order
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['orders']=self.get_queryset()
        total=0
        for order in context['orders']:
            order.total=order.Product.product.price*order.Product.quantity
            total+=order.total
        context['total']=total
        return context

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user,status='order-placed')



@method_decorator(login_required,name='dispatch')
class BuyNowPlaceOrderView(TemplateView):
    template_name='buy_now_placeorder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Products.objects.get(id=kwargs.get('id'))
        quantity = self.request.GET.get('quantity', 1)
        quantity = int(quantity) if quantity.isdigit() and int(quantity) > 0 else 1
        total = product.price * quantity
        context['product'] = product
        context['quantity'] = quantity
        context['total'] = total
        context['form'] = OrderForm()
        return context

    def post(self, request, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            product = Products.objects.get(id=kwargs.get('id'))
            quantity = self.request.GET.get('quantity', 1)
            quantity = int(quantity) if quantity.isdigit() and int(quantity) > 0 else 1
            total = product.price * quantity
            amount = int(total * 100)  # Amount in paise
            payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
            # Store shipping info and product details in session
            request.session['shipping_address'] = form.cleaned_data['shipping_address']
            request.session['contact_number'] = form.cleaned_data['contact_number']
            request.session['order_type'] = 'buy_now'
            request.session['product_id'] = kwargs.get('id')
            request.session['quantity'] = quantity
            return render(request, 'payment.html', {
                'payment': payment,
                'amount': amount,
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'product': product,
                'quantity': quantity,
                'grand_total': total,
                'shipping_address': form.cleaned_data['shipping_address'],
                'contact_number': form.cleaned_data['contact_number']
            })
        else:
            messages.error(request, 'Failed to place order. Please check the form.')
            return self.get(request, **kwargs)



@method_decorator(login_required,name='dispatch')
class OrderCancelView(DeleteView):
    def get(self,request,**kwargs):
        item=Order.objects.get(id=kwargs.get('id'))
        item.delete()
        messages.success(self.request,'Order cancelled')
        return redirect('order_list')

    # template_name='order_cancel.html'
    # model=Order
    # pk_url_kwarg='id'
    # success_url=reverse_lazy('order_list')


        


class RegisterView(CreateView):
    form_class=RegisterForm
    model=User
    template_name='register.html'
    success_url=reverse_lazy('home_view')

    def form_valid(self, form):
        User.objects.create_user(**form.cleaned_data)
        print('success')
        messages.success(self.request,'Registration Sucess')
        return redirect('home_view')
    def form_invalid(self, form):
        print('failed')
        messages.error(self.request,'Registration failed')
        return super().form_invalid(form)




class LoginView(FormView):
    template_name='login.html'
    form_class=LoginForm

    def post(self, request, *args, **kwargs):
        uname=request.POST.get("username")
        psw=request.POST.get('password')
        user=authenticate(request,username=uname,password=psw)
        if user:
            
            if user.is_superuser:
                login(request,user)
                messages.success(self.request,'admin login Sucess')
                return redirect('admin_home')
            else:
                login(request,user)
                messages.success(self.request,'login Sucess')
                return redirect('home_view')
        else:
            messages.warning(self.request,'login failed')
            return redirect('login')

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(self.request,'logout Sucess')
        return redirect('login')


class DemoView(TemplateView):
    template_name='home.html'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['products']=Products.objects.all()
        context['categories']=Category.objects.all()
        return context
        


class CatListView(ListView):
    template_name='cat_list.html'
    model=Products
    context_object_name='products'
    def get_queryset(self):
        self.category=Category.objects.get(id=self.kwargs.get('id'))
        return Products.objects.filter(category=self.category)[:9]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
    





class Start_PaymentView(View):
    def post(self, request, *args, **kwargs):
        amount = int(request.POST.get('amount')) * 100  # Amount in paise
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        return render(request, 'payment.html', {'payment': payment, 'amount': amount, 'razorpay_key_id': settings.RAZORPAY_KEY_ID})
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        # Retrieve shipping info from session
        shipping_address = request.session.get('shipping_address')
        contact_number = request.session.get('contact_number')
        order_type = request.session.get('order_type')

        if order_type == 'cart':
            carts = Cart.objects.filter(user=request.user, status='in-cart')
            for cart in carts:
                Order.objects.create(
                    user=request.user,
                    Product=cart,
                    shipping_address=shipping_address,
                    contact_number=contact_number
                )
                cart.status = 'order-placed'
                cart.save()
                send_mail(
                    'Order Confirmation - Ekart',
                    f'Thank you for your order! Your order for {cart.product.product_name} has been placed successfully.',
                    settings.EMAIL_HOST_USER,
                    [request.user.email])
        elif order_type == 'buy_now':
            product_id = request.session.get('product_id')
            quantity = request.session.get('quantity')
            product = Products.objects.get(id=product_id)
            cart = Cart.objects.create(
                product=product,
                quantity=quantity,
                user=request.user,
                status='order-placed'
            )
            Order.objects.create(
                user=request.user,
                Product=cart,
                shipping_address=shipping_address,
                contact_number=contact_number
            )
            send_mail(
                'Order Confirmation - Ekart',
                f'Thank you for your order! Your order for {product.product_name} has been placed successfully.',
                settings.EMAIL_HOST_USER,
                [request.user.email])

        # Clear session data
        request.session.pop('shipping_address', None)
        request.session.pop('contact_number', None)
        request.session.pop('order_type', None)
        request.session.pop('product_id', None)
        request.session.pop('quantity', None)

        messages.success(request, 'Payment successful! Order placed.')
        return render(request, 'payment_success.html', {'payment_id': payment_id})
    else:
        return redirect('home_view')
    