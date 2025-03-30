# Personal Finance Tracker

## Distinctiveness and Complexity

The **Personal Finance Tracker** is a web application designed to help users manage and track their personal finances, focusing on transactions, budgeting, and spending analysis. This project goes beyond simple transaction logging by integrating advanced features such as:

- **Dynamic statistics visualization** with interactive charts.
- **Transaction reports** downloadable in **PDF** or **CSV** formats.
- **Secure user authentication** for personalized tracking.

### Key Differentiators
- **Category-wise Spending Analysis**: Visual representation of spending patterns using **pie charts**.
- **Monthly Spending Overview**: Track expenses over time with **bar charts**.
- **Report Generation**: Export transaction data in **PDF** or **CSV** formats.
- **User Authentication**: Secure login and transaction management.

The project achieves complexity by integrating backend functionalities (**Django models, database integration, and user management**) with frontend interactivity (**charts, dynamic content, and report generation**), making it stand out from simpler projects.

---

## Project Overview
The **Personal Finance Tracker** allows users to:
- Track financial transactions (**income and expenses**).
- Categorize transactions for better analysis.
- Visualize spending trends over different time periods.
- Download detailed reports (**PDF or CSV**).

### Features
- **User Registration & Authentication**: Secure login and personalized experience.
- **Add and Edit Transactions**: Log and manage transactions with categories.
- **Interactive Charts**: Visual spending breakdown using **Chart.js**.
- **Report Downloads**: Generate reports using **jsPDF** and **html2canvas**.
- **Mobile-Responsive Design**: Built with **Bootstrap** for cross-device compatibility.

---

## Project Structure
```
finance-tracker/
│── transactions/      # Django app
│   ├── models.py      # Defines transaction data structure
│   ├── views.py       # Handles transaction display, reporting, and stats
│   ├── urls.py        # URL routing for various views
│   ├── templates/     # HTML templates for rendering views
│   │   ├── index.html   # Home page with transaction forms & charts
│   │   ├── stats.html   # Displays spending charts
│   ├── static/        # Static files for styling & scripts
│   │   ├── css/       # Custom styling files (styles.css)
│   │   ├── js/        # JavaScript for charts and interactivity
│── requirements.txt   # Dependencies (Django, Chart.js, jsPDF, etc.)
```

---

## How to Run the Application
### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/finance-tracker.git
cd finance-tracker
```

### Step 2: Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
.\venv\Scripts\activate   # Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Database Migrations
```bash
python manage.py migrate
```

### Step 5: Create a Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Run the Development Server
```bash
python manage.py runserver
```

**Access the application at:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Dependencies
This project uses the following libraries:
- **Django**: Backend framework for web development.
- **Chart.js**: Frontend library for interactive data visualization.
- **html2canvas**: Captures HTML elements as images for reports.
- **jsPDF**: Generates PDF reports for transactions.

Install all dependencies with:
```bash
pip install -r requirements.txt
```

---

## Additional Information
- **Mobile-Responsive**: Built using **Bootstrap** for seamless usability on all devices.
- **Chart Customization**: Interactive charts enhance financial insights.
- **Exporting Reports**: Download financial reports in **PDF and CSV** formats for further analysis.

---

## License
**MIT License** – See the LICENSE file for details.

