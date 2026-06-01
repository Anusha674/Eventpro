// Payment page logic
document.addEventListener('DOMContentLoaded', function() {
    const modeSelect = document.getElementById('paymentMode');
    if (modeSelect) {
        modeSelect.addEventListener('change', function() {
            document.querySelectorAll('.payment-detail').forEach(d => d.style.display = 'none');
            const detail = document.getElementById('detail-' + this.value);
            if (detail) detail.style.display = 'block';
        });
    }

    const paymentForm = document.getElementById('paymentForm');
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(e) {
            const btn = this.querySelector('button[type="submit"]');
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing Payment...';
        });
    }
});
