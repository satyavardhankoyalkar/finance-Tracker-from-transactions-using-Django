from django.shortcuts import get_object_or_404, render, redirect
from .models import Transaction
from .forms import TransactionForm
from django.http import JsonResponse
from django.urls import reverse
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse
from django.utils.dateformat import DateFormat
from django.core.paginator import Paginator
import calendar
from collections import defaultdict
from django.core.paginator import Paginator
from datetime import datetime
from decimal import Decimal
import matplotlib.pyplot as plt
from reportlab.lib import colors
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from django.conf import settings
import os
from tempfile import NamedTemporaryFile


def transaction_list(request):
    transactions = Transaction.objects.all()

    # Helper function to calculate total for specific categories
    def calculate_total(categories):
        return sum(t.amount for t in transactions if t.category in categories)

    # Define categories considered as expenses
    expense_categories = ['Food', 'Utilities', 'Rent', 'Entertainment', 'Salary']

    # Calculate totals
    total_income = calculate_total(['Income'])
    total_expense = calculate_total(expense_categories)
    balance = total_income - total_expense

    # Category-wise totals
    category_totals = {
        'Income': total_income,
        'Expense': total_expense,
        'Food': calculate_total(['Food']),
        'Utilities': calculate_total(['Utilities']),
        'Rent': calculate_total(['Rent']),
        'Entertainment': calculate_total(['Entertainment']),
        'Salary': calculate_total(['Salary']),
    }

    # Pagination logic
    paginator = Paginator(transactions, 3)  # 10 transactions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'transactions/transaction_list.html', {
        'page_obj': page_obj,  # Pass the page object for pagination
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'category_totals': category_totals,
    })



def add_transaction(request):
    if request.method == 'POST':
        category = request.POST['category']
        amount = request.POST['amount']
        description = request.POST['description']
        Transaction.objects.create(category=category, amount=amount, description=description)
        return redirect('transaction_list')
    return render(request, 'transactions/add_transaction.html')

# View to delete a transaction
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    return redirect('transaction_list')


def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()

            if request.is_ajax():  # Check if the request is AJAX
                return JsonResponse({
                    'success': True,
                    'redirect_url': reverse('transaction_list')
                })
            else:
                return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    
    return render(request, 'edit_transaction.html', {'form': form})


def download_csv(request):
    # Create the response object to return the CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=transactions.csv'
    
    # Create a CSV writer object to write data to the response
    writer = csv.writer(response)
    
    # Write the header of the CSV
    writer.writerow(['Category', 'Amount', 'Date', 'Description'])
    
    # Fetch all transactions from the database
    transactions = Transaction.objects.all()

    # Write each transaction as a row in the CSV
    for transaction in transactions:
        # Format the date in a readable format (e.g., YYYY-MM-DD)
        formatted_date = DateFormat(transaction.date).format('Y-m-d')
        writer.writerow([transaction.category, transaction.amount, formatted_date, transaction.description])
    
    return response


def download_pdf(request):
    # Create a response object with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=transactions.pdf'
    
    # Create a canvas for the PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Set up title and column headers
    p.setFont('Helvetica', 12)
    p.drawString(100, height - 50, "Transaction List")
    p.drawString(100, height - 70, "Category | Amount | Date | Description")

    # Fetch transactions from the database
    transactions = Transaction.objects.all()
    y_position = height - 90

    for transaction in transactions:
        formatted_date = transaction.date.strftime('%Y-%m-%d')  # Format date
        p.drawString(100, y_position, f"{transaction.category} | {transaction.amount} | {formatted_date} | {transaction.description}")
        y_position -= 20  # Move down for the next row

        if y_position < 100:  # Prevent overflow, create a new page if necessary
            p.showPage()
            y_position = height - 50

    p.showPage()
    p.save()

    return response

def stats_view(request):
    transactions = Transaction.objects.all()

    # Get filter parameters from the request (optional)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        transactions = transactions.filter(date__gte=start_date)
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        transactions = transactions.filter(date__lte=end_date)

    # Continue with category totals and monthly spending as before
    categories = ['Income', 'Food', 'Utilities', 'Rent', 'Entertainment', 'Salary']
    values = [
        sum(float(t.amount) for t in transactions if t.category == category) for category in categories
    ]
    
    monthly_spending = defaultdict(float)
    for transaction in transactions:
        month_name = calendar.month_name[transaction.date.month]
        monthly_spending[month_name] += float(transaction.amount)  # Convert to float

    months = list(monthly_spending.keys())
    spending_values = list(monthly_spending.values())

    return render(request, 'transactions/stats.html', {
        'categories': categories,
        'values': values,
        'months': months,
        'spending_values': spending_values,
        'start_date': start_date,
        'end_date': end_date,
    })


def export_stats_csv(request):
    transactions = Transaction.objects.all()
    
    # Define categories you want to track
    categories = ['Income', 'Food', 'Utilities', 'Rent', 'Entertainment', 'Salary']
    
    # Calculate the sum of transactions per category
    values = [
        sum(t.amount for t in transactions if t.category == category) for category in categories
    ]
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transaction_stats.csv"'

    writer = csv.writer(response)
    writer.writerow(['Category', 'Amount'])
    
    for category, value in zip(categories, values):
        writer.writerow([category, value])
    
    return response

def generate_chart_image(categories, values):
    # Create a pie chart using Matplotlib
    fig, ax = plt.subplots()
    ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

    # Save the chart to a temporary file
    tmpfile = NamedTemporaryFile(delete=False, suffix='.png')
    canvas = FigureCanvas(fig)
    canvas.print_png(tmpfile.name)
    tmpfile.close()  # Close the file so it can be accessed

    return tmpfile.name  # Return the path of the temporary file

def generate_report(request):
    # Example data for categories and spending
    categories = ["Food", "Transport", "Entertainment", "Bills"]
    values = [100, 50, 75, 120]
    
    # Generate the chart image
    chart_image_path = generate_chart_image(categories, values)
    
    # Create a byte buffer for the PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Add Title
    p.setFont("Helvetica", 16)
    p.drawString(100, 750, "Transaction Report")

    # Add Chart Image to PDF
    p.drawImage(chart_image_path, 100, 400, width=400, height=200)
    
    # Add Transaction Data
    p.setFont("Helvetica", 12)
    p.drawString(100, 350, f"Category-wise Spending:")

    for i, (category, value) in enumerate(zip(categories, values)):
        p.drawString(100, 320 - (i * 20), f"{category}: ${value}")
    
    # Save the PDF to the buffer
    p.showPage()
    p.save()
    
    # Get the PDF data from the buffer
    buffer.seek(0)
    
    # Return the PDF response
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transaction_report.pdf"'
    
    # Delete the temporary chart image file
    os.remove(chart_image_path)
    
    return response