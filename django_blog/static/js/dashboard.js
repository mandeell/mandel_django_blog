// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Animate stat numbers on load
    animateStatNumbers();
    
    // Auto-refresh dashboard data every 5 minutes
    setInterval(refreshDashboardData, 300000);
    
    // Add click handlers for quick actions
    setupQuickActions();
});

function animateStatNumbers() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const finalValue = parseInt(stat.textContent);
        let currentValue = 0;
        const increment = finalValue / 50;
        
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= finalValue) {
                stat.textContent = finalValue;
                clearInterval(timer);
            } else {
                stat.textContent = Math.floor(currentValue);
            }
        }, 30);
    });
}

function refreshDashboardData() {
    // This would typically make an AJAX call to refresh dashboard data
    console.log('Refreshing dashboard data...');
    
    // Add a subtle indicator that data is being refreshed
    const header = document.querySelector('.dashboard-header');
    if (header) {
        header.style.opacity = '0.7';
        setTimeout(() => {
            header.style.opacity = '1';
        }, 500);
    }
}

function setupQuickActions() {
    // Add hover effects to stat cards
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        });
    });
    
    // Add click handlers for recent items
    const recentItems = document.querySelectorAll('.recent-item');
    recentItems.forEach(item => {
        item.addEventListener('click', function() {
            // This would navigate to the item's detail page
            console.log('Clicked on:', this.querySelector('.item-title').textContent);
        });
        
        item.style.cursor = 'pointer';
    });
}