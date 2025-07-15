// Enhanced Mobile Admin Panel JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const userMenuButton = document.getElementById('userMenuButton');
    const userDropdown = document.getElementById('userDropdown');
    const toggleSidebar = document.getElementById('toggleSidebar');
    const closeSidebar = document.getElementById('closeSidebar');
    const sidebar = document.getElementById('sidebar');
    const mobileOverlay = document.getElementById('mobileOverlay');
    const mainContent = document.getElementById('mainContent');

    // User dropdown functionality
    if (userMenuButton && userDropdown) {
        userMenuButton.addEventListener('click', function(e) {
            e.stopPropagation();
            userDropdown.classList.toggle('hidden');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!userMenuButton.contains(e.target) && !userDropdown.contains(e.target)) {
                userDropdown.classList.add('hidden');
            }
        });
    }

    // Mobile sidebar functionality
    function openSidebar() {
        if (sidebar) {
            sidebar.classList.remove('-translate-x-full');
        }
        if (mobileOverlay) {
            mobileOverlay.classList.remove('hidden');
        }
        document.body.style.overflow = 'hidden';
    }

    function closeSidebarFunc() {
        if (sidebar) {
            sidebar.classList.add('-translate-x-full');
        }
        if (mobileOverlay) {
            mobileOverlay.classList.add('hidden');
        }
        document.body.style.overflow = '';
    }

    if (toggleSidebar) {
        toggleSidebar.addEventListener('click', function() {
            if (window.innerWidth < 1024) {
                openSidebar();
            } else {
                // Desktop toggle functionality
                if (sidebar && sidebar.classList.contains('-translate-x-full')) {
                    sidebar.classList.remove('-translate-x-full');
                    if (mainContent) {
                        mainContent.classList.remove('lg:ml-0');
                        mainContent.classList.add('lg:ml-64');
                    }
                } else if (sidebar) {
                    sidebar.classList.add('-translate-x-full');
                    if (mainContent) {
                        mainContent.classList.remove('lg:ml-64');
                        mainContent.classList.add('lg:ml-0');
                    }
                }
            }
        });
    }

    if (closeSidebar) {
        closeSidebar.addEventListener('click', closeSidebarFunc);
    }

    if (mobileOverlay) {
        mobileOverlay.addEventListener('click', closeSidebarFunc);
    }

    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 1024) {
            if (sidebar) {
                sidebar.classList.remove('-translate-x-full');
            }
            if (mobileOverlay) {
                mobileOverlay.classList.add('hidden');
            }
            document.body.style.overflow = '';
            if (mainContent) {
                mainContent.classList.add('lg:ml-64');
                mainContent.classList.remove('lg:ml-0');
            }
        } else {
            if (sidebar && !sidebar.classList.contains('-translate-x-full')) {
                closeSidebarFunc();
            }
        }
    });

    // Close sidebar when clicking on navigation links on mobile
    if (sidebar) {
        const sidebarLinks = sidebar.querySelectorAll('a');
        sidebarLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth < 1024) {
                    closeSidebarFunc();
                }
            });
        });
    }

    // Improve touch scrolling on mobile
    if ('ontouchstart' in window && sidebar) {
        sidebar.style.webkitOverflowScrolling = 'touch';
    }

    // Mobile table improvements
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        if (window.innerWidth <= 768) {
            table.classList.add('mobile-table');
            const container = table.parentElement;
            if (container) {
                container.classList.add('mobile-table-container');
            }
        }
    });

    // Touch-friendly button sizing
    if ('ontouchstart' in window) {
        const buttons = document.querySelectorAll('button, .btn, a[role="button"]');
        buttons.forEach(button => {
            if (window.getComputedStyle(button).minHeight === 'auto') {
                button.style.minHeight = '44px';
            }
            if (window.getComputedStyle(button).minWidth === 'auto') {
                button.style.minWidth = '44px';
            }
        });
    }

    // Prevent zoom on input focus for iOS
    if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
        const inputs = document.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            if (parseFloat(window.getComputedStyle(input).fontSize) < 16) {
                input.style.fontSize = '16px';
            }
        });
    }

    // Enhanced mobile form handling
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            // Disable submit button to prevent double submission
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Processing...';
                submitBtn.disabled = true;
                
                // Re-enable after 5 seconds as fallback
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });

    // Mobile-friendly dropdown menus
    const dropdowns = document.querySelectorAll('.dropdown-menu');
    dropdowns.forEach(dropdown => {
        if (window.innerWidth <= 768) {
            dropdown.style.position = 'fixed';
            dropdown.style.left = '1rem';
            dropdown.style.right = '1rem';
            dropdown.style.width = 'auto';
        }
    });

    // Swipe gesture for mobile sidebar
    let startX = 0;
    let currentX = 0;
    let isDragging = false;

    document.addEventListener('touchstart', function(e) {
        if (window.innerWidth < 1024) {
            startX = e.touches[0].clientX;
            isDragging = true;
        }
    });

    document.addEventListener('touchmove', function(e) {
        if (!isDragging || window.innerWidth >= 1024) return;
        
        currentX = e.touches[0].clientX;
        const diffX = currentX - startX;
        
        // Swipe right to open sidebar (from left edge)
        if (startX < 50 && diffX > 50 && sidebar && sidebar.classList.contains('-translate-x-full')) {
            openSidebar();
        }
        
        // Swipe left to close sidebar
        if (diffX < -50 && sidebar && !sidebar.classList.contains('-translate-x-full')) {
            closeSidebarFunc();
        }
    });

    document.addEventListener('touchend', function() {
        isDragging = false;
    });
});