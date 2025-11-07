from django import forms
from ekartApp.models import Order,Products,Category


class OrderUpdateForm(forms.Form):
    product = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    user=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    status = forms.ChoiceField(choices=[
        ('order-placed', 'Order Placed'),
        ('out-of-stock', 'Out of Stock'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ], widget=forms.Select(attrs={'class':'form-control'}))
    expected_delivery_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))




class ProductForm(forms.ModelForm):
    class Meta:
        model=Products
        fields=['product_name','category','price','description','image']
        widgets={
            'product_name':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
        }    




class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['category_name','image','is_active']
        widgets={
            'category_name':forms.TextInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
            'is_active':forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }   
        