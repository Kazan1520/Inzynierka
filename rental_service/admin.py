from django.contrib import admin
from rental_service.models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Rental)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(SafeConduct)

