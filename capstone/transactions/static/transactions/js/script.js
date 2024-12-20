document.addEventListener('DOMContentLoaded', () => {
    const filterDropdown = document.getElementById('categoryFilter');
    const transactionList = document.getElementById('transactionList');
    const transactions = transactionList.querySelectorAll('li');

    // Filter transactions based on the selected category
    filterDropdown.addEventListener('change', () => {
        const selectedCategory = filterDropdown.value;

        transactions.forEach(transaction => {
            const category = transaction.getAttribute('data-category');
            if (selectedCategory === 'all' || category === selectedCategory) {
                transaction.style.display = ''; // Show transaction
            } else {
                transaction.style.display = 'none'; // Hide transaction
            }
        });
    });
});
document.getElementById('categoryFilter').addEventListener('change', function() {
    const category = this.value;
    const transactions = document.querySelectorAll('#transactionList li');

    transactions.forEach(transaction => {
        const transactionCategory = transaction.getAttribute('data-category');
        if (category === 'all' || category === transactionCategory) {
            transaction.style.display = 'block';
        } else {
            transaction.style.display = 'none';
        }
    });
});
function searchTransactions() {
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    const transactions = document.querySelectorAll('#transactionList li');

    transactions.forEach(transaction => {
        const description = transaction.textContent.toLowerCase();
        if (description.includes(searchInput)) {
            transaction.style.display = 'block';
        } else {
            transaction.style.display = 'none';
        }
    });
}
function sortTransactionsByDate() {
    const transactions = Array.from(document.querySelectorAll('#transactionList li'));
    const sorted = transactions.sort((a, b) => {
        const dateA = new Date(a.getAttribute('data-date'));
        const dateB = new Date(b.getAttribute('data-date'));
        return dateA - dateB; // Ascending order
    });
    
    const list = document.getElementById('transactionList');
    list.innerHTML = '';
    sorted.forEach(transaction => list.appendChild(transaction));
}

// Call the function when needed (e.g., when a sort button is clicked)
document.querySelectorAll('#transactionList li').forEach(item => {
    item.addEventListener('mouseenter', () => {
        item.classList.add('highlight');
    });
    item.addEventListener('mouseleave', () => {
        item.classList.remove('highlight');
    });
});

document.querySelectorAll('#transactionList li').forEach(item => {
    item.addEventListener('click', () => {
        const details = item.querySelector('.transaction-details');
        if (details) {
            details.classList.toggle('hidden');
        }
    });
});
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    form.addEventListener('submit', function (event) {
        let isValid = true;
        const amount = document.querySelector('input[name="amount"]');
        const description = document.querySelector('input[name="description"]');

        // Check if the amount and description are filled in
        if (!amount.value || !description.value) {
            isValid = false;
            alert('Please fill in all required fields!');
        }

        if (!isValid) {
            event.preventDefault(); // Prevent form submission
        }
    });
});
document.addEventListener('DOMContentLoaded', function () {
    const editForm = document.querySelector('form');
    
    editForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent form from submitting normally
        
        // Collect form data
        const formData = new FormData(editForm);

        // Send AJAX request to the server
        fetch(editForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Transaction updated successfully!');
                window.location.href = data.redirect_url; // Redirect to transaction list
            } else {
                alert('Error updating transaction!');
            }
        })
        .catch(error => {
            alert('Error: ' + error);
        });
    });
});
