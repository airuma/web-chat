-- 1. Таблица Пользователей
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY, -- ID из Telegram
    username VARCHAR(255),
    first_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Таблица Категорий (Связь 1:Many с users)
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    category_name VARCHAR(100) NOT NULL
);

-- 3. Таблица Задач (Связь 1:Many с users и categories)
CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    category_id INT REFERENCES categories(category_id) ON DELETE SET NULL,
    task_text TEXT NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Таблица Напоминаний (Связь 1:1 с tasks)
-- Выполняет критерий о наличии разных типов связей
CREATE TABLE reminders (
    reminder_id SERIAL PRIMARY KEY,
    task_id INT UNIQUE REFERENCES tasks(task_id) ON DELETE CASCADE,
    reminder_time TIMESTAMP NOT NULL,
    is_sent BOOLEAN DEFAULT FALSE
);

-- 5. Таблица Логов (Связь 1:Many с users)
-- Выполняет критерий о безопасности и отслеживании действий
CREATE TABLE logs (
    log_id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    action_type VARCHAR(50), -- например: 'ADD_TASK', 'COMPLETE_TASK'
    action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);