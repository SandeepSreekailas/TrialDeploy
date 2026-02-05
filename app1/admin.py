from django.contrib import admin
from .models import Book, Cart

# Register your models here.

# class ShowBook(admin.ModelAdmin):
#     list_display=['title','author','description','price','published_date','cover']
#     list_filter=['title', 'price']
#     list_editable=['price']
#     #searching
#     search_fields=['title','author']
#     #sorting
#     list_per_page=5



class ShowBook(admin.ModelAdmin):
    list_display=['title','author','description','price','published_date','cover']

    actions=['Mark_Free']

    def Mark_Free(self, request, queryset):
        queryset.update(price=0)
        self.message_user(request, "Selected books marked as free.")
    Mark_Free.short_description="Make as free"
    

admin.site.register(Book,ShowBook)
admin.site.register(Cart)