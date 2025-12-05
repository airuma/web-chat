import telebot
from config import BOT_TOKEN
import db

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    # Сохраняем пользователя в БД
    db.add_user(message.from_user.id, message.from_user.username)
    bot.send_message(
        message.chat.id, 
        "Привет! Я To-Do бот с базой данных PostgreSQL.\n"
        "Команды:\n"
        "/add <текст> @<категория> - Добавить задачу\n"
        "/list - Список задач\n"
        "/done <ID> - Выполнить задачу"
    )

@bot.message_handler(commands=['add'])
def add_command(message):
    try:
        # Парсим текст: "/add Купить молоко @Продукты"
        full_text = message.text.replace('/add ', '')
        
        if '@' in full_text:
            task_text, category = full_text.split('@', 1)
            category = category.strip()
        else:
            task_text = full_text
            category = "Общее"
            
        db.add_task(message.from_user.id, task_text.strip(), category)
        bot.send_message(message.chat.id, f"✅ Задача добавлена в категорию '{category}'")
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка. Используйте формат: /add Текст @Категория")

@bot.message_handler(commands=['list'])
def list_command(message):
    tasks = db.get_active_tasks(message.from_user.id)
    if not tasks:
        bot.send_message(message.chat.id, "Список задач пуст.")
        return

    response = "📋 **Ваши задачи:**\n"
    for task in tasks:
        # task[0]=id, task[1]=text, task[2]=category
        response += f"🆔 {task[0]} | {task[1]} (📂 {task[2]})\n"
    
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['done'])
def done_command(message):
    try:
        task_id = int(message.text.split()[1])
        db.complete_task(task_id, message.from_user.id)
        bot.send_message(message.chat.id, f"✅ Задача {task_id} выполнена!")
    except:
        bot.send_message(message.chat.id, "Ошибка. Укажите ID, например: /done 1")

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()