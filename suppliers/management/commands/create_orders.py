from django.core.management.base import BaseCommand
from suppliers.utils import create_orders

class Command(BaseCommand):
    help = "Send order messages to suppliers and clear notebook entries."

    def handle(self, *args, **kwargs):
        create_orders()
