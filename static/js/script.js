function main() {
    function applyTheme(theme) {
        const logo = document.getElementById('logo_g');

        if (theme === 'dark') {
            document.documentElement.setAttribute('data-bs-theme', 'dark');
            logo.setAttribute('fill', '#c22');
        } else {
            document.documentElement.setAttribute('data-bs-theme', 'light');
            logo.setAttribute('fill', '#000');
        }
        localStorage.setItem('theme', theme);
    }

    // Проверяем сохраненную тему при загрузке
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        applyTheme(savedTheme);
    }

    // Обработчик переключения темы
    document.getElementById('btnSwitch').addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(newTheme);
    });
}

window.onload = main;