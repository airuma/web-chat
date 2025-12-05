import time
import psycopg2
from config import DB_CONFIG

def clean_old_logs():
    """Автоматически удаляет логи старше 30 дней"""
    print("Запуск автоматической очистки логов...")
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM logs WHERE action_timestamp < NOW() - INTERVAL '30 days'")
        print("Старые логи удалены.")
    conn.close()

if __name__ == "__main__":
    # Имитация работы планировщика
    while True:
        clean_old_logs()
        # Пауза 24 часа 
        print("Ожидание следующего цикла...")
        time.sleep(86400)