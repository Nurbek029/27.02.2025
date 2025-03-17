from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Avg

from .models import Product,Rating,RatingAnswer, PaymentMethod, Order, Category
from .forms import ProductCreateForm, ProductUpdateForm
from .filters import ProductListFilter

def index_view(request):
    product = Product.objects.filter(is_active = True)

    return render(request, 'main/index.html', {"products": product})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_update_form = ProductUpdateForm(instance=product)
    product_comments = Rating.objects.filter(product=product)

    rating_avg = product_comments.aggregate(Avg('count'))['count__avg']
    similar_products = Product.objects.filter(category = product.category).exclude(id=product_id)[:4]
    
    return render(
        request=request,
        template_name= 'main/product_detail.html',
        context={"product":product, 'similar_products': similar_products,
        'product_update_form':product_update_form,
        'product_comments': product_comments,
        'rating_avg': rating_avg
        }
        )

def product_create_view(request):
    if not request.user.is_authenticated:
        raise Http404()
    
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            product_object = form.save(commit=False)
            product_object.user = request.user
            product_object.save()

            messages.success(request, 'Успешно создано!')
            return redirect('index')
    
    form = ProductCreateForm()
    return render(
        request=request,
        template_name='main/product_create.html',
        context={'form':form} )

def product_update_view(request, product_id):
    product = get_object_or_404(Product, id = product_id)
#изменять должен только создатель
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успешно изменено!')
            return redirect('product_detail', product_id)

def rating_create_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not request.user.is_authenticated:
        messages.error(request, 'Только авторизованные!')
        return redirect('product_detail', product_id)

    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        count = int(request.POST.get('count', ''))

        rating = Rating(
            user=request.user,
            product=product,
            count=count,
            comment=comment
        )
        rating.save()
        messages.success(request, 'Спасибо за отзыв!')
        return redirect('product_detail', product_id)

def rating_answer_create_view(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)

    if rating.product.user != request.user:
        messages.error(request, 'Нету доступа')
        return redirect('product_detail', rating.product.id)
    
    if request.method == 'POST':
        comment = request.POST.get('comment', '')

        rating_answer = RatingAnswer(
            user=request.user,
            rating=rating,
            comment=comment
        )

        rating_answer.save()

        messages.success(request, 'Успешно отправлено')
        return redirect('product_detail', rating.product.id)
    
def user_profile_view(request):
    return render(
        request,
        'main/user_profile.html'
    )

def product_payment_create_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    seller_payment_methods = PaymentMethod.objects.filter(user=product.user)
    quantity = 0

    if 'quantity' in request.GET:
        quantity = int(request.GET.get('quantity'))

    if quantity < 1:
        messages.error(request, 'Укажите кол-во')
        return redirect('product_detail', product_id)

    if request.method == 'POST':
        check = request.FILES.get('check', '')
        order = Order(
            user = request.user,
            product = product,
            quantity = quantity,
            check_image = check
            )
        order.save()
        messages.success(request, 'Заявка на оплату отправлено продавцу')

    return redirect(
        request,
        'main/product_payment.html',
        {'seller_payment_methods':seller_payment_methods}
        )

def product_list_view(request):
    queryset = Product.objects.filter(is_active=True)

    if 'product_search' in request.GET:
        product_name = request.GET.get('product_search')
        queryset = queryset.filter(title_icontains=product_name)

    products = ProductListFilter(request.GET, queryset=queryset)
   
   #Paginator
    paginator = Paginator(products.qs, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/product_list.html', {'page_obj': page_obj})