// Раскрывающееся меню
function toggleMenu() {
    const menu = document.getElementById('nav-menu');
    menu.classList.toggle('active');
}

// Отправка формы
document.getElementById('contactForm')?.addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем стандартную отправку формы

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    if (!name || !email) {
        alert('Пожалуйста, заполните все обязательные поля.');
        return;
    }

    // Здесь можно добавить код для отправки данных на сервер
    alert(`Сообщение успешно отправлено!\nИмя: ${name}\nEmail: ${email}\nСообщение: ${message}`);
    
    // Очищаем форму после отправки
    document.getElementById('contactForm').reset();
});