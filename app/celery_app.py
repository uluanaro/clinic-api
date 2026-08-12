import redis
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
    r = redis.from_url("redis://localhost:6379/2", decode_responses=True)
    r.publish("notifications", f"Напоминание отправлено на {patient_email} о приёме {slot_time}")
    return "Напоминание успешно доставлено"


