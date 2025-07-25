// Модалка
const modal = document.getElementById('appointmentModal');
const openModalBtn = document.getElementById('openModalBtn');
const closeBtn = document.querySelector('.close-btn');

openModalBtn.onclick = () => modal.style.display = 'block';
closeBtn.onclick = () => modal.style.display = 'none';
window.onclick = (e) => { if (e.target === modal) modal.style.display = 'none'; }

// Отправка формы
document.getElementById('appointmentForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());
    data.privacy_consent = formData.get('privacy_consent') ? true : false;

    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/appointments/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (response.ok && result.success) {
            alert('Запись успешно создана!');
            modal.style.display = 'none';
            this.reset();
        } else {
            alert('Ошибка: ' + (result.message || 'Не удалось создать запись'));
        }
    } catch (err) {
        alert('Ошибка сети: ' + err.message);
    }
});
