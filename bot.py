import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ─────────────────────────────────────────────
# ✏️ SOZLAMALAR
# ─────────────────────────────────────────────

BOT_TOKEN = "8890938686:AAGAI677Up8O3M8xcdEJtf9l4rBfbN5368Y"
BOT_USERNAME = "@Animez1_bot"

# ─────────────────────────────────────────────
# RASM FILE_ID OLISH:
# Botga rasm yuboring → bot PHOTO FILE_ID ni beradi
# Shu file_id ni "rasm" maydoniga kiriting
# ─────────────────────────────────────────────

ANIMALAR = [
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 1 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "Yili: 2021",
        "sifat": "Sifat: 720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIBP2olZQWp61sfn8FYJlzHR1bkL23vAAIBHWsbntspSWKxxku7y2i0AQADAgADeQADOwQ",  # ← botga rasm yuboring, file_id ni shu yerga kiriting
        "qismlar": [
            ("1-qism",  "BAACAgIAAxkBAAOmaiQ-TTBlJTedh37EJ1lQCALOTMsAAuikAAKe2yFJceK8xOoUnHY7BA"),
            ("2-qism",  "BAACAgIAAxkBAAOsaiRVgiGA_oaWELYMhoCC5GSLDyUAAgOmAAKe2yFJUW4ZKdcuJqg7BA"),
            ("3-qism",  "BAACAgIAAxkBAAOuaiRVxC_eE_ZMecFNn5WqpIqLxqAAAgamAAKe2yFJCWy93UCaqQs7BA"),
            ("4-qism",  "BAACAgIAAxkBAAPaaiRxtyP15OZJCbx7R13UH1j01RIAAlynAAKe2yFJpXT67IegR9A7BA"),
            ("5-qism",  "BAACAgIAAxkBAAPcaiRyWvMPMX1vluW7CHF_i62lfPAAAm-nAAKe2yFJv1S5LOlchio7BA"),
            ("6-qism",  "BAACAgIAAxkBAAPeaiRynKHdEgGA81ywOVxpyvClclIAAnOnAAKe2yFJ9WEBY31cMS47BA"),
            ("7-qism",  "BAACAgIAAxkBAAPgaiR0CzxU31HRe1uqLj6F6TyfG3MAAoenAAKe2yFJAwABpFp0AouPOwQ"),
            ("8-qism",  "BAACAgIAAxkBAAPiaiR0M8WsaBFZulR6_jayYF6h5ugAAoinAAKe2yFJYyeMlcESQKg7BA"),
            ("9-qism",  "BAACAgIAAxkBAAPkaiR0WBQmJJU_IhirZUqJ4bx8tpQAAoynAAKe2yFJcNpQ4ryVnFw7BA"),
            ("10-qism", "BAACAgIAAxkBAAPmaiR0dXaQSlS9G23qvCwzC_fUNkkAAo2nAAKe2yFJ57ZY1G8TqhU7BA"),
            ("11-qism", "BAACAgIAAxkBAAPoaiR0j9U_PiY8P1p0LPfyMRtJqz8AApCnAAKe2yFJOu8G1pxYbC47BA"),
            ("12-qism", "BAACAgIAAxkBAAPqaiR00f9I0Qk1cqfiqUjkPtZFbM0AApenAAKe2yFJCvYKJS_YZp47BA"),
            ("13-qism", "BAACAgIAAxkBAAPsaiR0_l1TSrzJIMi4U7K6M1O2UdgAApmnAAKe2yFJWTsqnJ5rOi87BA"),
            ("14-qism", "BAACAgIAAxkBAAPvaiR1SZZQb202hg5QCBv_h4Kqw8wAAqCnAAKe2yFJ-aHIoiFcHdE7BA"),
            ("15-qism", "BAACAgIAAxkBAAPxaiR1Z2-oXyL7Kf6ItwHUSzORVf4AAqKnAAKe2yFJ4cr9bxMl_YU7BA"),
            ("16-qism", "BAACAgIAAxkBAAP0aiR12dGyeHZDayzYuy6wZoS0C2YAAqenAAKe2yFJ6L0ePRgLJNg7BA"),
            ("17-qism", "BAACAgIAAxkBAAP6aiR2O2CmRQtdjYDqW_oB8EM8MWQAAqynAAKe2yFJ2bNVtnrpaeA7BA"),
            ("18-qism", "BAACAgIAAxkBAAP8aiR2WbM8qNI2zR1ry8_bwG9xkg4AAq-nAAKe2yFJx5k3MzMzyXM7BA"),
            ("19-qism", "BAACAgIAAxkBAAP-aiR2equGuS8_c-ItN68yKYivXnsAArGnAAKe2yFJuNSC_yt8eTU7BA"),
            ("20-qism", "BAACAgIAAxkBAAIBAAFqJHabqzJVF7Lmf62kAuWqBiqd2wACtqcAAp7bIUmopOc9FDPI_zsE"),
            ("21-qism", "BAACAgIAAxkBAAIBAmokdsWTdaJSLKx6FoVifn9N04CIAAK5pwACntshSUz-V6h-QzfEOwQ"),
            ("22-qism", "BAACAgIAAxkBAAIBBGokdvDHlQey1HxAxjYvxUfp5LzNAAK7pwACntshSciZho1PxSjzOwQ"),
            ("23-qism", "BAACAgIAAxkBAAIBBmokdwT_f4jyMXg72PkV2e2uo4-1AAK8pwACntshSYUduPu11pU7OwQ"),
            ("24-qism", "BAACAgIAAxkDAAOJaiQkyHp2c1eowp91fxfZ3Eqmhj4AAuIVAAJhoDBKwsu7vNH0EuM7BA"),
        ],
    },
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 1 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "Yili: 2021",
        "sifat": "Sifat: 720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIBQWolZRdWAAGMqNm0SLn0KY_rD7fMHQACAh1rG57bKUldorQ01Mle4gEAAwIAA3kAAzsE",  # ← botga rasm yuboring, file_id ni shu yerga kiriting
        "qismlar": [
            ("1-qism",  "BAACAgIAAxkBAAO1aiRYEpuXnJAo3V0HvnVkhQXZjCYAAh-mAAKe2yFJEsCjWsR_JKE7BA"),
            ("2-qism",  "BAACAgIAAxkBAAPCaiRbZPHM6wFvC-PATQR7ghDhTmUAAmKmAAKe2yFJN7McGc5YrH07BA"),
            ("3-qism",  "BAACAgIAAxkBAAPEaiRbdj_p3z1RztvPpIVSc5PcGn4AAmamAAKe2yFJuDMIfuwrWhg7BA"),
            ("4-qism",  "BAACAgIAAxkBAAPMaiReoOSbioskpal7ElxF1OHKTGoAAoumAAKe2yFJwjcfI0MAAS4rOwQ"),
            ("5-qism",  "BAACAgIAAxkBAAPOaiRexmgBu-9i01iGt_dzU_0GvhYAAo6mAAKe2yFJ94nPI85-gGw7BA"),
            ("6-qism",  "BAACAgIAAxkBAAPYaiRf0bKXIo99U8ZUMoNmUbyh4XYAAqOmAAKe2yFJaJ8BYgsz7lc7BA"),
            ("7-qism",  "BAACAgIAAxkBAAPIaiReS6cBz-SOGMomCJm85eBjpIMAAoSmAAKe2yFJLYjtEFAwJEg7BA"),
            ("8-qism",  "BAACAgIAAxkBAAPSaiRfiFxQgEoRQRXeD2xNB5gEQZwAAp6mAAKe2yFJszdi2s0vrUU7BA"),
            ("9-qism",  "BAACAgIAAxkBAAPUaiRfqOpIAAFw8Quk1gs2c0pnARvcAAKfpgACntshSeKe4h-WWHTmOwQ"),
            ("10-qism", "BAACAgIAAxkBAAPKaiRec0Cg7FaZaWd7nlPFHNPh0ssAAoemAAKe2yFJDAsrnCMXxy47BA"),
            ("11-qism", "BAACAgIAAxkBAAPGaiReCqI0E-WhF-POS4VjjPwWZPEAAoGmAAKe2yFJWSNa_Kc7F4U7BA"),
            ("12-qism", "BAACAgIAAxkBAAPWaiRfuW3vkHYTVTdkbokOLYc1PoIAAqGmAAKe2yFJjtHX4pBHaIw7BA"),
        ],
    },
     {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 1 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "Yili: 2021",
        "sifat": "Sifat: 720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIBu2oppToia9q9wx7R2_eEY8or_U93AAJFHWsbTV5JSc7qaCicv392AQADAgADeQADOwQQ",  # ← botga rasm yuboring, file_id ni shu yerga kiriting
        "qismlar": [
            ("1-qism",  "BAACAgIAAxkBAAIBhGompzz11QZhadIPTt8gzkruonEfAAKsXwACXfoYSD6_xJ7H-npdOwQ"),
            ("2-qism",  "BAACAgIAAxkBAAIBhmomp0Jr_Zu3XuRpvEuchw_JB4W2AAK0XwACXfoYSPCboS8kzJLJOwQ"),
            ("3-qism",  "BAACAgIAAxkBAAIBiGomp2dXQEvOAAF1kJnmRNDW7LpGngACuV8AAl36GEhNinWFR0n7azsE"),
            ("4-qism",  "BAACAgIAAxkBAAIBimomp8xRRubyVFPn738XT3T-3SzLAAK-XwACXfoYSC1NkKzLD68NOwQ"),
            ("5-qism",  "BAACAgIAAxkBAAIBjGomp9SO2PTKgd0rG5ZaMjG6PaOiAALFXwACXfoYSLpgPhbBioy6OwQ"),
            ("6-qism",  "BAACAgIAAxkBAAIBjmomp9mXibY0VXxkLrMS5eNAwCkjAALLXwACXfoYSNXPB6UAAZL4kjsE"),
        ],
    },
     {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 1 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "Yili: 2021",
        "sifat": "Sifat: 720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIBvWoppbN_ejcyww49xlN9pU9N5NKJAAJIHWsbTV5JSQkMzSdDep9YAQADAgADeQADOwQ",  # ← botga rasm yuboring, file_id ni shu yerga kiriting
        "qismlar": [
            ("1-qism",  "BAACAgIAAxkBAAIBv2oppkgGdXg47WBrysDFt5dB-bnbAALPXwACXfoYSGQKhXihPWsqOwQ"),
            ("2-qism",  "BAACAgIAAxkBAAIBwWopplP9Ef0H2fzNCmLSJ7ljIAkRAALUXwACXfoYSJmgUL-KEVhsOwQ"),
            ("3-qism",  "BAACAgIAAxkBAAIBw2opplmTLwXZm2NWrwyLXVa3xs5DAALhXwACXfoYSMInYfQfba17OwQ"),
            ("4-qism",  "BAACAgIAAxkBAAIBxWoppq-vfjeJRm_79YTUIg3H0AtnAALzXwACXfoYSJYcuCNpjttEOwQ"),
            ("5-qism",  "BAACAgIAAxkBAAIBx2opprRiGg6FC5gZ5Cwd9y7gbeeDAAL3XwACXfoYSKQ3zRcWLVITOwQ"),
            ("6-qism",  "BAACAgIAAxkBAAIByWopprnozyuPDqzJkfPGJ8LEXTGGAANgAAJd-hhIFJPEovKrtps7BA"),
            ("7-qism",  "BAACAgIAAxkBAAIBy2opp2Ge25WdiBJrsiVHnXg3UnD_AAIhYAACXfoYSEvUSvR_OG1QOwQ"),
            ("8-qism",  "BAACAgIAAxkBAAIBzWopp2boIsFS7YAzqmsktYlQTMRrAAIlYAACXfoYSHGxr1KMx2uqOwQ"),
            ("9-qism",  "BAACAgIAAxkBAAIBz2opp2sntZSgnhWFX04UyMfXuMXCAAJBYAACXfoYSKLaIX6kUcu_OwQ"),
            ("10-qism", "BAACAgIAAxkBAAIB0Wopp2_fqUYt3SfDiVw4uoswwgo6AAJHYAACXfoYSE9dGmAQ0jM8OwQ"),
            ("11-qism", "BAACAgIAAxkBAAIB02opp3R2qod619Erguab1ov5EOIjAAJUYAACXfoYSGrGusZQRT-JOwQ"),
            ("12-qism", "BAACAgIAAxkBAAIB1Wopp3i0W8ML-7pYBla0OCo3H4J_AAJmYAACXfoYSM5UFaWGQx1JOwQ"),
            ("13-qism", "BAACAgIAAxkBAAIB12opqEGb8I19fhE4nTK8BrUxXX9jAAJwYAACXfoYSDAwCHSTCBm3OwQ"),
            ("14-qism", "BAACAgIAAxkBAAIB2WopqEdg5p8OrwtjtotkI4IXnpLLAAJyYAACXfoYSE5_Dvpu_OzAOwQ"),
            ("15-qism", "BAACAgIAAxkBAAIB22opqE2IEkF4WXU2VLTmtg_YBUdRAAKTYAACXfoYSL-SQ2nboYHgOwQ"),
            ("16-qism", "BAACAgIAAxkBAAIB3WopqFLmQb5k_Nxm-nV5SDM-WwMKAAKZYAACXfoYSPWjivFBN1ukOwQ"),
            ("17-qism", "BAACAgIAAxkBAAIB32opqFfksoPxQnYLj313deerSuszAAKfYAACXfoYSCbl42E2U26rOwQ"),
            ("18-qism", "BAACAgIAAxkBAAIB4WopqFu2B9jpYLQrnxWZIg7jRqxwAAKpYAACXfoYSJw456BrjEqsOwQ"),
            ("19-qism", ""),
            ("20-qism", ""),
            ("21-qism", ""),
            ("22-qism", ""),
            ("23-qism", ""),
            ("24-qism", ""),
        ],
    },
    # Keyingi anime qo'shish uchun:
    # {
    #     "nomi": "Boshqa Anime",
    #     "emoji": "⭐",
    #     "tavsif": "Tavsif matni",
    #     "rasm": "PHOTO_FILE_ID_BU_YERGA",
    #     "qismlar": [
    #         ("1-qism", "FILE_ID_BU_YERGA"),
    #     ],
    # },
]

USTUN_SONI = 4

# ─────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def qismlar_klaviaturasi(anime_index: int):
    anime = ANIMALAR[anime_index]
    barcha = [
        InlineKeyboardButton(f"▶️ {nom}", callback_data=f"video_{anime_index}_{i}")
        for i, (nom, _) in enumerate(anime["qismlar"])
    ]
    keyboard = [
        barcha[i : i + USTUN_SONI]
        for i in range(0, len(barcha), USTUN_SONI)
    ]
    return InlineKeyboardMarkup(keyboard)


def animalar_klaviaturasi():
    keyboard = [
        [InlineKeyboardButton(
            f"{a['emoji']} {a['nomi']}",
            callback_data=f"anime_{i}"
        )]
        for i, a in enumerate(ANIMALAR)
    ]
    return InlineKeyboardMarkup(keyboard)


async def anime_qismlari_yuborish(update_or_message, anime_index: int, edit=False):
    anime = ANIMALAR[anime_index]
    matn = (
        f"Nomi: *{anime['nomi']}*\n\n"
        f"Janrlari: *{anime['janrlari']}*\n\n"
        f"Yili: *{anime['yili']}*\n\n"
        f"Sifat: *{anime['sifat']}*\n\n"
        f"Qism: *{len(anime['qismlar'])}*\n\n"
    )
    markup = qismlar_klaviaturasi(anime_index)
    rasm = anime.get("rasm")

    if edit:
        if rasm and not rasm.startswith("PHOTO_FILE_ID"):
            try:
                await update_or_message.edit_media(
                    media=InputMediaPhoto(media=rasm, caption=matn, parse_mode="Markdown"),
                    reply_markup=markup,
                )
                return
            except Exception:
                pass
        await update_or_message.edit_text(matn, parse_mode="Markdown", reply_markup=markup)
    else:
        if rasm and not rasm.startswith("PHOTO_FILE_ID"):
            await update_or_message.reply_photo(
                photo=rasm,
                caption=matn,
                parse_mode="Markdown",
                reply_markup=markup,
            )
        else:
            await update_or_message.reply_text(matn, parse_mode="Markdown", reply_markup=markup)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if args and args[0].startswith("anime_"):
        try:
            anime_index = int(args[0].split("_")[1])
            if 0 <= anime_index < len(ANIMALAR):
                await anime_qismlari_yuborish(update.message, anime_index)
                return
        except (ValueError, IndexError):
            pass

    await update.message.reply_text(
        "🎌 Anime botiga *xush kelibsiz!*",
        parse_mode="Markdown",
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("video_"):
        try:
            parts = data.split("_")
            anime_index = int(parts[1])
            qism_index  = int(parts[2])

            anime = ANIMALAR[anime_index]
            qism_nomi, file_id = anime["qismlar"][qism_index]

            await query.message.reply_video(
                video=file_id,
                caption=(
                    f"{anime['emoji']} *{anime['nomi']}* — {qism_nomi}\n\n"
                    f"▶️ Davom etish uchun keyingi qismni tanlang 👇"
                ),
                parse_mode="Markdown",
            )

        except (ValueError, IndexError) as e:
            logger.error(f"video_ xatolik: {e}")
            await query.answer("❌ Xatolik yuz berdi!", show_alert=True)

    elif data.startswith("anime_"):
        try:
            anime_index = int(data.split("_")[1])
            if 0 <= anime_index < len(ANIMALAR):
                await anime_qismlari_yuborish(query.message, anime_index, edit=True)
        except (ValueError, IndexError):
            await query.answer("❌ Xatolik!", show_alert=True)

    elif data == "back_main":
        await query.message.edit_text(
            "🎌 Anime botiga *xush kelibsiz!*\n\n📋 Qaysi animani ko'rmoqchisiz?",
            parse_mode="Markdown",
            reply_markup=animalar_klaviaturasi(),
        )


async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        file_id = update.message.video.file_id
        await update.message.reply_text(
            f"✅ *VIDEO FILE\\_ID:*\n`{file_id}`\n\n"
            f"⬆️ Shu file\\_id ni ANIMALAR ichiga kiriting.",
            parse_mode="Markdown",
        )
    elif update.message.photo:
        file_id = update.message.photo[-1].file_id
        await update.message.reply_text(
            f"✅ *PHOTO FILE\\_ID:*\n`{file_id}`\n\n"
            f"⬆️ Shu file\\_id ni ANIMALAR ichidagi *'rasm'* maydoniga kiriting.",
            parse_mode="Markdown",
        )


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.VIDEO | filters.PHOTO, get_file_id))

    logger.info("Bot ishga tushdi ✅")
    app.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=False)


if __name__ == "__main__":
    main()
