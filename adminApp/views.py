from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView,DetailView,FormView,CreateView,ListView,DeleteView,UpdateView
from ekartApp.models import Products, Category,Cart,Order
from django.contrib.auth.models import User
from adminApp.forms import OrderUpdateForm,ProductForm,CategoryForm
from django.urls import reverse_lazy
from django.core.mail import send_mail,settings
from django.contrib import messages
# Create your views here.

class AdminHomeView(TemplateView):
    template_name = "adminhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Products.objects.all()
        context['categories'] = Category.objects.all()
        context['orders'] = Order.objects.filter(status='order-placed').count()
        context['users'] = User.objects.all().count()
        return context



class AdminUserListView(ListView):
    template_name='adminuserlist.html'
    model=User
    context_object_name='users'


class AdminEditUserView(UpdateView):
    template_name='adminedituser.html'
    model=User
    fields=['is_active','is_staff']
    pk_url_kwarg='id'
    success_url=reverse_lazy('admin_user_list')

class AdminDeleteUserView(DeleteView):
    def get(self, request, *args, **kwargs):
        user=User.objects.get(id=kwargs.get('id'))
        user.delete()
        messages.success(self.request,'User deleted successfully!')
        return redirect('admin_user_list')




class AdminOrderListView(ListView):
    template_name='adminorderlist.html'
    model=Order
    context_object_name='orders'

    def get_queryset(self):
        return Order.objects.exclude(status='in-cart')
    


class AdminPendingOrderListView(ListView):
    template_name='adminpendingorderlist.html'
    model=Order
    context_object_name='orders'

    def get_queryset(self):
        return Order.objects.filter(status='order-placed')


class AdminProductListView(ListView):
    template_name='adminproductlist.html'
    model=Products
    context_object_name='products'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        sort_by = self.request.GET.get('sort', 'none')  # Default ordering by id

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        
        if sort_by == 'product_name':
            queryset = queryset.order_by('product_name')
        elif sort_by == 'price':
            queryset = queryset.order_by('price')
        elif sort_by == 'category':
            queryset = queryset.order_by('category__category_name')
        else:
            queryset = queryset.order_by('id')  # Default ordering

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from ekartApp.models import Category
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_sort'] = self.request.GET.get('sort', 'none')
        return context


class AdminCategoryListView(ListView):
    template_name='admincategorylist.html'
    model=Category
    context_object_name='categories'





class OrderUpdateView(TemplateView):
    # form_class=OrderUpdateForm
    template_name='updateorder.html'
    success_url=reverse_lazy('admin_home')

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['order']=Order.objects.get(id=kwargs.get('id'))
        # context['form']=OrderUpdateForm(initial={'status':context['order'].status,'product':context['order'].Product.product,'user':context['order'].user,'quantity':context['order'].Product.quantity})
        context['form']=OrderUpdateForm()
        return context
    
    def post(self, request, **kwargs):
        form = OrderUpdateForm(request.POST)
        if form.is_valid():
            product = Order.objects.get(id=kwargs.get('id'))
            status = form.cleaned_data['status']
            expected_delivery_date = form.cleaned_data.get('expected_delivery_date')
            email = product.user.email
            if status == 'out-of-stock':
                expected_delivery_date = None  # Clear expected delivery date for out of stock
                send_mail(
                    'Order Update',
                    'Your order is out of stock. We apologize for the inconvenience.',
                    settings.EMAIL_HOST_USER,
                    [email])
            else:
                message = f'Your order status has been updated to {status}.'
                if expected_delivery_date:
                    message += f' Expected delivery date: {expected_delivery_date}'
                send_mail(
                    'Order Update',
                    message,
                    settings.EMAIL_HOST_USER,
                    [email])
            product.status = status
            product.expected_delivery_date = expected_delivery_date
            product.save()
            messages.success(request, 'Order updated successfully!')
            return redirect('admin_order_list')
        else:
            messages.error(request, 'Invalid form data.')
            return self.get(request, **kwargs)
        
        
class OrderDeleteView(DeleteView):
    def get(self, request, *args, **kwargs):
       item=Order.objects.get(id=kwargs.get('id'))
       item.delete()
       messages.success(self.request,'Order deleted successfully!')
       return redirect('admin_order_list')





class AdminCreateProductView(CreateView):
    template_name='admincreateproduct.html'
    form_class=ProductForm
    model=Products
    success_url=reverse_lazy('admin_product_list')

    # def get(self, request, *args, **kwargs):
    #     form = ProductForm()
    #     return render(request, self.template_name, {'form': form})



class AdminDeleteProductView(DeleteView):
    def get(self,request,**kwargs):
        item=Products.objects.get(id=kwargs.get('pk'))
        item.delete()
        messages.success(self.request,'Product deleted successfully!')
        return redirect('admin_product_list')



class EditProductView(View):
    template_name='admineditproduct.html'
    form_class=ProductForm
    success_url=reverse_lazy('admin_product_list')

    def get(self, request, **kwargs):
        product=Products.objects.get(id=kwargs.get('id'))
        form=ProductForm(instance=product)
        return render(request,self.template_name,{'form':form,'product':product})
    def post(self, request, **kwargs):
        product=Products.objects.get(id=kwargs.get('id'))
        form=ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            messages.success(self.request,'Product updated successfully!')
            return redirect(self.success_url)
        


class CategoryCreateView(CreateView):
    template_name='admincreatecategory.html'
    model=Category
    form_class=CategoryForm
    success_url=reverse_lazy('admin_category_list')



class CategoryUpdateView(UpdateView):
    template_name='admineditcategory.html'
    model=Category
    form_class=CategoryForm
    success_url=reverse_lazy('admin_category_list')


class CategoryDeleteView(DeleteView):
    def get(self,request,**kwargs):
        item=Category.objects.get(id=kwargs.get('pk'))
        # Check if category has associated products
        if Products.objects.filter(category=item).exists():
            messages.error(self.request,'Cannot delete category because it has associated products. Please delete the products first.')
            return redirect('admin_category_list')
        item.delete()
        messages.success(self.request,'Category deleted successfully!')
        return redirect('admin_category_list')
