import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Заберем токен нашего бота (прописать в файле ".env")
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

# Заберем данные для подключения к базе данных (юзер, пароль, название бд) - тоже прописать в файле ".env"
PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))

admins = [
    os.getenv("ADMIN_ID"),
    os.getenv("IRA_ID"),
]

ADMINS = os.getenv("ADMIN_ID")  # Тут у нас будет список из админов

ip = os.getenv("ip")

# Ссылка подключения к базе данных
POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@bot_bear_postgres_1/{DATABASE}" # Подключение из контейнера
# POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@localhost/{DATABASE}"

try:
    # Попробуем установить соединение
    conn = psycopg2.connect(POSTGRES_URI)
    print("Успешное подключение к базе данных!")
except Exception as e:
    print(f"Ошибка подключения к базе данных: {e}")
# finally:
#     # Всегда закрываем соединение в конце
#     if conn is not None:
#         conn.close()
# aiogram_redis = {
#     'host': ip,
# }
#
# redis = {
#     'address': (ip, 6379),
#     'encoding': 'utf8'
# }

