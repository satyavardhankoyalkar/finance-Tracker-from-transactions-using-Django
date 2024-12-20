// Dropdown functionality (show/hide)
document.querySelector('.dropbtn')?.addEventListener('click', function () {
    const dropdownContent = document.querySelector('.dropdown-content');
    dropdownContent?.classList.toggle('show');
});

// Close the dropdown if clicked outside
window.addEventListener('click', function (event) {
    if (!event.target.matches('.dropbtn')) {
        const dropdownContent = document.querySelector('.dropdown-content');
        dropdownContent?.classList.remove('show');
    }
});

// Filter transactions by category
document.getElementById('categoryFilter')?.addEventListener('change', function () {
    const selectedCategory = this.value;
    document.querySelectorAll('#transactionList li').forEach(transaction => {
        const transactionCategory = transaction.getAttribute('data-category');
        transaction.style.display = selectedCategory === 'all' || transactionCategory === selectedCategory
            ? 'list-item'
            : 'none';
    });
});
