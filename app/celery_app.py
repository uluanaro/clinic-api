from celery import Celery
celery_app = Celery('celery_app',
                    broker="redis://localhost:6379/0",
                    backend="redis://localhost:6379/1",)
@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def send_appointment_reminder(self, patient_email: str, slot_time: str):
    print(f"Отправляю напоминание на {patient_email}...")
    return "Напоминание успешно доставлено"


