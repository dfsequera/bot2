import telebot
from telebot.types import ReplyKeyboardRemove
import sqlite3 

# Inicializar el bot de Telegram
bot = telebot.TeleBot('5845836818:AAF4iGHTM4HdMUGeEjo62fpMf-bcQfhi8nQ')

@bot.message_handler(commands=["start", "ayuda", "help"])
def cmd_start(message):
    #username = message.chat.username
    username = message.from_user.username
    bot.reply_to(message, f"Hola {username}, Bienvenido a EstaGen!")
    markup = ReplyKeyboardRemove()
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, "Usa el comando /consulta para hacer una consulta, referente a conceptos en el área de las estadísticas", reply_markup=markup)
    
    
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Bienvenida"),
        telebot.types.BotCommand("/consulta", "Pregunta"),
        
    ])

# Definir un controlador para el comando /consulta
@bot.message_handler(commands=['consulta'])
def handle_query(message):
    import sqlite3
    # Configurar la conexión a la base de datos
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()

    # Obtener el parámetro pasado por el usuario
    parametro = message.text.split()[1]

    # Ejecutar la consulta y obtener el resultado
    #c.execute("SELECT descr FROM bot WHERE LOWER(nombre)=LOWER(?)", (parametro,))
    c.execute("SELECT descr FROM bot WHERE LOWER(nombre) LIKE LOWER(?) ORDER BY nombre='parametro' ASC", (f"%{parametro.replace(' ', '%')}%",))
    resultado = c.fetchone()

    # Responder al usuario con el resultado
    bot.send_chat_action(message.chat.id, "typing")
    if resultado:
        bot.reply_to(message, "{}".format(resultado[0]))
    else:
        bot.reply_to(message, "No se encontró resultado para esta consulta, verifica que la estés realizando correctamente.")
# Cierra la conexión a la base de datos
    c.close()
    conn.close()

# Definir un controlador predeterminado para mensajes que no sean comandos
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_invalid_command(message):
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(message, "Lo siento, no entendí ese comando. Por favor, usa uno de los comandos disponibles o revisa la especificación del bot para obtener más información.")


# Ejecuta el bot
if __name__ == '__main__':
    print('Bot Iniciado')
    bot.infinity_polling()