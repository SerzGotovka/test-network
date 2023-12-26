from .models import Network
from random import randint
from electro.celery import app
from celery.schedules import crontab
import qrcode
from io import BytesIO
from django.core.mail import EmailMessage


# Задача для увеличения задолженности перед поставщиком
@app.task(name='increase_debt')
def increase_debt(network_id):
    
    network = Network.objects.get(pk=network_id)

    debt = network.debt or 0
    debt += randint(5, 500)

    network.debt = debt
    network.save()


# Задача для уменьшения задолженности перед поставщиком
@app.task(name='decrease_debt')
def decrease_debt(network_id):
    # Получить сеть
    network = Network.objects.get(pk=network_id)

    debt = network.debt or 0
    debt -= randint(100, 10000)
    
    network.debt = debt
    network.save()


# Запланировать задачу на выполнение каждые 3 часа
app.conf.beat_schedule['increase_debt'] = {
    'task': 'increase_debt',
    'schedule': crontab(minute='*/3'),
    'args': (1,)
}

# Запланировать задачу на выполнение в 6:30 каждый день
app.conf.beat_schedule['decrease_debt'] = {
    'task': 'decrease_debt',
    'schedule': crontab(minute='30', hour='6'),
    'args': (1,)
}

@app.task(name='null_debt')
def async_clear_debt(list_id):
    for id in list_id:
        Network.objects.filter(id=id['id']).update(debt=0)


@app.task
def generate_qr_code_and_send_email(contact_email, contact_data):
    # Генерировать QR-код с контактными данными
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(contact_data)
    qr.make(fit=True)

    # Создать изображение QR-кода в памяти
    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = BytesIO()
    img.save(img_buffer)
    img_buffer.seek(0)

    # Создать и отправить письмо с QR-кодом на указанную электронную почту
    email_subject = 'QR Code'
    email_body = 'Ваш QR-код во вложении.'
    email = EmailMessage(email_subject, email_body, 'sender@example.com', [contact_email])
    email.attach('qr_code.png', img_buffer.read(), 'image/png')
    email.send(fail_silently=False)
    