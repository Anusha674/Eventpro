// ============================================
// Admin Dashboard JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    initSidebar();
    initAdminSearch();
});

// ---- Sidebar toggle for mobile ----
function initSidebar() {
    const toggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.admin-sidebar');
    if (toggle && sidebar) {
        toggle.addEventListener('click', () => sidebar.classList.toggle('show'));
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 992 && !sidebar.contains(e.target) && !toggle.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        });
    }
}

// ---- Admin table search ----
function initAdminSearch() {
    const searchInputs = document.querySelectorAll('.admin-search');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const tableId = this.getAttribute('data-table');
            const rows = document.querySelectorAll(`#${tableId} tbody tr`);
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            });
        });
    });
}

// ---- Delete confirmation ----
function adminDelete(url, itemName) {
    if (confirm(`Delete "${itemName}"? This action cannot be undone.`)) {
        window.location.href = url;
    }
}
