// Admin Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Auto-submit forms on select change
    const selectElements = document.querySelectorAll('select[onchange*="this.form.submit()"]');
    selectElements.forEach(select => {
        select.addEventListener('change', function() {
            this.form.submit();
        });
    });

    // Handle delete confirmation modal
    var deleteModal = document.getElementById('deleteModal');
    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', function (event) {
            var button = event.relatedTarget;
            var url = button.getAttribute('data-url');
            var confirmDelete = document.getElementById('confirmDelete');
            confirmDelete.href = url;
        });
    }

    // Disable expected delivery date when status is out of stock
    const statusSelect = document.getElementById('id_status');
    const expectedDeliveryDateInput = document.getElementById('id_expected_delivery_date');

    if (statusSelect && expectedDeliveryDateInput) {
        function toggleExpectedDeliveryDate() {
            if (statusSelect.value === 'out-of-stock') {
                expectedDeliveryDateInput.disabled = true;
                expectedDeliveryDateInput.value = '';
            } else {
                expectedDeliveryDateInput.disabled = false;
            }
        }

        statusSelect.addEventListener('change', toggleExpectedDeliveryDate);
        // Initial check
        toggleExpectedDeliveryDate();
    }
});
