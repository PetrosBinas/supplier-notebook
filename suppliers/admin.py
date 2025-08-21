from django.contrib import admin
from .models import Supplier, Product, NoteBookEntry

admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(NoteBookEntry)
