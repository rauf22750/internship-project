"""djangocrud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from final import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcomepage, name='home'),
    path('signup/', views.signaction, name='Signup'),
    path('accounts/login/', views.loginuser, name='login'),
    path('signout/', views.signout, name='signout'),
    path('productadd/', views.productadd, name='productadd'),
    path('productlist/', views.productlist, name='productlist'),
    path('productdetail/<str:id>/', views.productdetail, name='productdetail'),
    path('product/update/<str:signed_product_id>/', views.productupdate, name='productupdate'),
    path('productdelete/', views.productdelete, name='productdelete'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('order/',views.order,name='order'),
    # path('order-success/', views.order_success, name='order_success'),
    path('vendor/orders/', views.vendor_orders, name='vendor_orders'),
    path('order/update-status/<int:item_id>/', views.update_item_status, name='update_item_status'),
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),




    # path('product/',views.product, name='product'),
    #path('',views.info ,name='data'),
    #path('',views.info,name='data')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Uncomment if needed
    # path('delete/<int:id>', views.Delete_record, name='delete'),
    # path('info/<int:id>', views.info_detail, name='info'),
    # path('category/', views.category, name='category'),
    # path('categoryadd/', views.categoryadd, name='categoryadd'),



