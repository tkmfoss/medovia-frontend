function redirectTo(filename) {
    // Fallback: If it's already a route (like 'dashboard'), just redirect to it
    if (!filename.endsWith('.html')) {
        window.location.href = '/' + filename;
        return;
    }

    // Strip .html to match Flask route
    const route = filename.replace('.html', '');
    window.location.href = '/' + route;
}


document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');

    sidebar.addEventListener('mouseenter', () => {
        sidebar.classList.remove('collapsed');
    });

    sidebar.addEventListener('mouseleave', () => {
        sidebar.classList.add('collapsed');
    });
});