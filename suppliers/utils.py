import datetime
from .models import Supplier, NoteBookEntry, Product

def get_due_suppliers():
    time = datetime.datetime.now().time()
    day = datetime.datetime.now().strftime('%A')
    supplier_list = []
    
    for supplier in Supplier.objects.all():
        if day in supplier.order_days and time >= supplier.order_time :
            supplier_list.append(supplier)
    
    return supplier_list
 
def create_orders():
    supplier_list = get_due_suppliers()

    for supplier in supplier_list:
        order_list = []
        for entry in NoteBookEntry.objects.all():
            if entry.product.supplier == supplier:
                order_list.append(entry)
        
        if len(order_list) > 0:
            message = "Hello, Please send:\n"
            for entry in order_list:
                message += f"   - {entry.quantity} {entry.product.unit} {entry.product.name}\n"
            
            send_message(
                method=entry.product.supplier.preferred_method,
                contact=entry.product.supplier.contact_info,
                message=message
            )
           
            for entry in order_list:
                entry.delete()

def send_message(method, contact, message):
    print(f"[{method.upper()}] Sent to {contact}:\n{message}\n")


create_orders()