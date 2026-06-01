// ============================================
// Charts JavaScript (Chart.js)
// ============================================

function initRevenueChart(labels, data) {
    const ctx = document.getElementById('revenueChart');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Revenue (₹)',
                data: data,
                borderColor: '#4F46E5',
                backgroundColor: 'rgba(79,70,229,0.1)',
                fill: true,
                tension: 0.4,
                borderWidth: 3,
                pointBackgroundColor: '#4F46E5',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.05)' } },
                x: { grid: { display: false } }
            }
        }
    });
}

function initBookingChart(labels, data) {
    const ctx = document.getElementById('bookingChart');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: ['#4F46E5', '#7C3AED', '#059669', '#D97706', '#0891B2', '#DC2626'],
                borderWidth: 0,
                hoverOffset: 8
            }]
        },
        options: {
            responsive: true,
            cutout: '65%',
            plugins: {
                legend: { position: 'bottom', labels: { padding: 16, usePointStyle: true } }
            }
        }
    });
}

function initMonthlyBookingChart(labels, data) {
    const ctx = document.getElementById('monthlyBookingChart');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Bookings',
                data: data,
                backgroundColor: 'rgba(124,58,237,0.8)',
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.05)' } },
                x: { grid: { display: false } }
            }
        }
    });
}
