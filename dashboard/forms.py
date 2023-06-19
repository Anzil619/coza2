


from django import forms
from store.models import Product


class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['product_name', 'slug', 'price', 'images', 'image1', 'image2',
                  'image3', 'stock', 'category', 'sub_category', 'description']
        
        labels = {

            'product_name': 'product_name',
            'slug': 'slug',
            'price': 'price',
            'images': 'images',
            'image1': 'image1',
            'image2': 'image2',
            'image3': 'image3',
            'stock': 'stock',
            'category': 'category',
            'sub_category': 'sub_category',
            'description': 'description'

        }

# class Update_ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['product_name','slug', 'price', 'image','image1','image2','image3', 'stock', 'category','sub_category',]
#         labels = {
#             'product_name': 'product_name',
#                    'slug' :'slug' ,
#                    'price': 'price',
#                    'image': 'image',
#                   'image1':'image1',
#                   'image2':'image2',
#                   'image3':'image3',
#                    'stock': 'stock',
#                 'category': 'category',
#             'sub_category':'sub_category'
           
#         }