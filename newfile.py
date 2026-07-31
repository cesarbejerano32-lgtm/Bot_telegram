import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ====================== CONFIGURACIÓN ======================
TOKEN = "8632897212:AAGdwZlyfLf956fLB86Pst_FSkJlCzMvm9c"
ADMIN_ID = 7417314949          # Tu ID de Telegram
# ===========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Almacenamiento temporal
pedidos = []
valoraciones = []


# ====================== MENÚ PRINCIPAL ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📋 Catálogo de Servicios", callback_data="catalogo")],
        [InlineKeyboardButton("💳 Métodos de Pago", callback_data="pagos")],
        [InlineKeyboardButton("⭐ Valorar Servicio", callback_data="valorar")],
        [InlineKeyboardButton("ℹ️ Información", callback_data="info")],
    ]

    if update.effective_user and update.effective_user.id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("📊 Panel de Administrador", callback_data="admin")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    texto = (
        "¡Hola! 👋\n\n"
        "Bienvenido a mi bot de servicios digitales.\n"
        "¿En qué puedo ayudarte hoy?"
    )

    if update.message:
        await update.message.reply_text(texto, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(texto, reply_markup=reply_markup)


# ====================== CATÁLOGO ======================
async def mostrar_catalogo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("🤖 Bots para Telegram", callback_data="servicio_bots")],
        [InlineKeyboardButton("🐍 Programas en Python", callback_data="servicio_python")],
        [InlineKeyboardButton("⚙️ Automatizaciones", callback_data="servicio_auto")],
        [InlineKeyboardButton("⬅️ Volver al menú", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "📋 *Catálogo de Servicios*\n\nSelecciona el servicio que te interesa:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def detalle_servicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    servicios = {
        "servicio_bots": {
            "titulo": "🤖 Bots para Telegram",
            "desc": (
                "Desarrollo de bots profesionales:\n\n"
                "• Menús interactivos con botones\n"
                "• Sistemas de pedidos y notificaciones\n"
                "• Integración con pagos\n"
                "• Paneles de administrador\n\n"
                "Ideal para negocios que quieren automatizar la atención al cliente."
            ),
            "pedir": "pedir_bots"
        },
        "servicio_python": {
            "titulo": "🐍 Programas en Python",
            "desc": (
                "Programas y scripts a medida:\n\n"
                "• Automatización de tareas repetitivas\n"
                "• Extracción y análisis de datos\n"
                "• Herramientas de productividad\n"
                "• Scripts personalizados\n\n"
                "Soluciones eficientes y fáciles de usar."
            ),
            "pedir": "pedir_python"
        },
        "servicio_auto": {
            "titulo": "⚙️ Automatizaciones",
            "desc": (
                "Automatización de procesos:\n\n"
                "• Conexión entre aplicaciones\n"
                "• Flujos de trabajo automáticos\n"
                "• Notificaciones y reportes\n"
                "• Integraciones con APIs\n\n"
                "Haz que tu negocio trabaje solo."
            ),
            "pedir": "pedir_auto"
        }
    }

    serv = servicios[data]

    keyboard = [
        [InlineKeyboardButton("✅ Solicitar este servicio", callback_data=serv["pedir"])],
        [InlineKeyboardButton("⬅️ Volver al catálogo", callback_data="catalogo")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    texto = f"*{serv['titulo']}*\n\n{serv['desc']}"

    await query.edit_message_text(
        texto,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


# ====================== PROCESAR PEDIDO ======================
async def procesar_pedido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    usuario = query.from_user
    key = query.data

    nombres = {
        "pedir_bots": "🤖 Bots para Telegram",
        "pedir_python": "🐍 Programas en Python",
        "pedir_auto": "⚙️ Automatizaciones",
    }

    nombre_servicio = nombres.get(key, "Servicio")

    pedido = {
        "id": len(pedidos) + 1,
        "usuario_id": usuario.id,
        "nombre": usuario.full_name,
        "username": usuario.username,
        "servicio": nombre_servicio,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    pedidos.append(pedido)

    await query.edit_message_text(
        f"✅ *¡Pedido recibido!*\n\n"
        f"Has solicitado: *{nombre_servicio}*\n\n"
        f"En breve me pondré en contacto contigo.\n"
        f"¡Gracias por tu confianza! 🙌",
        parse_mode="Markdown"
    )

    mensaje_admin = (
        f"🛒 *NUEVO PEDIDO #{pedido['id']}*\n\n"
        f"👤 {usuario.full_name}\n"
        f"🆔 `{usuario.id}`\n"
        f"🔗 @{usuario.username if usuario.username else 'Sin username'}\n\n"
        f"📦 Servicio: *{nombre_servicio}*\n"
        f"📅 {pedido['fecha']}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=mensaje_admin, parse_mode="Markdown")


# ====================== MÉTODOS DE PAGO ======================
async def metodos_pago(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    texto = (
        "💳 *Métodos de Pago*\n\n"
        "Puedes pagarme de las siguientes formas:\n\n"
        "🟣 *QvaPay* (Recomendado)\n"
        "• La forma más fácil desde Cuba\n"
        "• Puedes pagar con saldo QvaPay o enviarme USDT\n\n"
        "🪙 *USDT*\n"
        "• Red TRC20 o BEP20\n\n"
        "Una vez confirmado el pedido te enviaré los datos exactos de pago."
    )

    keyboard = [
        [InlineKeyboardButton("🟣 Pagar con QvaPay", callback_data="pago_qvapay")],
        [InlineKeyboardButton("🪙 Pagar con USDT", callback_data="pago_usdt")],
        [InlineKeyboardButton("⬅️ Volver al menú", callback_data="menu")]
    ]

    await query.edit_message_text(texto, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


async def pago_qvapay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    texto = (
        "🟣 *Pago con QvaPay*\n\n"
        "Para pagarme con QvaPay tienes estas opciones:\n\n"
        "1️⃣ Envíame USDT a mi cuenta de QvaPay\n"
        "2️⃣ Genera un enlace de pago desde tu cuenta QvaPay\n\n"
        "Cuando estés listo para pagar, avísame y te envío los datos exactos (dirección + red)."
    )

    keyboard = [[InlineKeyboardButton("⬅️ Volver a Métodos de Pago", callback_data="pagos")]]
    await query.edit_message_text(texto, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


async def pago_usdt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    texto = (
        "🪙 *Pago con USDT*\n\n"
        "Puedes enviarme USDT de forma directa.\n\n"
        "📌 Redes aceptadas:\n"
        "• *TRC20* (Tron) → Recomendada (más barata)\n"
        "• *BEP20* (BSC)\n\n"
        "Cuando confirmemos el pedido te enviaré la dirección exacta de mi wallet en QvaPay.\n\n"
        "⚠️ Usa exactamente la misma red que te indique."
    )

    keyboard = [[InlineKeyboardButton("⬅️ Volver a Métodos de Pago", callback_data="pagos")]]
    await query.edit_message_text(texto, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


# ====================== SISTEMA DE VALORACIONES ======================
async def iniciar_valoracion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("⭐", callback_data="val_1"),
            InlineKeyboardButton("⭐⭐", callback_data="val_2"),
            InlineKeyboardButton("⭐⭐⭐", callback_data="val_3"),
        ],
        [
            InlineKeyboardButton("⭐⭐⭐⭐", callback_data="val_4"),
            InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="val_5"),
        ],
        [InlineKeyboardButton("⬅️ Cancelar", callback_data="menu")],
    ]
    await query.edit_message_text(
        "⭐ *Valorar el servicio*\n\n¿Qué puntuación me das?",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


async def guardar_valoracion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    estrellas = int(query.data.replace("val_", ""))
    usuario = query.from_user

    valoracion = {
        "usuario_id": usuario.id,
        "nombre": usuario.full_name,
        "estrellas": estrellas,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    valoraciones.append(valoracion)

    await query.edit_message_text(
        f"¡Gracias por tu valoración de {'⭐' * estrellas}!\n\nTu opinión me ayuda a mejorar. 🙏"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"⭐ *Nueva valoración*\n\n"
            f"👤 {usuario.full_name}\n"
            f"Puntuación: {'⭐' * estrellas} ({estrellas}/5)\n"
            f"📅 {valoracion['fecha']}"
        ),
        parse_mode="Markdown"
    )


# ====================== PANEL DE ADMINISTRADOR ======================
async def panel_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        await query.edit_message_text("⛔ No tienes permiso para acceder aquí.")
        return

    total_pedidos = len(pedidos)
    total_valoraciones = len(valoraciones)
    promedio = 0
    if valoraciones:
        promedio = sum(v["estrellas"] for v in valoraciones) / len(valoraciones)

    texto = (
        f"📊 *Panel de Administrador*\n\n"
        f"📦 Pedidos recibidos: *{total_pedidos}*\n"
        f"⭐ Valoraciones: *{total_valoraciones}*\n"
        f"📈 Promedio: *{promedio:.1f}/5*\n"
    )

    keyboard = [
        [InlineKeyboardButton("📋 Ver últimos pedidos", callback_data="admin_pedidos")],
        [InlineKeyboardButton("⭐ Ver valoraciones", callback_data="admin_valoraciones")],
        [InlineKeyboardButton("⬅️ Volver al menú", callback_data="menu")],
    ]
    await query.edit_message_text(texto, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


async def admin_pedidos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not pedidos:
        texto = "Aún no hay pedidos registrados."
    else:
        texto = "📋 *Últimos pedidos:*\n\n"
        for p in pedidos[-10:][::-1]:
            texto += (
                f"#{p['id']} - {p['servicio']}\n"
                f"👤 {p['nombre']} (`{p['usuario_id']}`)\n"
                f"📅 {p['fecha']}\n\n"
            )

    keyboard = [[InlineKeyboardButton("⬅️ Volver al panel", callback_data="admin")]]
    await query.edit_message_text(texto, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


async def admin_valoraciones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not valoraciones:
        texto = "Aún no hay valoraciones."
    else:
        texto = "⭐ *Últimas valoraciones:*\n\n"
        for v in valoraciones[-10:][::-1]:
            texto += f"{'⭐' * v['estrellas']} - {v['nombre']}\n📅 {v['fecha']}\n\n"

    keyboard = [[InlineKeyboardButton("⬅️ Volver al panel", callback_data="admin")]]
    await query.edit_message_text(texto, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


# ====================== INFORMACIÓN ======================
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    texto = (
        "ℹ️ *Información*\n\n"
        "Este bot fue creado como ejemplo profesional de automatización con Telegram.\n\n"
        "Servicios disponibles:\n"
        "• Bots para Telegram\n"
        "• Programas en Python\n"
        "• Automatizaciones\n\n"
        "¿Quieres un bot parecido para tu negocio? ¡Háblame!"
    )
    keyboard = [[InlineKeyboardButton("⬅️ Volver al menú", callback_data="menu")]]
    await query.edit_message_text(texto, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")


# ====================== MANEJADOR DE BOTONES ======================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "menu":
        await start(update, context)
    elif data == "catalogo":
        await mostrar_catalogo(update, context)
    elif data.startswith("servicio_"):
        await detalle_servicio(update, context)
    elif data.startswith("pedir_"):
        await procesar_pedido(update, context)
    elif data == "pagos":
        await metodos_pago(update, context)
    elif data == "pago_qvapay":
        await pago_qvapay(update, context)
    elif data == "pago_usdt":
        await pago_usdt(update, context)
    elif data == "valorar":
        await iniciar_valoracion(update, context)
    elif data.startswith("val_"):
        await guardar_valoracion(update, context)
    elif data == "admin":
        await panel_admin(update, context)
    elif data == "admin_pedidos":
        await admin_pedidos(update, context)
    elif data == "admin_valoraciones":
        await admin_valoraciones(update, context)
    elif data == "info":
        await info(update, context)


# ====================== MAIN ======================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot iniciado correctamente...")
    app.run_polling()


if __name__ == "__main__":
    main()