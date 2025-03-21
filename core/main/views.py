from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.contrib import messages
from django.db.models import Avg, Sum
from django.core.paginator import Paginator

from .forms import ProductCreateForm, ProductUpdateForm
from .filters import ProductListFilter
from .models import Product, Rating, RatingAnswer, PaymentMethod, PaymentRequest, Category, Payment


def index_view(request):
    products = Product.objects.filter(is_active=True)

    return render(request, 'main/index.html', {"products": products})


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_update_form = ProductUpdateForm(instance=product)
    product_comments = Rating.objects.filter(product=product)

    rating_avg = product_comments.aggregate(Avg('count'))['count__avg']
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)

    return render(
        request=request,
        template_name='main/product_detail.html',
        context={
            "product": product,
            "similar_products": similar_products,
            "product_update_form": product_update_form,
            "product_comments": product_comments,
            "rating_avg": rating_avg
        })


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
    return render(request, 'main/product_create.html', {"form": form})


def product_update_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

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
    payment_requests = PaymentRequest.objects.filter(product__user=request.user, status='in_processing').order_by('-id')[:3]

    return render(
        request=request,
        template_name='main/user_profile.html',
        context={
            'payment_requests': payment_requests
        }
    )


def product_payment_create_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    seller_payment_methods = PaymentMethod.objects.filter(user=product.user)

    if request.method == 'POST':
        check = request.FILES.get('check', '')
        quantity = request.POST.get('quantity')

        total_price = Decimal(quantity) * product.price

        order = PaymentRequest(
            user=request.user,
            product=product,
            quantity=quantity,
            check_image=check,
            total_price=total_price
        )
        order.save()
        messages.success(request, 'Заявку на оплату отправлена продавцу')
        return redirect('index')

    return render(
        request=request,
        template_name='main/product_payment.html',
        context={
            "seller_payment_methods": seller_payment_methods
        }
    )


def product_list_view(request):
    queryset = Product.objects.filter(is_active=True)

    if 'product_search' in request.GET:
        product_name = request.GET.get("product_search")
        queryset = queryset.filter(title__icontains=product_name)

    products = ProductListFilter(request.GET, queryset=queryset)

    # Paginator
    paginator = Paginator(products.qs, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/product_list.html', {'page_obj': page_obj, 'products': products})


def payment_request_list_view(request):
    payment_requests = PaymentRequest.objects.filter(product__user=request.user).order_by('-id')

    return render(
        request=request,
        template_name='main/payment_request.html',
        context={
            'payment_requests': payment_requests
        }
    )


def payment_request_update_status(request, payment_request_id):
    payment_request = get_object_or_404(PaymentRequest, id=payment_request_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        payment_request.status = status
        payment_request.save()

        if payment_request.status == 'accepted':

            payment = Payment(
                seller=payment_request.product.user,
                user=payment_request.user.first_name,
                product=payment_request.product.title,
                quantity=payment_request.quantity,
                check_image=payment_request.check_image,
                total_price=payment_request.total_price
            )
            payment.save()

        messages.success(request, 'Успешно изменено')

    return redirect('payment_requests')

def payment_list_view(request):
    payments = Payment.objects.filter(seller=request.user)

    total_payments = payments.aggregate(Sum('total_price'))['total_price__sum']

    return render(
        request=request,
        template_name='main/payments.html',
        context={
            "payments": payments,
            "total_payments": total_payments
        }
    )