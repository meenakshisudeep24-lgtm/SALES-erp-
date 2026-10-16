
from decimal import Decimal

from django.db import models


class Customer(models.Model):
    customer_code = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=200)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    credit_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    status = models.CharField(max_length=20, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer_code} - {self.customer_name}'

    class Meta:
        ordering = ['-id']


class Product(models.Model):
    product_code = models.CharField(max_length=20, unique=True)
    product_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True, null=True)
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product_code} - {self.product_name}'

    class Meta:
        ordering = ['-id']


class SalesInvoice(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
    ]

    invoice_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='sales_invoices'
    )

    invoice_date = models.DateField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00')
    )

    subtotal = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00')
    )

    tax_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00')
    )

    grand_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00')
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Save first to obtain a unique database ID.
            super().save(*args, **kwargs)

            self.invoice_number = f'INV-{self.pk:05d}'

            super().save(update_fields=['invoice_number'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number or 'New Sales Invoice'

    class Meta:
        ordering = ['-id']


class SalesInvoiceItem(models.Model):
    invoice = models.ForeignKey(
        SalesInvoice,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='invoice_items'
    )

    quantity = models.PositiveIntegerField(default=1)

    # Saves the product price at the time of the sale.
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    line_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00')
    )

    def save(self, *args, **kwargs):
        self.line_total = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f'{self.invoice.invoice_number} - '
            f'{self.product.product_name}'
        )

    class Meta:
        ordering = ['id']
