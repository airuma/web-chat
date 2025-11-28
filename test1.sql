CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    first_login TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    category_name VARCHAR(100) NOT NULL,
    UNIQUE (user_id, category_name)
);

CREATE TABLE tasks1 (
    task_id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    category_id INTEGER REFERENCES categories(category_id) ON DELETE SET NULL,
    task_text TEXT NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    due_date DATE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Вставка данных 
INSERT INTO users (user_id, username)
VALUES (123456789, 'Berik_Test');

INSERT INTO categories (user_id, category_name)
VALUES (123456789, 'Учеба');

INSERT INTO tasks1 (user_id, category_id, task_text, due_date)
VALUES (
    123456789, 
    (SELECT category_id FROM categories WHERE user_id = 123456789 AND category_name = 'Учеба'),
    'Завершить презентацию по физкультуре', 
    '2025-11-15'
);

-- Запросы на выборку
SELECT * FROM users;

SELECT 
    t.task_id, 
    u.username, 
    c.category_name, 
    t.task_text, 
    t.due_date
FROM tasks1 t
JOIN users u ON t.user_id = u.user_id
LEFT JOIN categories c ON t.category_id = c.category_id
WHERE u.user_id = 123456789;