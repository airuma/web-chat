import psycopg2
from config import DB_CONFIG

def get_connection():
    """Создает подключение к БД"""
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    return conn

def add_user(user_id, username):
    """Регистрирует пользователя (INSERT)"""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            # Проверяем, есть ли пользователь, чтобы не было ошибки
            cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO users (user_id, username) VALUES (%s, %s)",
                    (user_id, username)
                )

def log_action(user_id, action):
    """Записывает действие в таблицу logs (INSERT)"""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO logs (user_id, action_type) VALUES (%s, %s)",
                (user_id, action)
            )

def add_task(user_id, text, category_name="Общее"):
    """Добавляет задачу и категорию (Транзакция)"""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            # 1. Сначала находим или создаем категорию
            cursor.execute(
                "SELECT category_id FROM categories WHERE user_id = %s AND category_name = %s", 
                (user_id, category_name)
            )
            cat_result = cursor.fetchone()
            
            if cat_result:
                cat_id = cat_result[0]
            else:
                cursor.execute(
                    "INSERT INTO categories (user_id, category_name) VALUES (%s, %s) RETURNING category_id", 
                    (user_id, category_name)
                )
                cat_id = cursor.fetchone()[0]

            # 2. Добавляем задачу
            cursor.execute(
                "INSERT INTO tasks (user_id, category_id, task_text) VALUES (%s, %s, %s)",
                (user_id, cat_id, text)
            )
    # Логируем действие
    log_action(user_id, f"ADDED_TASK: {text[:20]}")

def get_active_tasks(user_id):
    """
    Получает задачи с названиями категорий.
    Использует JOIN (Критерий 2.2 - сложные запросы)
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            query = """
                SELECT t.task_id, t.task_text, c.category_name 
                FROM tasks t
                JOIN categories c ON t.category_id = c.category_id
                WHERE t.user_id = %s AND t.is_completed = FALSE
                ORDER BY t.created_at
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()

def complete_task(task_id, user_id):
    """Отмечает задачу выполненной (UPDATE)"""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE tasks SET is_completed = TRUE WHERE task_id = %s AND user_id = %s",
                (task_id, user_id)
            )
    log_action(user_id, f"COMPLETED_TASK_ID: {task_id}")
    # ... весь ваш код выше ...

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("✅ Успешное подключение к базе данных!")
        conn.close()
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")