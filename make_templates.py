import os

# Create template directory
os.makedirs('sales_app/templates', exist_ok=True)

# 1. BASE TEMPLATE
base_html = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}SalesERP - 1-Year Sales Management{% endblock %}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: { 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca' }
          }
        }
      }
    }
  </script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex font-sans antialiased">

  <!-- Sidebar -->
  <aside class="w-64 bg-slate-900 border-r border-slate-800 flex flex-col fixed inset-y-0 z-50">
    <div class="h-16 flex items-center px-6 border-b border-slate-800 gap-3">
      <div class="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/30">
        <i class="fa-solid fa-chart-line text-lg"></i>
      </div>
      <div>
        <h1 class="font-bold text-base tracking-wide text-white">Sales<span class="text-indigo-400">ERP</span></h1>
        <p class="text-[10px] text-slate-400 font-medium tracking-wider uppercase">Enterprise Edition</p>
      </div>
    </div>

    <!-- Navigation links -->
    <nav class="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
      <a href="/" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition text-indigo-400 bg-indigo-500/10 border border-indigo-500/20">
        <i class="fa-solid fa-gauge w-5 text-center"></i> 1-Year Analytics
      </a>
      <a href="/customers/" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-400 hover:text-white hover:bg-slate-800/60 transition">
        <i class="fa-solid fa-users w-5 text-center"></i> Customers Master
      </a>
      <a href="/products/" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-400 hover:text-white hover:bg-slate-800/60 transition">
        <i class="fa-solid fa-box-archive w-5 text-center"></i> Product Master
      </a>
      <a href="/sales/new/" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-400 hover:text-white hover:bg-slate-800/60 transition">
        <i class="fa-solid fa-file-invoice-dollar w-5 text-center"></i> New Sales Invoice
      </a>
    </nav>

    <!-- User Section -->
    <div class="p-4 border-t border-slate-800 bg-slate-900/60">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-sm font-bold text-indigo-400">
            MS
          </div>
          <div>
            <p class="text-xs font-semibold text-white">Meenakshi</p>
            <p class="text-[10px] text-emerald-400 font-medium">Sales Administrator</p>
          </div>
        </div>
        <a href="/login/" class="text-slate-400 hover:text-rose-400 text-sm p-1.5 rounded-lg transition" title="Logout">
          <i class="fa-solid fa-arrow-right-from-bracket"></i>
        </a>
      </div>
    </div>
  </aside>

  <!-- Main Content Area -->
  <main class="flex-1 ml-64 p-8 min-h-screen bg-slate-950">
    {% block content %}{% endblock %}
  </main>

  {% block scripts %}{% endblock %}
</body>
</html>"""

# 2. DASHBOARD TEMPLATE (1-YEAR ANALYTICS)
dashboard_html = """{% extends 'base.html' %}
{% block title %}Dashboard - 1-Year Sales ERP{% endblock %}

{% block content %}
<div class="space-y-8">
  <!-- Top Header -->
  <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
    <div>
      <h2 class="text-2xl font-bold text-white tracking-tight">1-Year Sales & Revenue Analytics</h2>
      <p class="text-sm text-slate-400 mt-1">Full 12-month performance overview, annual totals, and recent customer invoices.</p>
    </div>
    <div class="flex items-center gap-3">
      <button class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-semibold flex items-center gap-2 transition">
        <i class="fa-solid fa-download"></i> Export Annual Report
      </button>
      <a href="/sales/new/" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-indigo-600/30 flex items-center gap-2 transition">
        <i class="fa-solid fa-plus"></i> Create Invoice
      </a>
    </div>
  </div>

  <!-- KPI Cards -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
    <div class="p-5 rounded-xl bg-slate-900 border border-slate-800 shadow-sm">
      <div class="flex items-center justify-between">
        <span class="text-xs font-medium text-slate-400 uppercase tracking-wider">Annual Revenue</span>
        <div class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center text-sm"><i class="fa-solid fa-dollar-sign"></i></div>
      </div>
      <p class="text-2xl font-bold text-white mt-3">$1,482,900</p>
      <p class="text-xs text-emerald-400 mt-2 font-medium flex items-center gap-1">
        <i class="fa-solid fa-arrow-trend-up"></i> +18.4% vs previous year
      </p>
    </div>

    <div class="p-5 rounded-xl bg-slate-900 border border-slate-800 shadow-sm">
      <div class="flex items-center justify-between">
        <span class="text-xs font-medium text-slate-400 uppercase tracking-wider">Total Invoices</span>
        <div class="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center text-sm"><i class="fa-solid fa-file-invoice"></i></div>
      </div>
      <p class="text-2xl font-bold text-white mt-3">2,845</p>
      <p class="text-xs text-indigo-400 mt-2 font-medium flex items-center gap-1">
        <i class="fa-solid fa-check"></i> 96.2% payment completion
      </p>
    </div>

    <div class="p-5 rounded-xl bg-slate-900 border border-slate-800 shadow-sm">
      <div class="flex items-center justify-between">
        <span class="text-xs font-medium text-slate-400 uppercase tracking-wider">Avg Order Value</span>
        <div class="w-8 h-8 rounded-lg bg-sky-500/10 text-sky-400 flex items-center justify-center text-sm"><i class="fa-solid fa-basket-shopping"></i></div>
      </div>
      <p class="text-2xl font-bold text-white mt-3">$521.23</p>
      <p class="text-xs text-sky-400 mt-2 font-medium flex items-center gap-1">
        <i class="fa-solid fa-arrow-trend-up"></i> +6.8% expansion
      </p>
    </div>

    <div class="p-5 rounded-xl bg-slate-900 border border-slate-800 shadow-sm">
      <div class="flex items-center justify-between">
        <span class="text-xs font-medium text-slate-400 uppercase tracking-wider">Active Customers</span>
        <div class="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center text-sm"><i class="fa-solid fa-building-user"></i></div>
      </div>
      <p class="text-2xl font-bold text-white mt-3">348</p>
      <p class="text-xs text-amber-400 mt-2 font-medium flex items-center gap-1">
        <i class="fa-solid fa-plus"></i> 42 onboarded this quarter
      </p>
    </div>
  </div>

  <!-- 1-Year Interactive Sales Chart -->
  <div class="p-6 rounded-xl bg-slate-900 border border-slate-800 shadow-sm">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h3 class="font-bold text-white text-base">12-Month Sales & Profit Trajectory</h3>
        <p class="text-xs text-slate-400">Monthly breakdown for January through December</p>
      </div>
      <span class="px-3 py-1 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold rounded-full">
        Current Financial Year
      </span>
    </div>
    <div class="h-80">
      <canvas id="salesYearChart"></canvas>
    </div>
  </div>

  <!-- Recent Invoices Table -->
  <div class="p-6 rounded-xl bg-slate-900 border border-slate-800 shadow-sm">
    <div class="flex items-center justify-between mb-4">
      <h3 class="font-bold text-white text-base">Recent Sales Invoices</h3>
      <a href="/sales/new/" class="text-xs text-indigo-400 hover:text-indigo-300 font-semibold">View All Invoices &rarr;</a>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full text-left text-sm text-slate-300">
        <thead class="bg-slate-800/60 text-slate-400 text-xs uppercase font-semibold">
          <tr>
            <th class="py-3 px-4">Invoice #</th>
            <th class="py-3 px-4">Customer</th>
            <th class="py-3 px-4">Date</th>
            <th class="py-3 px-4">Amount</th>
            <th class="py-3 px-4">Status</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800">
          <tr class="hover:bg-slate-800/40">
            <td class="py-3 px-4 font-mono font-medium text-indigo-400">INV-2026-0891</td>
            <td class="py-3 px-4 font-medium text-white">Apex Global Logistics</td>
            <td class="py-3 px-4 text-xs text-slate-400">Oct 12, 2026</td>
            <td class="py-3 px-4 font-semibold text-white">$14,250.00</td>
            <td class="py-3 px-4"><span class="px-2.5 py-1 text-xs rounded-full bg-emerald-500/10 text-emerald-400 font-semibold border border-emerald-500/20">Paid</span></td>
          </tr>
          <tr class="hover:bg-slate-800/40">
            <td class="py-3 px-4 font-mono font-medium text-indigo-400">INV-2026-0890</td>
            <td class="py-3 px-4 font-medium text-white">Quantum Tech Solutions</td>
            <td class="py-3 px-4 text-xs text-slate-400">Oct 11, 2026</td>
            <td class="py-3 px-4 font-semibold text-white">$8,620.00</td>
            <td class="py-3 px-4"><span class="px-2.5 py-1 text-xs rounded-full bg-amber-500/10 text-amber-400 font-semibold border border-amber-500/20">Pending</span></td>
          </tr>
          <tr class="hover:bg-slate-800/40">
            <td class="py-3 px-4 font-mono font-medium text-indigo-400">INV-2026-0889</td>
            <td class="py-3 px-4 font-medium text-white">Silverline Retailers</td>
            <td class="py-3 px-4 text-xs text-slate-400">Oct 09, 2026</td>
            <td class="py-3 px-4 font-semibold text-white">$21,400.00</td>
            <td class="py-3 px-4"><span class="px-2.5 py-1 text-xs rounded-full bg-emerald-500/10 text-emerald-400 font-semibold border border-emerald-500/20">Paid</span></td>
          </tr>
          <tr class="hover:bg-slate-800/40">
            <td class="py-3 px-4 font-mono font-medium text-indigo-400">INV-2026-0888</td>
            <td class="py-3 px-4 font-medium text-white">Nexus Enterprises</td>
            <td class="py-3 px-4 text-xs text-slate-400">Oct 07, 2026</td>
            <td class="py-3 px-4 font-semibold text-white">$5,130.00</td>
            <td class="py-3 px-4"><span class="px-2.5 py-1 text-xs rounded-full bg-emerald-500/10 text-emerald-400 font-semibold border border-emerald-500/20">Paid</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
{% endblock %}

{% block scripts %}
<script>
  const ctx = document.getElementById('salesYearChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      datasets: [
        {
          label: 'Revenue ($)',
          data: [95000, 105000, 118000, 112000, 126000, 134000, 129000, 142000, 139000, 151000, 168000, 185000],
          backgroundColor: 'rgba(99, 102, 241, 0.85)',
          borderRadius: 6,
        },
        {
          type: 'line',
          label: 'Net Profit ($)',
          data: [38000, 42000, 49000, 44000, 52000, 58000, 53000, 62000, 60000, 68000, 77000, 89000],
          borderColor: '#10b981',
          borderWidth: 3,
          tension: 0.35,
          fill: false,
          pointBackgroundColor: '#10b981',
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#94a3b8', font: { size: 12 } } }
      },
      scales: {
        x: { grid: { color: 'rgba(51, 65, 85, 0.3)' }, ticks: { color: '#94a3b8' } },
        y: { grid: { color: 'rgba(51, 65, 85, 0.3)' }, ticks: { color: '#94a3b8' } }
      }
    }
  });
</script>
{% endblock %}"""

# 3. CUSTOMERS MASTER TEMPLATE
customers_html = """{% extends 'base.html' %}
{% block title %}Customer Master - Sales ERP{% endblock %}

{% block content %}
<div class="space-y-6">
  <div class="flex items-center justify-between">
    <div>
      <h2 class="text-2xl font-bold text-white tracking-tight">Customer Master</h2>
      <p class="text-sm text-slate-400 mt-1">Directory of accounts, commercial terms, credit limits, and contact points.</p>
    </div>
    <button class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-indigo-600/30 flex items-center gap-2">
      <i class="fa-solid fa-user-plus"></i> Add New Customer
    </button>
  </div>

  <div class="p-5 rounded-xl bg-slate-900 border border-slate-800">
    <div class="overflow-x-auto">
      <table class="w-full text-left text-sm text-slate-300">
        <thead class="bg-slate-800/60 text-slate-400 text-xs uppercase font-semibold">
          <tr>
            <th class="py-3 px-4">Account ID</th>
            <th class="py-3 px-4">Company Name</th>
            <th class="py-3 px-4">Contact Person</th>
            <th class="py-3 px-4">Credit Limit</th>
            <th class="py-3 px-4">Outstanding</th>
            <th class="py-3 px-4">Tier</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800">
          <tr class="hover:bg-slate-800/40">
            <td class="py-3 px-4 font-mono text-indigo-400">CUST-1001</td>
            <td class="py-3 px-4 font-bold text-white">Apex Global Logistics</td>
            <td class="py-3 px-4 text-slate-400">David Miller (david@apex.com)</td>
            <td class="py-3 px-4 font-medium text-white">$100,000</td>
            <td class="py-3 px-4 text-emerald-400 font-semibold">$14,250</td>
            <td class="py-3 px-4"><span class="px-2.5 py-0.5 rounded-full text-xs bg-indigo-500/20 text-indigo-400 font-semibold">Enterprise</span></td>
          </tr>
          <tr class="hover:bg-slate-800/40">
            <td class="py-3 px-4 font-mono text-indigo-400">CUST-1002</td>
            <td class="py-3 px-4 font-bold text-white">Quantum Tech Solutions</td>
            <td class="py-3 px-4 text-slate-400">Sarah Jenkins (sarah@qtech.io)</td>
            <td class="py-3 px-4 font-medium text-white">$50,000</td>
            <td class="py-3 px-4 text-amber-400 font-semibold">$8,620</td>
            <td class="py-3 px-4"><span class="px-2.5 py-0.5 rounded-full text-xs bg-sky-500/20 text-sky-400 font-semibold">Mid-Market</span></td>
          </tr>
          <tr class="hover:bg-slate-800/40">
            <td class="py-3 px-4 font-mono text-indigo-400">CUST-1003</td>
            <td class="py-3 px-4 font-bold text-white">Silverline Retailers</td>
            <td class="py-3 px-4 text-slate-400">Alex Reed (alex@silverline.com)</td>
            <td class="py-3 px-4 font-medium text-white">$150,000</td>
            <td class="py-3 px-4 text-emerald-400 font-semibold">$0</td>
            <td class="py-3 px-4"><span class="px-2.5 py-0.5 rounded-full text-xs bg-indigo-500/20 text-indigo-400 font-semibold">Enterprise</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
{% endblock %}"""

# 4. PRODUCTS MASTER TEMPLATE
products_html = """{% extends 'base.html' %}
{% block title %}Product Master - Sales ERP{% endblock %}

{% block content %}
<div class="space-y-6">
  <div class="flex items-center justify-between">
    <div>
      <h2 class="text-2xl font-bold text-white tracking-tight">Product Master</h2>
      <p class="text-sm text-slate-400 mt-1">Item catalog, SKU management, list pricing, and warehouse inventory.</p>
    </div>
    <button class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-indigo-600/30 flex items-center gap-2">
      <i class="fa-solid fa-plus"></i> Add Product
    </button>
  </div>

  <div class="p-5 rounded-xl bg-slate-900 border border-slate-800">
    <div class="overflow-x-auto">
      <table class="w-full text-left text-sm text-slate-300">
        <thead class="bg-slate-800/60 text-slate-400 text-xs uppercase font-semibold">
          <tr>
            <th class="py-3 px-4">SKU</th>
            <th class="py-3 px-4">Product Name</th>
            <th class="py-3 px-4">Category</th>
            <th class="py-3 px-4">Unit Price</th>
            <th class="py-3 px-4">Stock Level</th>
            <th class="py-3 px-4">Status</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800">
          <tr class="hover:bg-slate-800/40">
            <td class="py-3 px-4 font-mono text-indigo-400">PRD-CORE-01</td>
            <td class="py-3 px-4 font-bold text-white">Enterprise Database Server Rack</td>
            <td class="py-3 px-4 text-slate-400">Hardware</td>
            <td class="py-3 px-4 font-medium text-white">$4,850.00</td>
            <td class="py-3 px-4 text-emerald-400 font-semibold">32 Units</td>
            <td class="py-3 px-4"><span class="px-2.5 py-0.5 rounded-full text-xs bg-emerald-500/20 text-emerald-400 font-semibold">In Stock</span></td>
          </tr>
          <tr class="hover:bg-slate-800/40">
            <td class="py-3 px-4 font-mono text-indigo-400">PRD-LIC-02</td>
            <td class="py-3 px-4 font-bold text-white">Annual Cloud ERP Subscription</td>
            <td class="py-3 px-4 text-slate-400">SaaS License</td>
            <td class="py-3 px-4 font-medium text-white">$1,200.00</td>
            <td class="py-3 px-4 text-slate-400 font-semibold">Unlimited</td>
            <td class="py-3 px-4"><span class="px-2.5 py-0.5 rounded-full text-xs bg-emerald-500/20 text-emerald-400 font-semibold">Active</span></td>
          </tr>
          <tr class="hover:bg-slate-800/40">
            <td class="py-3 px-4 font-mono text-indigo-400">PRD-SRV-03</td>
            <td class="py-3 px-4 font-bold text-white">Implementation & Integration Pack</td>
            <td class="py-3 px-4 text-slate-400">Consulting</td>
            <td class="py-3 px-4 font-medium text-white">$3,500.00</td>
            <td class="py-3 px-4 text-amber-400 font-semibold">14 Slots</td>
            <td class="py-3 px-4"><span class="px-2.5 py-0.5 rounded-full text-xs bg-amber-500/20 text-amber-400 font-semibold">Limited</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
{% endblock %}"""

# 5. NEW INVOICE TEMPLATE
sales_form_html = """{% extends 'base.html' %}
{% block title %}Create Invoice - Sales ERP{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto space-y-6">
  <div>
    <h2 class="text-2xl font-bold text-white tracking-tight">Create Sales Invoice</h2>
    <p class="text-sm text-slate-400 mt-1">Issue a new commercial invoice, specify items, and track receivables.</p>
  </div>

  <div class="p-6 rounded-xl bg-slate-900 border border-slate-800 shadow-sm space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-xs font-semibold text-slate-300 uppercase mb-2">Customer Account</label>
        <select class="w-full bg-slate-800 border border-slate-700 text-white rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500">
          <option>Apex Global Logistics (CUST-1001)</option>
          <option>Quantum Tech Solutions (CUST-1002)</option>
          <option>Silverline Retailers (CUST-1003)</option>
        </select>
      </div>
      <div>
        <label class="block text-xs font-semibold text-slate-300 uppercase mb-2">Invoice Date</label>
        <input type="date" value="2026-10-13" class="w-full bg-slate-800 border border-slate-700 text-white rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500">
      </div>
    </div>

    <div>
      <label class="block text-xs font-semibold text-slate-300 uppercase mb-2">Product Line Item</label>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <select class="w-full bg-slate-800 border border-slate-700 text-white rounded-lg px-3 py-2 text-sm">
          <option>PRD-CORE-01: Enterprise Server Rack ($4,850)</option>
          <option>PRD-LIC-02: Annual ERP License ($1,200)</option>
          <option>PRD-SRV-03: Implementation Pack ($3,500)</option>
        </select>
        <input type="number" value="1" min="1" placeholder="Quantity" class="w-full bg-slate-800 border border-slate-700 text-white rounded-lg px-3 py-2 text-sm">
        <input type="text" value="$4,850.00" readonly class="w-full bg-slate-800/50 border border-slate-700 text-slate-400 rounded-lg px-3 py-2 text-sm">
      </div>
    </div>

    <div class="flex justify-end gap-3 pt-4 border-t border-slate-800">
      <a href="/" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-sm font-semibold transition">Cancel</a>
      <button type="button" class="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-semibold shadow-lg shadow-indigo-600/30 transition">Issue Invoice</button>
    </div>
  </div>
</div>
{% endblock %}"""

# 6. LOGIN TEMPLATE
login_html = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <title>Login - Sales ERP</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>
<body class="bg-slate-950 flex items-center justify-center min-h-screen p-4">
  <div class="w-full max-w-md p-8 bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl">
    <div class="text-center mb-8">
      <div class="w-12 h-12 mx-auto rounded-xl bg-indigo-600 flex items-center justify-center text-white text-xl shadow-lg shadow-indigo-600/30 mb-3">
        <i class="fa-solid fa-chart-line"></i>
      </div>
      <h1 class="text-2xl font-bold text-white tracking-wide">Sales<span class="text-indigo-400">ERP</span></h1>
      <p class="text-xs text-slate-400 mt-1">Sign in to your Enterprise Sales Portal</p>
    </div>

    <form method="POST" action="/login/" class="space-y-4">
      <div>
        <label class="block text-xs font-semibold text-slate-400 uppercase mb-2">Username</label>
        <input type="text" name="username" value="admin" required class="w-full px-3.5 py-2.5 bg-slate-800 border border-slate-700 text-white rounded-lg text-sm focus:outline-none focus:border-indigo-500">
      </div>
      <div>
        <label class="block text-xs font-semibold text-slate-400 uppercase mb-2">Password</label>
        <input type="password" name="password" value="admin123" required class="w-full px-3.5 py-2.5 bg-slate-800 border border-slate-700 text-white rounded-lg text-sm focus:outline-none focus:border-indigo-500">
      </div>
      <a href="/" class="block text-center w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-lg text-sm transition shadow-lg shadow-indigo-600/30 mt-6">
        Sign In to ERP
      </a>
    </form>
  </div>
</body>
</html>"""

files = {
    'sales_app/templates/base.html': base_html,
    'sales_app/templates/dashboard.html': dashboard_html,
    'sales_app/templates/customers.html': customers_html,
    'sales_app/templates/products.html': products_html,
    'sales_app/templates/sales_form.html': sales_form_html,
    'sales_app/templates/login.html': login_html,
}

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("SUCCESS: ALL 6 TEMPLATES GENERATED IN sales_app/templates/!")