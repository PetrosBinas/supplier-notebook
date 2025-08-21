from celery import shared_task
from .models import Supplier, NoteBookEntry
from spending.models import ProductSpendingMonthly
import datetime
from suppliers.gmail_messaging.gmail import GmailSender
from decimal import Decimal

now = datetime.datetime.now()
cur_month = now.month
cur_year = now.year


@shared_task
def create_orders_task():
    time = datetime.datetime.now().time()
    day = datetime.datetime.now().strftime('%A')
    supplier_list = []
    
    for supplier in Supplier.objects.all():
        if day in supplier.order_days and time >= supplier.order_time :
            supplier_list.append(supplier)
    
    if len(supplier_list) > 0:
        create_orders(supplier_list)
    
def create_orders(supplier_list):

    for supplier in supplier_list:
        order_list = []
        for entry in NoteBookEntry.objects.all():
            if entry.product.supplier == supplier:
                order_list.append(entry)
        
        if len(order_list) > 0:
            message = "Hello! Please send the following items:\n"
            for entry in order_list:
                message += f"   - {entry.quantity} {entry.product.unit} {entry.product.name}\n"
            
            
            GmailSender.send_gmail(
                contact=entry.product.supplier.contact_info,
                message_info=message,
                subject=f"Order for {supplier.name}"
            )
            
            for entry in order_list:
                spending, _ = ProductSpendingMonthly.objects.get_or_create(
                    product = entry.product ,
                    month = cur_month , 
                    year = cur_year ,
                    defaults = {"cost": Decimal("0.00")}
                )
                spending.cost += Decimal(entry.quantity) * entry.product.price_per_unit
                spending.save(update_fields=["cost"])
                
                print(f"for {entry.product.name} new monthly for {spending.month}/{spending.year} month/year cost is calculated to {spending.cost} $ of spending")
                
            for entry in order_list:
                entry.delete()
