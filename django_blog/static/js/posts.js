// Posts Management JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize post management features
    setupDeleteConfirmation();
    setupFormValidation();
    setupTableSorting();
    setupBulkActions();
});

//function setupDeleteConfirmation() {
//    const deleteButtons = document.querySelectorAll('.btn-danger');
//    deleteButtons.forEach(button => {
//        button.addEventListener('click', function(e) {
//            if (!confirm('Are you sure you want to delete this post? This action cannot be undone.')) {
//                e.preventDefault();
//            }
//        });
//    });
//}

function setupFormValidation() {
    const postForm = document.getElementById('postForm');
    if (postForm) {
        postForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Clear previous errors
            document.querySelectorAll('.field-error').forEach(error => {
                error.remove();
            });
            
            // Validate title
            const titleField = document.getElementById('id_title');
            if (titleField && !titleField.value.trim()) {
                showFieldError(titleField, 'Title is required');
                isValid = false;
            }
            
            // Validate content
            const contentField = document.getElementById('id_content');
            if (contentField && !contentField.value.trim()) {
                showFieldError(contentField, 'Content is required');
                isValid = false;
            }
            
            // Validate excerpt
            const excerptField = document.getElementById('id_excerpt');
            if (excerptField && !excerptField.value.trim()) {
                showFieldError(excerptField, 'Excerpt is required');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
}

function setupTableSorting() {
    const tableHeaders = document.querySelectorAll('th[data-sort]');
    tableHeaders.forEach(header => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            const sortBy = this.dataset.sort;
            sortTable(sortBy);
        });
    });
}

function setupBulkActions() {
    const selectAllCheckbox = document.getElementById('selectAll');
    const itemCheckboxes = document.querySelectorAll('.item-checkbox');
    const bulkActionButton = document.getElementById('bulkAction');
    
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            itemCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateBulkActionButton();
        });
    }
    
    itemCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateBulkActionButton);
    });
    
    function updateBulkActionButton() {
        const checkedItems = document.querySelectorAll('.item-checkbox:checked');
        if (bulkActionButton) {
            bulkActionButton.style.display = checkedItems.length > 0 ? 'block' : 'none';
        }
    }
}

function sortTable(sortBy) {
    // This would typically make an AJAX call to sort the table
    console.log('Sorting by:', sortBy);
    
    // Add visual feedback
    const currentUrl = new URL(window.location);
    currentUrl.searchParams.set('sort', sortBy);
    window.location.href = currentUrl.toString();
}

function showFieldError(field, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.style.color = '#dc3545';
    errorDiv.style.fontSize = '12px';
    errorDiv.style.marginTop = '5px';
    errorDiv.textContent = message;
    field.parentElement.appendChild(errorDiv);
}

// Auto-save draft functionality
function setupAutoSave() {
    const titleField = document.getElementById('id_title');
    const contentField = document.getElementById('id_content');
    
    if (titleField && contentField) {
        let autoSaveTimer;
        
        [titleField, contentField].forEach(field => {
            field.addEventListener('input', function() {
                clearTimeout(autoSaveTimer);
                autoSaveTimer = setTimeout(saveDraft, 30000); // Auto-save after 30 seconds
            });
        });
    }
}

function saveDraft() {
    const formData = new FormData(document.getElementById('postForm'));
    formData.set('status', 'draft');
    
    // This would typically make an AJAX call to save the draft
    console.log('Auto-saving draft...');
    
    // Show save indicator
    showSaveIndicator('Draft saved automatically');
}

function showSaveIndicator(message) {
    const indicator = document.createElement('div');
    indicator.className = 'save-indicator';
    indicator.textContent = message;
    indicator.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #28a745;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
        z-index: 1000;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    
    document.body.appendChild(indicator);
    
    setTimeout(() => {
        indicator.style.opacity = '1';
    }, 100);
    
    setTimeout(() => {
        indicator.style.opacity = '0';
        setTimeout(() => {
            indicator.remove();
        }, 300);
    }, 3000);
}