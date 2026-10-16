
import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from django.http import JsonResponse
from .models import Product

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.db import transaction
from django.db.models import Q, Sum
from django.shortcuts import render, redirect, get_object_or_404

from .models import Customer, Product, SalesInvoice, SalesInvoiceItem


# ============================================================
# LOGIN AND LOGOUT
# ============================================================

def user_login_view(request):
    if request.user.is_authenticated or request.session.get(
        "is_erp_authenticated"
    ):
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            auth_login(request, user)
            request.session["is_erp_authenticated"] = True
            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def user_logout_view(request):
    auth_logout(request)
    request.session.pop("is_erp_authenticated", None)
    return redirect("login")


# ============================================================
# DASHBOARD AND ONE-YEAR CSV SALES GRAPH
# ============================================================

def dashboard_view(request):
    total_customers = Customer.objects.count()
    total_products = Product.objects.count()
    total_invoices = SalesInvoice.objects.count()

    
    total_sales = (
    SalesInvoice.objects.aggregate(
        total=Sum("grand_total")
    )["total"]
    or Decimal("0.00")
)


    recent_invoices = SalesInvoice.objects.select_related(
        "customer"
    ).order_by("-id")[:5]

    sales_labels = []
    sales_values = []
    csv_error = ""

    csv_path = (
        Path(__file__).resolve().parent
        / "one_year_sales_dataset.csv"
    )

    if csv_path.exists():
        try:
            monthly_sales = {}

            with open(
                csv_path,
                "r",
                encoding="utf-8-sig",
                newline="",
            ) as csv_file:
                reader = csv.DictReader(csv_file)

                if not reader.fieldnames:
                    raise ValueError(
                        "The CSV file has no header row."
                    )

                column_map = {
                    column.strip().lower(): column
                    for column in reader.fieldnames
                    if column
                }

                date_column = next(
                    (
                        column_map[name]
                        for name in (
                            "month",
                            "date",
                            "order_date",
                            "sales_date",
                        )
                        if name in column_map
                    ),
                    None,
                )

                amount_column = next(
                    (
                        column_map[name]
                        for name in (
                            "total_sales",
                            "sales",
                            "sales_amount",
                            "revenue",
                        )
                        if name in column_map
                    ),
                    None,
                )

                if not date_column or not amount_column:
                    raise ValueError(
                        "CSV needs a month/date column and a "
                        "total_sales/sales/revenue column."
                    )

                date_formats = (
                    "%Y-%m",
                    "%Y-%m-%d",
                    "%d/%m/%Y",
                    "%m/%d/%Y",
                    "%d-%m-%Y",
                    "%m-%d-%Y",
                    "%Y/%m/%d",
                    "%b %Y",
                    "%B %Y",
                    "%b-%Y",
                    "%B-%Y",
                )

                for row in reader:
                    raw_date = (
                        row.get(date_column) or ""
                    ).strip()

                    raw_amount = (
                        row.get(amount_column) or ""
                    ).strip().replace(",", "").replace("₹", "")

                    if not raw_date or not raw_amount:
                        continue

                    parsed_date = None

                    for date_format in date_formats:
                        try:
                            parsed_date = datetime.strptime(
                                raw_date, date_format
                            )
                            break
                        except ValueError:
                            continue

                    if parsed_date is None:
                        continue

                    try:
                        amount = Decimal(raw_amount)
                    except InvalidOperation:
                        continue

                    if not amount.is_finite():
                        continue

                    month_key = parsed_date.strftime("%Y-%m")
                    monthly_sales[month_key] = (
                        monthly_sales.get(
                            month_key, Decimal("0")
                        ) + amount
                    )

            latest_months = sorted(
                monthly_sales.items()
            )[-12:]

            sales_labels = [
                datetime.strptime(
                    month, "%Y-%m"
                ).strftime("%b %Y")
                for month, _ in latest_months
            ]

            sales_values = [
                float(amount)
                for _, amount in latest_months
            ]

            if not sales_labels:
                csv_error = (
                    "No valid monthly sales rows were found "
                    "in the CSV file."
                )

        except (OSError, csv.Error, ValueError) as exc:
            csv_error = (
                f"Could not read the sales dataset: {exc}"
            )
    else:
        csv_error = (
            f"Sales dataset not found: {csv_path}"
        )

    context = {
        "total_customers": total_customers,
        "total_products": total_products,
        "total_invoices": total_invoices,
        "total_sales": total_sales,
        "recent_invoices": recent_invoices,
        "sales_labels": sales_labels,
        "sales_values": sales_values,
        "csv_error": csv_error,
    }

    return render(request, "dashboard.html", context)


# ============================================================
# CUSTOMER MASTER
# ============================================================

def customer_master_view(request):
    search_query = request.GET.get("q", "").strip()

    customers = Customer.objects.all()

    if search_query:
        customers = customers.filter(
            Q(customer_code__icontains=search_query)
            | Q(customer_name__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(tax_id__icontains=search_query)
        )

    context = {
        "customers": customers,
        "search_query": search_query,
        "total_customers": Customer.objects.count(),
    }

    return render(
        request,
        "customers/customer_master.html",
        context,
    )


def customer_create_view(request):
    if request.method == "POST":
        customer = Customer(
            customer_code=request.POST.get(
                "customer_code", ""
            ).strip(),
            customer_name=request.POST.get(
                "customer_name", ""
            ).strip(),
            tax_id=request.POST.get(
                "tax_id", ""
            ).strip() or None,
            email=request.POST.get(
                "email", ""
            ).strip() or None,
            status=request.POST.get(
                "status", "Active"
            ).strip() or "Active",
        )

        try:
            credit_limit = request.POST.get(
                "credit_limit", "0"
            ).strip()
            customer.credit_limit = Decimal(
                credit_limit or "0"
            )

            customer.full_clean()
            customer.save()

            messages.success(
                request, "Customer added successfully."
            )
            return redirect("customer_master")

        except (InvalidOperation, ValueError):
            messages.error(
                request, "Enter a valid credit limit."
            )
        except Exception as exc:
            messages.error(
                request,
                f"Could not save customer. Check the fields. {exc}",
            )

    return render(
        request,
        "customers/customer_form.html",
        {"customer": None, "page_title": "Add Customer"},
    )


def customer_detail_view(request, customer_id):
    customer = get_object_or_404(
        Customer, id=customer_id
    )

    return render(
        request,
        "customers/customer_detail.html",
        {"customer": customer},
    )


def customer_edit_view(request, customer_id):
    customer = get_object_or_404(
        Customer, id=customer_id
    )

    if request.method == "POST":
        customer.customer_code = request.POST.get(
            "customer_code", ""
        ).strip()
        customer.customer_name = request.POST.get(
            "customer_name", ""
        ).strip()
        customer.tax_id = request.POST.get(
            "tax_id", ""
        ).strip() or None
        customer.email = request.POST.get(
            "email", ""
        ).strip() or None
        customer.status = request.POST.get(
            "status", "Active"
        ).strip() or "Active"

        try:
            customer.credit_limit = Decimal(
                request.POST.get(
                    "credit_limit", "0"
                ).strip() or "0"
            )
            customer.full_clean()
            customer.save()

            messages.success(
                request, "Customer updated successfully."
            )
            return redirect("customer_master")

        except (InvalidOperation, ValueError):
            messages.error(
                request, "Enter a valid credit limit."
            )
        except Exception as exc:
            messages.error(
                request,
                f"Could not update customer. Check the fields. {exc}",
            )

    return render(
        request,
        "customers/customer_form.html",
        {
            "customer": customer,
            "page_title": "Edit Customer",
        },
    )


def customer_delete_view(request, customer_id):
    customer = get_object_or_404(
        Customer, id=customer_id
    )

    if request.method == "POST":
        try:
            customer.delete()
            messages.success(
                request, "Customer deleted successfully."
            )
            return redirect("customer_master")
        except Exception:
            messages.error(
                request,
                "This customer cannot be deleted because "
                "related records may exist.",
            )
            return redirect(
                "customer_detail",
                customer_id=customer.id,
            )

    return render(
        request,
        "customers/customer_confirm_delete.html",
        {"customer": customer},
    )


# ============================================================
# PRODUCT MASTER
# ============================================================

def product_master_view(request):
    search_query = request.GET.get("q", "").strip()

    products = Product.objects.all()

    if search_query:
        products = products.filter(
            Q(product_code__icontains=search_query)
            | Q(product_name__icontains=search_query)
            | Q(category__icontains=search_query)
        )

    context = {
        "products": products,
        "search_query": search_query,
        "total_products": Product.objects.count(),
        "product_count": Product.objects.count(),
        "products_count": Product.objects.count(),
    }

    return render(
        request,
        "products/product_master.html",
        context,
    )


def product_create_view(request):
    if request.method == "POST":
        product = Product(
            product_code=request.POST.get(
                "product_code", ""
            ).strip(),
            product_name=request.POST.get(
                "product_name", ""
            ).strip(),
            category=request.POST.get(
                "category", ""
            ).strip() or None,
            status=request.POST.get(
                "status", "Active"
            ).strip() or "Active",
        )

        try:
            product.unit_price = Decimal(
                request.POST.get(
                    "unit_price", "0"
                ).strip() or "0"
            )
            product.stock_quantity = int(
                request.POST.get(
                    "stock_quantity", "0"
                ).strip() or "0"
            )

            product.full_clean()
            product.save()

            messages.success(
                request, "Product added successfully."
            )
            return redirect("product_master")

        except (InvalidOperation, ValueError):
            messages.error(
                request,
                "Enter a valid unit price and stock quantity.",
            )
        except Exception as exc:
            messages.error(
                request,
                f"Could not save product. Check the fields. {exc}",
            )

    return render(
        request,
        "products/product_form.html",
        {"product": None, "page_title": "Add Product"},
    )


# ============================================================
# SALES INVOICES
# ============================================================

def sales_invoice_view(request):
    search_query = request.GET.get("q", "").strip()

    invoices = SalesInvoice.objects.select_related(
        "customer"
    ).prefetch_related("items__product")

    if search_query:
        invoices = invoices.filter(
            Q(invoice_number__icontains=search_query)
            | Q(customer__customer_name__icontains=search_query)
            | Q(status__icontains=search_query)
        )

    context = {
        "invoices": invoices,
        "sales_invoices": invoices,
        "search_query": search_query,
        "total_invoices": SalesInvoice.objects.count(),
    }

    return render(
        request,
        "invoices/sales_invoice.html",
        context,
    )


def sales_invoice_create_view(request):
    customers = Customer.objects.filter(status="Active")
    products = Product.objects.filter(status="Active")

    if request.method == "POST":
        customer_id = request.POST.get(
            "customer_id"
        ) or request.POST.get("customer")

        if not customer_id:
            messages.error(
                request, "Please select a customer."
            )
            return render(
                request,
                "invoices/sales_invoice_form.html",
                {
                    "customers": customers,
                    "products": products,
                },
            )

        customer = get_object_or_404(
            Customer, pk=customer_id
        )

        # Supports forms submitting one or more product rows.
        product_ids = (
            request.POST.getlist("product_id")
            or request.POST.getlist("product")
        )
        quantities = request.POST.getlist("quantity")

        selected_items = []

        for index, product_id in enumerate(product_ids):
            if not product_id:
                continue

            try:
                quantity = int(
                    quantities[index]
                    if index < len(quantities)
                    else "1"
                )
            except (ValueError, TypeError):
                quantity = 0

            if quantity < 1:
                messages.error(
                    request,
                    "Each item quantity must be at least 1.",
                )
                return render(
                    request,
                    "invoices/sales_invoice_form.html",
                    {
                        "customers": customers,
                        "products": products,
                    },
                )

            product = get_object_or_404(
                Product, pk=product_id
            )
            selected_items.append((product, quantity))

        if not selected_items:
            messages.error(
                request, "Please select at least one product."
            )
            return render(
                request,
                "invoices/sales_invoice_form.html",
                {
                    "customers": customers,
                    "products": products,
                },
            )

        try:
            tax_rate = Decimal(
                request.POST.get(
                    "tax_rate", "0"
                ).strip() or "0"
            )

            if not tax_rate.is_finite() or tax_rate < 0:
                raise InvalidOperation

            status = request.POST.get(
                "status", "Pending"
            ).strip()

            valid_statuses = {
                choice[0]
                for choice in SalesInvoice.STATUS_CHOICES
            }
            if status not in valid_statuses:
                status = "Pending"

            with transaction.atomic():
                invoice = SalesInvoice.objects.create(
                    customer=customer,
                    tax_rate=tax_rate,
                    status=status,
                )

                subtotal = Decimal("0.00")

                for product, quantity in selected_items:
                    line_total = (
                        product.unit_price * quantity
                    )
                    subtotal += line_total

                    SalesInvoiceItem.objects.create(
                        invoice=invoice,
                        product=product,
                        quantity=quantity,
                        unit_price=product.unit_price,
                        line_total=line_total,
                    )

                tax_amount = (
                    subtotal * tax_rate / Decimal("100")
                ).quantize(Decimal("0.01"))

                invoice.subtotal = subtotal
                invoice.tax_amount = tax_amount
                invoice.grand_total = subtotal + tax_amount
                invoice.save(
                    update_fields=[
                        "subtotal",
                        "tax_amount",
                        "grand_total",
                    ]
                )

            messages.success(
                request,
                f"Invoice {invoice.invoice_number} created successfully.",
            )
            return redirect(
                "sales_invoice_detail",
                invoice_id=invoice.id,
            )

        except (InvalidOperation, ValueError):
            messages.error(
                request, "Please enter a valid tax rate."
            )
        except Exception as exc:
            messages.error(
                request,
                f"Could not create invoice: {exc}",
            )

    return render(
        request,
        "invoices/sales_invoice_form.html",
        {
            "customers": customers,
            "products": products,
        },
    )


context = {
    "customers": Customer.objects.all(),
    "products": Product.objects.filter(status="Active"),
}


def sales_invoice_detail_view(request, invoice_id):
    invoice = get_object_or_404(
        SalesInvoice.objects.select_related(
            "customer"
        ).prefetch_related("items__product"),
        id=invoice_id,
    )

    return render(
        request,
        "invoices/sales_invoice_detail.html",
        {"invoice": invoice},
    )


def sales_invoice_delete_view(request, invoice_id):
    invoice = get_object_or_404(
        SalesInvoice, id=invoice_id
    )

    if request.method == "POST":
        invoice.delete()
        messages.success(
            request, "Invoice deleted successfully."
        )
        return redirect("sales_invoice")

    return render(
        request,
        "invoices/sales_invoice_confirm_delete.html",
        {"invoice": invoice},
    )

def get_product_price_view(request, product_id):
    if request.method != "GET":
        return JsonResponse(
            {"success": False, "message": "Invalid request."},
            status=405,
        )

    try:
        product = Product.objects.get(
            pk=product_id,
            status="Active",
        )

        return JsonResponse({
            "success": True,
            "product_id": product.pk,
            "product_name": product.product_name,
            "unit_price": str(product.unit_price),
        })

    except Product.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Product not found or inactive.",
        }, status=404)
