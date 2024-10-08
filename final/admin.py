from django.contrib import admin
from .models import product , UserProfile ,ProductImage , data ,samedata ,thirddata,forthdata,cartitem,Order,OrderItem,ProductReview

class adminuserprofile(admin.ModelAdmin):
    list_display=('user','email','is_approved')
admin.site.register(UserProfile,adminuserprofile)

class adminproduct(admin.ModelAdmin):
    list_display=('p_name','color','price','detail','is_approved','user')
admin.site.register(product,adminproduct)

class adminProductImage(admin.ModelAdmin):
    list_display=('product','image')
admin.site.register(ProductImage,adminProductImage)

class admindata(admin.ModelAdmin):
    list_display=('name','username','email')
admin.site.register(data,admindata)

class adminsavedata(admin.ModelAdmin):
    list_display=('name','username','email')
admin.site.register(samedata,adminsavedata)

class adminthird(admin.ModelAdmin):
    list_display=('name','username','email')
admin.site.register(thirddata,adminthird)

class adminforthdata(admin.ModelAdmin):
    list_display=()
admin.site.register(forthdata,adminforthdata)

class adminCartItem(admin.ModelAdmin):
    list_display=('product_id','user','product','quantity','total_price','added_at')
admin.site.register(cartitem,adminCartItem)

class adminOrder(admin.ModelAdmin):
    list_display=('user','total_amount','order_date','mobile','address')
admin.site.register(Order,adminOrder)

class adminOrderItem(admin.ModelAdmin):
    list_display=('order','product','quantity','total_price','order_status')
admin.site.register(OrderItem,adminOrderItem)

class adminProductReview(admin.ModelAdmin):
    list_display=('user','product','review_text','review_rating','images')
admin.site.register(ProductReview,adminProductReview)


# Register your models here.

