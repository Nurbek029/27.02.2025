from django.shortcuts import render, get_object_or_404
from .models import Product

def index_view(request):
    product = Product.objects.filter(is_active = True)

    return render(request, 'main/index.html', {"products": product})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    similar_products = Product.objects.filter(category = product.category).exclude(id=product_id)[:4]
    print(similar_products)  # Выведет список в консоль Django
    return render(
        request=request,
        template_name= 'main/product_detail.html',
        context={"product":product, 'similar_products': similar_products})
