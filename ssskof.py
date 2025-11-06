import telebot
from telebot import types
import logging
import json
import os
from datetime import datetime, timedelta

# НАСТРОЙКИ
BOT_TOKEN = '8493265398:AAHd1sHN_IyIFHDojWvnO03v_LWBDCQ1n-U'
ADMIN_ID = 7698756917  # Главный админ (скупщик)
REPORT_ID = 7558662794  # Для отчетов о сделках

bot = telebot.TeleBot(BOT_TOKEN)
logging.basicConfig(level=logging.INFO)

# Файл базы данных
DB_FILE = 'ssskof.txt'
ACTIVE_CHATS_FILE = 'active_chats.txt'
USERS_FILE = 'users.txt'
ADMIN_CHATS_FILE = 'admin_chats.txt'
STATS_FILE = 'stats.txt'


# Инициализация базы
def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            f.write("")
    if not os.path.exists(ACTIVE_CHATS_FILE):
        with open(ACTIVE_CHATS_FILE, 'w', encoding='utf-8') as f:
            f.write("")
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            f.write("")
    if not os.path.exists(ADMIN_CHATS_FILE):
        with open(ADMIN_CHATS_FILE, 'w', encoding='utf-8') as f:
            f.write("")
    if not os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            f.write("")


def save_user(user_id):
    try:
        users = get_all_users()
        if user_id not in users:
            users.append(user_id)
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                for uid in users:
                    f.write(str(uid) + '\n')
        return True
    except Exception as e:
        logging.error(f"Ошибка сохранения пользователя: {e}")
        return False


def get_all_users():
    users = []
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    users.append(int(line.strip()))
    except FileNotFoundError:
        pass
    return users


def save_stats(deal_data):
    try:
        with open(STATS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(deal_data, ensure_ascii=False) + '\n')
        return True
    except Exception as e:
        logging.error(f"Ошибка сохранения статистики: {e}")
        return False


def get_stats():
    stats = []
    try:
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    stats.append(json.loads(line.strip()))
    except FileNotFoundError:
        pass
    return stats


def calculate_income(period='day'):
    stats = get_stats()
    now = datetime.now()
    total_income = 0

    for deal in stats:
        deal_time = datetime.fromisoformat(deal['timestamp'])

        if period == 'day' and deal_time.date() == now.date():
            total_income += deal['income']
        elif period == 'week' and deal_time >= now - timedelta(days=7):
            total_income += deal['income']
        elif period == 'month' and deal_time >= now - timedelta(days=30):
            total_income += deal['income']
        elif period == 'year' and deal_time >= now - timedelta(days=365):
            total_income += deal['income']
        elif period == 'all':
            total_income += deal['income']

    return total_income


def save_admin_chat(admin_id, user_id):
    try:
        with open(ADMIN_CHATS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps({'admin_id': admin_id, 'user_id': user_id}) + '\n')
        return True
    except Exception as e:
        logging.error(f"Ошибка сохранения чата админа: {e}")
        return False


def get_admin_chat(user_id):
    try:
        with open(ADMIN_CHATS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    chat = json.loads(line.strip())
                    if chat['user_id'] == user_id:
                        return chat
    except FileNotFoundError:
        pass
    return None


def remove_admin_chat(user_id):
    chats = []
    try:
        with open(ADMIN_CHATS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    chat = json.loads(line.strip())
                    if chat['user_id'] != user_id:
                        chats.append(chat)

        with open(ADMIN_CHATS_FILE, 'w', encoding='utf-8') as f:
            for chat in chats:
                f.write(json.dumps(chat) + '\n')
        return True
    except Exception as e:
        logging.error(f"Ошибка удаления чата админа: {e}")
        return False


def save_application(user_data):
    try:
        with open(DB_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(user_data, ensure_ascii=False) + '\n')
        return True
    except Exception as e:
        logging.error(f"Ошибка сохранения: {e}")
        return False


def get_applications():
    applications = []
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    applications.append(json.loads(line.strip()))
    except FileNotFoundError:
        pass
    return applications


def remove_application(user_id):
    applications = get_applications()
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            for app in applications:
                if app.get('user_id') != user_id:
                    f.write(json.dumps(app, ensure_ascii=False) + '\n')
        return True
    except Exception as e:
        logging.error(f"Ошибка удаления заявки: {e}")
        return False


def save_active_chat(user_id, admin_id):
    try:
        with open(ACTIVE_CHATS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps({'user_id': user_id, 'admin_id': admin_id, 'active': True}) + '\n')
        return True
    except Exception as e:
        logging.error(f"Ошибка сохранения чата: {e}")
        return False


def get_active_chats():
    chats = []
    try:
        with open(ACTIVE_CHATS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    chats.append(json.loads(line.strip()))
    except FileNotFoundError:
        pass
    return chats


def close_active_chat(user_id):
    chats = get_active_chats()
    try:
        with open(ACTIVE_CHATS_FILE, 'w', encoding='utf-8') as f:
            for chat in chats:
                if chat['user_id'] != user_id:
                    f.write(json.dumps(chat, ensure_ascii=False) + '\n')
        return True
    except Exception as e:
        logging.error(f"Ошибка закрытия чата: {e}")
        return False


def is_user_in_active_chat(user_id):
    chats = get_active_chats()
    return any(chat['user_id'] == user_id for chat in chats)


# Инициализируем БД
init_db()
print("Бот и база данных инициализированы!")


# Проверка на админа
def is_admin(user_id):
    return user_id == ADMIN_ID


def is_report_user(user_id):
    return user_id == REPORT_ID


# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_user(message.from_user.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if is_admin(message.from_user.id):
        btn_applications = types.KeyboardButton('📋 Список заявок')
        btn_admin = types.KeyboardButton('📢 Сделать рассылку')
        btn_stats = types.KeyboardButton('💰 Общий доход')
        markup.add(btn_applications, btn_admin, btn_stats)
        welcome_text = "👑 Панель администратора"
    elif is_report_user(message.from_user.id):
        btn_stats = types.KeyboardButton('💰 Общий доход')
        markup.add(btn_stats)
        welcome_text = "📊 Панель отчетов"
    else:
        if is_user_in_active_chat(message.from_user.id):
            welcome_text = "💬 Чат с администратором открыт. Пишите сообщения."
        else:
            btn_sell = types.KeyboardButton('💰 Продать аккаунт')
            btn_info = types.KeyboardButton('ℹ️ Информация')
            markup.add(btn_sell, btn_info)
            welcome_text = "🤖 Привет! Это бот скупщик тг акков новорегов/с отлежкой\n\n💰 Цена: $1.3 за аккаунт\n💳 Выплата: CryptoBot\n⏰ Ответ: 20 мин - 2 часа\n\nВыберите действие:"

    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


# Команда /cancel
@bot.message_handler(commands=['cancel'])
def cancel_process(message):
    send_welcome(message)


# ОБЩИЙ ДОХОД
@bot.message_handler(func=lambda message: message.text == '💰 Общий доход' and (
        is_admin(message.from_user.id) or is_report_user(message.from_user.id)))
def show_income(message):
    day_income = calculate_income('day')
    week_income = calculate_income('week')
    month_income = calculate_income('month')
    year_income = calculate_income('year')
    total_income = calculate_income('all')

    income_text = f"""
💰 ОБЩИЙ ДОХОД

📊 Статистика доходов:
• За сегодня: ${day_income:.2f}
• За неделю: ${week_income:.2f}
• За месяц: ${month_income:.2f}
• За год: ${year_income:.2f}
• Всего: ${total_income:.2f}

👤 Покупатели: {len(get_all_users())}
"""
    bot.send_message(message.chat.id, income_text)


# АДМИН-ПАНЕЛЬ - РАССЫЛКА
@bot.message_handler(func=lambda message: message.text == '📢 Сделать рассылку' and is_admin(message.from_user.id))
def start_broadcast(message):
    msg = bot.send_message(message.chat.id, "✍️ Введите сообщение для рассылки (для отмены используйте /cancel):")
    bot.register_next_step_handler(msg, process_broadcast_message)


def process_broadcast_message(message):
    if message.text == '/cancel':
        send_welcome(message)
        return

    if is_admin(message.from_user.id):
        broadcast_text = message.text

        preview_markup = types.InlineKeyboardMarkup()
        btn_confirm = types.InlineKeyboardButton("✅ Разослать", callback_data="confirm_broadcast")
        btn_cancel = types.InlineKeyboardButton("❌ Отменить", callback_data="cancel_broadcast")
        preview_markup.add(btn_confirm, btn_cancel)

        bot.send_message(message.chat.id,
                         f"📨 Предпросмотр рассылки:\n\n{broadcast_text}",
                         reply_markup=preview_markup)


# ОБРАБОТКА РАССЫЛКИ
@bot.callback_query_handler(func=lambda call: call.data in ['confirm_broadcast', 'cancel_broadcast'])
def handle_broadcast_confirmation(call):
    if call.data == 'cancel_broadcast':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "❌ Рассылка отменена")
        return

    elif call.data == 'confirm_broadcast':
        broadcast_text = call.message.text.split('\n\n', 1)[1]

        bot.edit_message_text("🔄 Начинаю рассылку...", call.message.chat.id, call.message.message_id)

        users = get_all_users()
        success_count = 0
        fail_count = 0

        for user_id in users:
            try:
                bot.send_message(user_id, broadcast_text)
                success_count += 1
            except Exception as e:
                fail_count += 1

        bot.send_message(call.message.chat.id,
                         f"✅ Рассылка завершена!\n\nУспешно: {success_count}\nНе удалось: {fail_count}")


# СПИСОК ЗАЯВОК ДЛЯ АДМИНА
@bot.message_handler(func=lambda message: message.text == '📋 Список заявок' and is_admin(message.from_user.id))
def show_applications_list(message):
    applications = get_applications()
    pending_apps = [app for app in applications if
                    app.get('status') == 'pending' and not is_user_in_active_chat(app.get('user_id'))]

    if not pending_apps:
        bot.send_message(message.chat.id, "📭 Нет новых заявок")
        return

    for app in pending_apps[-10:]:
        total_price = 1.3 * app.get('account_count', 1)
        app_text = f"""
🆕 Новая заявка #{app.get('id', len(applications))}

👤 Покупатель ID: {app.get('user_id', 'N/A')}
📱 Username: @{app.get('username', 'N/A')}
👤 Имя: {app.get('user_name', 'N/A')}

📊 Детали:
• Количество аккаунтов: {app.get('account_count', 1)}
• Номера: {app.get('phones', 'N/A')}

💰 Цена: ${total_price:.2f}
        """

        markup = types.InlineKeyboardMarkup()
        btn_accept = types.InlineKeyboardButton("✅ Принять заявку", callback_data=f"accept_{app.get('user_id')}")
        markup.add(btn_accept)

        bot.send_message(message.chat.id, app_text, reply_markup=markup)


# ОБРАБОТКА ЗАЯВОК
@bot.callback_query_handler(func=lambda call: call.data.startswith('accept_'))
def handle_application_response(call):
    user_id = int(call.data.split('_')[1])

    remove_application(user_id)
    save_active_chat(user_id, call.from_user.id)
    save_admin_chat(call.from_user.id, user_id)

    bot.send_message(user_id, "💬 Чат с администратором открыт. Пишите сообщения.")

    markup = types.InlineKeyboardMarkup()
    btn_complete = types.InlineKeyboardButton("✅ Завершить сделку", callback_data=f"complete_{user_id}")
    markup.add(btn_complete)

    bot.send_message(call.message.chat.id,
                     f"💬 Чат с покупателем {user_id} открыт. Просто напишите сообщение - оно отправится покупателю.",
                     reply_markup=markup)

    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id, "Заявка принята")


# ЗАВЕРШЕНИЕ СДЕЛКИ
@bot.callback_query_handler(func=lambda call: call.data.startswith('complete_'))
def handle_complete_deal(call):
    user_id = int(call.data.split('_')[1])

    # Находим данные сделки
    applications = get_applications()
    deal_data = None
    for app in applications:
        if app.get('user_id') == user_id:
            deal_data = app
            break

    close_active_chat(user_id)
    remove_admin_chat(user_id)

    # Сохраняем статистику
    if deal_data:
        income = 1.3 * deal_data.get('account_count', 1)
        stats_data = {
            'user_id': user_id,
            'income': income,
            'account_count': deal_data.get('account_count', 1),
            'timestamp': datetime.now().isoformat()
        }
        save_stats(stats_data)

        # Отправляем отчет о сделке
        report_text = f"""
✅ СДЕЛКА ЗАВЕРШЕНА

👤 Покупатель: {deal_data.get('user_name', 'N/A')}
🆔 ID: {user_id}
📱 Username: @{deal_data.get('username', 'N/A')}

💰 Доход: ${income:.2f}
📊 Аккаунтов: {deal_data.get('account_count', 1)}

⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
        bot.send_message(REPORT_ID, report_text)

    bot.send_message(user_id, "✅ Сделка завершена! Спасибо за сотрудничество.")

    bot.answer_callback_query(call.id, "Сделка завершена")
    bot.delete_message(call.message.chat.id, call.message.message_id)


# ПРОЦЕСС ПРОДАЖИ АККАУНТА
@bot.message_handler(func=lambda message: message.text == '💰 Продать аккаунт' and not is_admin(message.from_user.id))
def start_sell_process(message):
    if is_user_in_active_chat(message.from_user.id):
        bot.send_message(message.chat.id, "💬 Вы уже в активной сделке. Завершите текущую сделку перед созданием новой.")
        return

    msg = bot.send_message(message.chat.id,
                           "🔢 Сколько аккаунтов хотите продать? (1-25)\n\nДля отмены используйте /cancel")
    bot.register_next_step_handler(msg, process_account_count)


def process_account_count(message):
    if message.text == '/cancel':
        send_welcome(message)
        return

    try:
        account_count = int(message.text.strip())
        if account_count <= 0:
            bot.send_message(message.chat.id, "❌ Введите число больше 0\nПопробуйте снова:")
            bot.register_next_step_handler(message, process_account_count)
            return
        elif account_count > 25:
            bot.send_message(message.chat.id, "❌ Максимум 25 аккаунтов за раз\nВведите число от 1 до 25:")
            bot.register_next_step_handler(message, process_account_count)
            return

        user_data = {
            'account_count': account_count,
            'user_id': message.from_user.id,
            'user_name': f"{message.from_user.first_name} {message.from_user.last_name or ''}",
            'username': message.from_user.username or 'Нет username',
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }

        if account_count == 1:
            msg = bot.send_message(message.chat.id,
                                   "📞 Введите номер телефона аккаунта:\n\nДля отмены используйте /cancel")
            bot.register_next_step_handler(msg, process_single_phone, user_data)
        else:
            msg = bot.send_message(message.chat.id,
                                   f"📞 Введите {account_count} номеров телефонов через запятую:\n\nДля отмены используйте /cancel")
            bot.register_next_step_handler(msg, process_multiple_phones, user_data)

    except ValueError:
        bot.send_message(message.chat.id, "❌ Пожалуйста, введите корректное число (только цифры):")
        bot.register_next_step_handler(message, process_account_count)


def process_single_phone(message, user_data):
    if message.text == '/cancel':
        send_welcome(message)
        return

    user_data['phones'] = message.text.strip()
    complete_application(message, user_data)


def process_multiple_phones(message, user_data):
    if message.text == '/cancel':
        send_welcome(message)
        return

    user_data['phones'] = message.text.strip()
    complete_application(message, user_data)


def complete_application(message, user_data):
    try:
        save_user(message.from_user.id)

        applications = get_applications()
        user_data['id'] = len(applications) + 1

        if save_application(user_data):
            notify_admin(user_data)

            total_price = 1.3 * user_data['account_count']
            user_text = f"""
✅ Заявка создана!

📊 Детали заявки:
• Количество аккаунтов: {user_data['account_count']}
• Номера: 
<code>{user_data['phones']}</code>

💰 Сумма к выплате: ${total_price:.2f}
💳 Выплата: CryptoBot

⏱ После передачи аккаунтов выплата производится в течение 15-40 минут

Ожидайте подтверждения заявки администратором.
            """
            bot.send_message(message.chat.id, user_text, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, "❌ Ошибка создания заявки!")

    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")


def notify_admin(user_data):
    try:
        total_price = 1.3 * user_data['account_count']
        admin_text = f"""
🆕 Новая заявка #{user_data['id']}

👤 Покупатель ID: {user_data['user_id']}
📱 Username: @{user_data['username']}
👤 Имя: {user_data['user_name']}

📊 Детали:
• Количество аккаунтов: {user_data['account_count']}
• Номера: 
<code>{user_data['phones']}</code>

💰 Сумма: ${total_price:.2f}
"""
        bot.send_message(ADMIN_ID, admin_text, parse_mode='HTML')
    except Exception as e:
        logging.error(f"Ошибка уведомления админа: {e}")


# ИНФОРМАЦИЯ
@bot.message_handler(func=lambda message: message.text == 'ℹ️ Информация')
def show_info(message):
    info_text = """
ℹ️ Информация о боте

🤖 Бот для скупки Telegram аккаунтов

💳 Выплаты: CryptoBot
💰 Цена: $1.3 за аккаунт

👨‍💻 Разработчик: @steddyrevival
🛠 Скупщик: @CLS141

⏱ Выплата в течение 15-40 минут после передачи аккаунтов
⏰ Ответ администратора: 20 минут - 2 часа
"""
    bot.send_message(message.chat.id, info_text)


# ОБРАБОТКА ВСЕХ СООБЩЕНИЙ ДЛЯ ЧАТА
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    save_user(message.from_user.id)

    # ЕСЛИ АДМИН ПИШЕТ СООБЩЕНИЕ
    if is_admin(message.from_user.id) and message.text not in ['📋 Список заявок', '📢 Сделать рассылку',
                                                               '💰 Общий доход']:
        active_chats = get_active_chats()
        admin_chat = None
        for chat in active_chats:
            if chat['admin_id'] == message.from_user.id:
                admin_chat = chat
                break

        if admin_chat:
            user_id = admin_chat['user_id']
            bot.send_message(user_id, message.text)
        return

    # ЕСЛИ ПОКУПАТЕЛЬ ПИШЕТ И У НЕГО ЕСТЬ АКТИВНЫЙ ЧАТ
    if not is_admin(message.from_user.id) and is_user_in_active_chat(message.from_user.id):
        if message.text not in ['💰 Продать аккаунт', 'ℹ️ Информация']:
            bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        return

    # ЕСЛИ ПОКУПАТЕЛЬ ПИШЕТ НЕ В АКТИВНОМ ЧАТЕ
    if not is_admin(message.from_user.id) and message.text not in ['💰 Продать аккаунт',
                                                                   'ℹ️ Информация'] and not is_user_in_active_chat(
            message.from_user.id):
        bot.send_message(message.chat.id, "ℹ️ Используйте кнопки для взаимодействия с ботом")


# Запуск бота
if __name__ == '__main__':
    print("Бот запускается...")
    bot.polling(none_stop=True)