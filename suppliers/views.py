from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Product, NoteBookEntry, Supplier
from spending.models import ProductSpendingMonthly, ProductSpendingYearly, SupplierSpendingMonthly, SupplierSpendingYearly

def home_page(request):
    return render(request, "suppliers/home.html")

def notebook_page(request):
    if request.method == "POST":
        
        action = request.POST.get("action")
        quantity_str = request.POST.get("quantity")
        prod_name = request.POST.get("product_name")

        if action == "add":
            if not prod_name or not quantity_str:
                return redirect("notebook")
            
            try:
                qty = float(quantity_str)
            except Exception:
                return redirect("notebook")
            
            if qty <= 0:
                return redirect("notebook")

            product = get_object_or_404(Product, name=prod_name)

            entry, _ = NoteBookEntry.objects.get_or_create(product=product, defaults={"quantity": 0.1})
            entry.quantity = qty
            entry.save()
        
        elif action == "delete":
            if not prod_name:
                return redirect("notebook")

            for entry in NoteBookEntry.objects.all():
                if entry.product.name == prod_name:
                    entry.delete()


        return redirect("notebook")
    
    all_products = Product.objects.order_by("name")
    notebook_entries = NoteBookEntry.objects.select_related("product").order_by("-created_at")

    context = {
        "all_products": all_products,
        "notebook_entries": notebook_entries,
    }
    return render(request, "suppliers/notebook.html", context)
    
def add_product_view(request):
    if request.method == "POST":

        action = request.POST.get("action")
        product_name = (request.POST.get("product-name"))
        unit = request.POST.get("unit")
        price = request.POST.get("price")
        supplier = (request.POST.get("supplier"))


        if action == "add":
            try:
                price = float(price)
                if Product.objects.filter(name=product_name).exists():
                    return redirect("add-product")
                else:
                    if Supplier.objects.filter(name=supplier).exists():
                        Product.objects.create(
                            name=product_name,
                            unit=unit,
                            price_per_unit=price,
                            supplier=Supplier.objects.get(name=supplier)
                        )
                        return redirect("add-product")
                    else: return redirect("add-product")
            except:
                return redirect("add-product")
            
        elif action == "delete":
            if product_name:
                Product.objects.filter(name=product_name).delete()
                return redirect("add-product")
            
        elif action == "update":
            try:
                price = float(price)
                if product_name and Product.objects.filter(name=product_name).exists():
                    product = Product.objects.get(name=product_name)

                    if unit and unit != product.unit:
                        product.unit = unit
                        product.save()
                    
                    if price and price != product.price_per_unit:
                        product.price_per_unit = price
                        product.save()
                    
                    if supplier and supplier != product.supplier.name:
                        if Supplier.objects.filter(name=supplier).exists():
                            product.supplier = Supplier.objects.get(name=supplier)
                            product.save()
            except:
                return redirect("add-product")




    all_products = Product.objects.order_by("name")
    suppliers = Supplier.objects.order_by("name")
    units = [value for value, _ in Product.UNIT_CHOICES]

    context = {
        "all_products": all_products,
        "suppliers": suppliers,
        "units": units,
    }

    return render(request, "suppliers/add_product.html", context)


def add_supplier_view(request):

    if request.method == "POST":
        
        action = request.POST.get("action")
        name = request.POST.get("supplier")
        contact_info = request.POST.get("contact_info")
        order_days = request.POST.getlist("order_days")
        order_time = request.POST.get("order-time")

        if action == "add":
            if Supplier.objects.filter(name=name).exists():
                supplier = Supplier.objects.get(name=name)

                if contact_info and contact_info != supplier.contact_info:
                    supplier.contact_info = contact_info
                    supplier.save()
                
                if len(order_days)>0 and order_days != supplier.order_days:
                    supplier.order_days = order_days
                    supplier.save()
                
                if order_time and order_time != supplier.order_time:
                    supplier.order_time = order_time
                    supplier.save()

                return redirect("suppliers")
            
            if not Supplier.objects.filter(name=name).exists():
                if all([name,contact_info,order_days,order_time]):
                    Supplier.objects.create(
                        name=name,
                        contact_info=contact_info,
                        order_days=order_days,
                        order_time=order_time
                    )
                return redirect("suppliers")
        
        if action == "delete":
            if Supplier.objects.filter(name=name).exists():
                Supplier.objects.filter(name=name).delete()
            return redirect("suppliers")

    suppliers = Supplier.objects.order_by("name")
    days = [day for day, _ in Supplier.WEEKDAY_CHOICES]

    context = {
        "days": days,
        "suppliers": suppliers,
    }

    return render(request, "suppliers/add_suppliers.html", context)


def monthly_expenses(request):

    product_spendings = ProductSpendingMonthly.objects.all().order_by("-year", "-month")
    supplier_spendings = SupplierSpendingMonthly.objects.all().order_by("-year", "-month")

    context = {
        "product_spendings": product_spendings,
        "supplier_spendings": supplier_spendings,
    }

    return render(request, "suppliers/monthly_expenses.html", context)

def yearly_expenses(request):

    product_spendings = ProductSpendingYearly.objects.all().order_by("-year")
    supplier_spendings = SupplierSpendingYearly.objects.all().order_by("-year")

    context = {
        "product_spendings": product_spendings,
        "supplier_spendings": supplier_spendings,
    }

    return render(request, "suppliers/yearly_expenses.html", context)