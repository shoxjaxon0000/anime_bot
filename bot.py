import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.constants import ChatMemberStatus
from telegram.error import BadRequest, Forbidden
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

BOT_TOKEN = "8890938686:AAF35bXN90eNd2fRUFje12sZS0cL9LNDf7o"
BOT_USERNAME = "@Animez1_bot"

# ─────────────────────────────────────────────
# 📢 MAJBURIY OBUNA SOZLAMALARI
# ─────────────────────────────────────────────
# Bot kanalga ADMIN qilib qo'shilgan bo'lishi SHART, aks holda
# a'zolikni tekshira olmaydi.
#
# CHANNEL_ID  -> kanalning ID raqami (masalan: -1001234567890)
#                Buni bilish uchun: kanalga biror xabarni botga forward qiling
#                yoki @username_to_id_bot kabi yordamchi botlardan foydalaning.
# CHANNEL_URL -> foydalanuvchi bosadigan obuna havolasi (https://t.me/...)
# CHANNEL_NAME-> tugmada ko'rinadigan nom
#
# Yana kanal qo'shish kerak bo'lsa, shu ro'yxatga yana bitta dict qo'shing.
# ─────────────────────────────────────────────

MAJBURIY_KANALLAR = [
    {
        "channel_id": -1003817068566,          # ← o'zingizning kanal ID'ingizni kiriting
        "url": "https://t.me/Animeztv1",     # ← obuna havolasi
        "name": "📢 Kanalimiz",                  # ← tugma nomi
    },
]

# ─────────────────────────────────────────────
# RASM FILE_ID OLISH:
# Botga rasm yuboring → bot PHOTO FILE_ID ni beradi
# Shu file_id ni "rasm" maydoniga kiriting
# ─────────────────────────────────────────────

ANIMALAR = [
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 1 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2018",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIBP2olZQWp61sfn8FYJlzHR1bkL23vAAIBHWsbntspSWKxxku7y2i0AQADAgADeQADOwQ",  # ← botga rasm yuboring, file_id ni shu yerga kiriting
        "qismlar": [
            ("1-qism","BAACAgIAAxkBAAOmaiQ-TTBlJTedh37EJ1lQCALOTMsAAuikAAKe2yFJceK8xOoUnHY7BA"),
            ("2-qism","BAACAgIAAxkBAAOsaiRVgiGA_oaWELYMhoCC5GSLDyUAAgOmAAKe2yFJUW4ZKdcuJqg7BA"),
            ("3-qism","BAACAgIAAxkBAAOuaiRVxC_eE_ZMecFNn5WqpIqLxqAAAgamAAKe2yFJCWy93UCaqQs7BA"),
            ("4-qism","BAACAgIAAxkBAAPaaiRxtyP15OZJCbx7R13UH1j01RIAAlynAAKe2yFJpXT67IegR9A7BA"),
            ("5-qism","BAACAgIAAxkBAAPcaiRyWvMPMX1vluW7CHF_i62lfPAAAm-nAAKe2yFJv1S5LOlchio7BA"),
            ("6-qism","BAACAgIAAxkBAAPeaiRynKHdEgGA81ywOVxpyvClclIAAnOnAAKe2yFJ9WEBY31cMS47BA"),
            ("7-qism","BAACAgIAAxkBAAPgaiR0CzxU31HRe1uqLj6F6TyfG3MAAoenAAKe2yFJAwABpFp0AouPOwQ"),
            ("8-qism","BAACAgIAAxkBAAPiaiR0M8WsaBFZulR6_jayYF6h5ugAAoinAAKe2yFJYyeMlcESQKg7BA"),
            ("9-qism","BAACAgIAAxkBAAPkaiR0WBQmJJU_IhirZUqJ4bx8tpQAAoynAAKe2yFJcNpQ4ryVnFw7BA"),
            ("10-qism","BAACAgIAAxkBAAPmaiR0dXaQSlS9G23qvCwzC_fUNkkAAo2nAAKe2yFJ57ZY1G8TqhU7BA"),
            ("11-qism","BAACAgIAAxkBAAPoaiR0j9U_PiY8P1p0LPfyMRtJqz8AApCnAAKe2yFJOu8G1pxYbC47BA"),
            ("12-qism","BAACAgIAAxkBAAPqaiR00f9I0Qk1cqfiqUjkPtZFbM0AApenAAKe2yFJCvYKJS_YZp47BA"),
            ("13-qism","BAACAgIAAxkBAAPsaiR0_l1TSrzJIMi4U7K6M1O2UdgAApmnAAKe2yFJWTsqnJ5rOi87BA"),
            ("14-qism","BAACAgIAAxkBAAPvaiR1SZZQb202hg5QCBv_h4Kqw8wAAqCnAAKe2yFJ-aHIoiFcHdE7BA"),
            ("15-qism","BAACAgIAAxkBAAPxaiR1Z2-oXyL7Kf6ItwHUSzORVf4AAqKnAAKe2yFJ4cr9bxMl_YU7BA"),
            ("16-qism","BAACAgIAAxkBAAP0aiR12dGyeHZDayzYuy6wZoS0C2YAAqenAAKe2yFJ6L0ePRgLJNg7BA"),
            ("17-qism","BAACAgIAAxkBAAP6aiR2O2CmRQtdjYDqW_oB8EM8MWQAAqynAAKe2yFJ2bNVtnrpaeA7BA"),
            ("18-qism","BAACAgIAAxkBAAP8aiR2WbM8qNI2zR1ry8_bwG9xkg4AAq-nAAKe2yFJx5k3MzMzyXM7BA"),
            ("19-qism","BAACAgIAAxkBAAP-aiR2equGuS8_c-ItN68yKYivXnsAArGnAAKe2yFJuNSC_yt8eTU7BA"),
            ("20-qism","BAACAgIAAxkBAAIBAAFqJHabqzJVF7Lmf62kAuWqBiqd2wACtqcAAp7bIUmopOc9FDPI_zsE"),
            ("21-qism","BAACAgIAAxkBAAIBAmokdsWTdaJSLKx6FoVifn9N04CIAAK5pwACntshSUz-V6h-QzfEOwQ"),
            ("22-qism","BAACAgIAAxkBAAIBBGokdvDHlQey1HxAxjYvxUfp5LzNAAK7pwACntshSciZho1PxSjzOwQ"),
            ("23-qism","BAACAgIAAxkBAAIBBmokdwT_f4jyMXg72PkV2e2uo4-1AAK8pwACntshSYUduPu11pU7OwQ"),
            ("24-qism","BAACAgIAAxkDAAOJaiQkyHp2c1eowp91fxfZ3Eqmhj4AAuIVAAJhoDBKwsu7vNH0EuM7BA"),
        ],
    },
    {
        "nomi": "Shilliq kundaligi",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2018",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIBQWolZRdWAAGMqNm0SLn0KY_rD7fMHQACAh1rG57bKUldorQ01Mle4gEAAwIAA3kAAzsE",  # ← botga rasm yuboring, file_id ni shu yerga kiriting
        "qismlar": [
            ("1-qism","BAACAgIAAxkBAAO1aiRYEpuXnJAo3V0HvnVkhQXZjCYAAh-mAAKe2yFJEsCjWsR_JKE7BA"),
            ("2-qism","BAACAgIAAxkBAAPCaiRbZPHM6wFvC-PATQR7ghDhTmUAAmKmAAKe2yFJN7McGc5YrH07BA"),
            ("3-qism","BAACAgIAAxkBAAPEaiRbdj_p3z1RztvPpIVSc5PcGn4AAmamAAKe2yFJuDMIfuwrWhg7BA"),
            ("4-qism","BAACAgIAAxkBAAPMaiReoOSbioskpal7ElxF1OHKTGoAAoumAAKe2yFJwjcfI0MAAS4rOwQ"),
            ("5-qism","BAACAgIAAxkBAAPOaiRexmgBu-9i01iGt_dzU_0GvhYAAo6mAAKe2yFJ94nPI85-gGw7BA"),
            ("6-qism","BAACAgIAAxkBAAPYaiRf0bKXIo99U8ZUMoNmUbyh4XYAAqOmAAKe2yFJaJ8BYgsz7lc7BA"),
            ("7-qism","BAACAgIAAxkBAAPIaiReS6cBz-SOGMomCJm85eBjpIMAAoSmAAKe2yFJLYjtEFAwJEg7BA"),
            ("8-qism","BAACAgIAAxkBAAPSaiRfiFxQgEoRQRXeD2xNB5gEQZwAAp6mAAKe2yFJszdi2s0vrUU7BA"),
            ("9-qism","BAACAgIAAxkBAAPUaiRfqOpIAAFw8Quk1gs2c0pnARvcAAKfpgACntshSeKe4h-WWHTmOwQ"),
            ("10-qism","BAACAgIAAxkBAAPKaiRec0Cg7FaZaWd7nlPFHNPh0ssAAoemAAKe2yFJDAsrnCMXxy47BA"),
            ("11-qism","BAACAgIAAxkBAAPGaiReCqI0E-WhF-POS4VjjPwWZPEAAoGmAAKe2yFJWSNa_Kc7F4U7BA"),
            ("12-qism","BAACAgIAAxkBAAPWaiRfuW3vkHYTVTdkbokOLYc1PoIAAqGmAAKe2yFJjtHX4pBHaIw7BA"),
        ],
    },
     {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida ovil",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2018 kuz",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIBu2oppToia9q9wx7R2_eEY8or_U93AAJFHWsbTV5JSc7qaCicv392AQADAgADeQADOwQ",  # ← botga rasm yuboring, file_id ni shu yerga kiriting
        "qismlar": [
            ("1-qism","BAACAgIAAxkBAAIBhGompzz11QZhadIPTt8gzkruonEfAAKsXwACXfoYSD6_xJ7H-npdOwQ"),
            ("2-qism","BAACAgIAAxkBAAIBhmomp0Jr_Zu3XuRpvEuchw_JB4W2AAK0XwACXfoYSPCboS8kzJLJOwQ"),
            ("3-qism","BAACAgIAAxkBAAIBiGomp2dXQEvOAAF1kJnmRNDW7LpGngACuV8AAl36GEhNinWFR0n7azsE"),
            ("4-qism","BAACAgIAAxkBAAIBimomp8xRRubyVFPn738XT3T-3SzLAAK-XwACXfoYSC1NkKzLD68NOwQ"),
            ("5-qism","BAACAgIAAxkBAAIBjGomp9SO2PTKgd0rG5ZaMjG6PaOiAALFXwACXfoYSLpgPhbBioy6OwQ"),
            ("6-qism","BAACAgIAAxkBAAIBjmomp9mXibY0VXxkLrMS5eNAwCkjAALLXwACXfoYSNXPB6UAAZL4kjsE"),
        ],
    },
     {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 2 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2021",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIBvWoppbN_ejcyww49xlN9pU9N5NKJAAJIHWsbTV5JSQkMzSdDep9YAQADAgADeQADOwQ",  # ← botga rasm yuboring, file_id ni shu yerga kiriting
        "qismlar": [
            ("1-qism","BAACAgIAAxkBAAIBv2oppkgGdXg47WBrysDFt5dB-bnbAALPXwACXfoYSGQKhXihPWsqOwQ"),
            ("2-qism","BAACAgIAAxkBAAIBwWopplP9Ef0H2fzNCmLSJ7ljIAkRAALUXwACXfoYSJmgUL-KEVhsOwQ"),
            ("3-qism","BAACAgIAAxkBAAIBw2opplmTLwXZm2NWrwyLXVa3xs5DAALhXwACXfoYSMInYfQfba17OwQ"),
            ("4-qism","BAACAgIAAxkBAAIBxWoppq-vfjeJRm_79YTUIg3H0AtnAALzXwACXfoYSJYcuCNpjttEOwQ"),
            ("5-qism","BAACAgIAAxkBAAIBx2opprRiGg6FC5gZ5Cwd9y7gbeeDAAL3XwACXfoYSKQ3zRcWLVITOwQ"),
            ("6-qism","BAACAgIAAxkBAAIByWopprnozyuPDqzJkfPGJ8LEXTGGAANgAAJd-hhIFJPEovKrtps7BA"),
            ("7-qism","BAACAgIAAxkBAAIBy2opp2Ge25WdiBJrsiVHnXg3UnD_AAIhYAACXfoYSEvUSvR_OG1QOwQ"),
            ("8-qism","BAACAgIAAxkBAAIBzWopp2boIsFS7YAzqmsktYlQTMRrAAIlYAACXfoYSHGxr1KMx2uqOwQ"),
            ("9-qism","BAACAgIAAxkBAAIBz2opp2sntZSgnhWFX04UyMfXuMXCAAJBYAACXfoYSKLaIX6kUcu_OwQ"),
            ("10-qism","BAACAgIAAxkBAAIB0Wopp2_fqUYt3SfDiVw4uoswwgo6AAJHYAACXfoYSE9dGmAQ0jM8OwQ"),
            ("11-qism","BAACAgIAAxkBAAIB02opp3R2qod619Erguab1ov5EOIjAAJUYAACXfoYSGrGusZQRT-JOwQ"),
            ("12-qism","BAACAgIAAxkBAAIB1Wopp3i0W8ML-7pYBla0OCo3H4J_AAJmYAACXfoYSM5UFaWGQx1JOwQ"),
            ("13-qism","BAACAgIAAxkBAAIB12opqEGb8I19fhE4nTK8BrUxXX9jAAJwYAACXfoYSDAwCHSTCBm3OwQ"),
            ("14-qism","BAACAgIAAxkBAAIB2WopqEdg5p8OrwtjtotkI4IXnpLLAAJyYAACXfoYSE5_Dvpu_OzAOwQ"),
            ("15-qism","BAACAgIAAxkBAAIB22opqE2IEkF4WXU2VLTmtg_YBUdRAAKTYAACXfoYSL-SQ2nboYHgOwQ"),
            ("16-qism","BAACAgIAAxkBAAIB3WopqFLmQb5k_Nxm-nV5SDM-WwMKAAKZYAACXfoYSPWjivFBN1ukOwQ"),
            ("17-qism","BAACAgIAAxkBAAIB32opqFfksoPxQnYLj313deerSuszAAKfYAACXfoYSCbl42E2U26rOwQ"),
            ("18-qism","BAACAgIAAxkBAAIB4WopqFu2B9jpYLQrnxWZIg7jRqxwAAKpYAACXfoYSJw456BrjEqsOwQ"),
            ("19-qism","BAACAgIAAxkBAAICK2op0GM1Q-FGW-nHPvwNtftTeMDjAAKwYAACXfoYSH4qeJXAqDokOwQ"),
            ("20-qism","BAACAgIAAxkBAAICLWop0GnO-OI442XAc1zhGjl9gSecAAK4YAACXfoYSLM3sI_CnpEuOwQ"),
            ("21-qism","BAACAgIAAxkBAAICL2op0G1hhbJMpHrmVsAWQiOXGLbrAALgYAACXfoYSPS4cNse57ooOwQ"),
            ("22-qism","BAACAgIAAxkBAAICMWop0HJbKxSkaaeFrYzkW85hA5WgAALkYAACXfoYSPAFj7HqC-yHOwQ"),
            ("23-qism","BAACAgIAAxkBAAICM2op0HfVNmzggqwE95x3DvVpRfmnAALsYAACXfoYSNAlw9JU9NiMOwQ"),
            ("24-qism","BAACAgIAAxkBAAICNWop0H31rIcy50J3oRAxIp_TdIH3AAIGYQACXfoYSP-F3EPAwfZfOwQ"),
        ],
    },
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida ovli 2 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2023",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAICN2op0S7JDCROzCB5VFhFsQfAbiiaAAJmFWsbu-nRSjeA4rz6UTxMAQADAgADeQADOwQ",  # ← botga rasm yuboring, file_id ni shu yerga kiriting
        "qismlar": [
            ("1-qism","BAACAgIAAxkBAAICOWop0TXvZCz9od1PeQ16flxFCwW7AAIsYQACXfoYSPX1fZ2x2hDfOwQ"),
            ("2-qism","BAACAgIAAxkBAAICO2op0TpHUBWjx5uYQNVU-nuU-UpLAAIvYQACXfoYSBtCxnwzdjwAATsE"),
            ("3-qism","BAACAgIAAxkBAAICPWop0UDF6_rLXhjqJneOqSXXako2AAI8YQACXfoYSI-hg3n27cCOOwQ"),
        ],
    },
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 1-film",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2024",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAICP2op0ctKketzAuGUqhuBNQXIp1JjAAJtFWsbu-nRSi7ZwOHn3fscAQADAgADeQADOwQ",  # ← botga rasm yuboring, file_id ni shu yerga kiriting
        "qismlar": [
            ("1-flim","BAACAgIAAxkBAAICQWop0dA0YlJQ2iZ4BzYVccJq9hMpAAJtYQACXfoYSOwCOCyTCB8-OwQ"),
        ],
    },
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 3 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2024",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAICQ2op08ahCNXUvXa-0EaiKdczEEkFAAJ2FWsbu-nRSt0XVDI8PIZqAQADAgADeQADOwQ",  # ← botga rasm yuboring, file_id ni shu yerga kiriting
        "qismlar": [
            ("1-qism","BAACAgIAAxkBAAICRWop09Sr9f6UE36e9ISkSu5e7NQcAAJwYQACXfoYSG8wBvVT6vpMOwQ"),
            ("2-qism","BAACAgIAAxkBAAICRmop09QOtR_4lze3uK8UtjKNBUWmAAJ3YQACXfoYSM3nWoBPhgevOwQ"),
            ("3-qism","BAACAgIAAxkBAAICR2op09S8-KxhM3RZD4roKC_WK2OpAAJ5YQACXfoYSFYHOXBvP_v-OwQ"),
            ("4-qism","BAACAgIAAxkBAAICUWop1AoO5vwo9J_FZF1qSOLzNuR1AAKBYQACXfoYSHwJaPepZ7tsOwQ"),
            ("5-qism","BAACAgIAAxkBAAICU2op1A-PsDN4oJAUYosflJPEWb5bAAKDYQACXfoYSPM3vA1FZYpEOwQ"),
            ("6-qism","BAACAgIAAxkBAAICVWop1BQx3SLvz3grMX4AAU5-e-ORuAAClmEAAl36GEiYUfhoAVsHJzsE"),
            ("7-qism","BAACAgIAAxkBAAICV2op1Boo9PEQ3IQPimnkRa5sfKS8AAKZYQACXfoYSAho6Gb9i7xKOwQ"),
            ("8-qism","BAACAgIAAxkBAAICWWop1D0eT-1Nu-qII84nyXZ36jlzAAK7YQACXfoYSPFyov568sIYOwQ"),
            ("9-qism","BAACAgIAAxkBAAICW2op1TpTngcTISg_2ogj9JJ26mm4AAK-YQACXfoYSDgR1ddjw2BMOwQ"),
            ("10-qism","BAACAgIAAxkBAAICXWop1UE5J8uYF9gsvbY9m9fAA1crAALDYQACXfoYSAgr_4uhcHzROwQ"),
            ("11-qism","BAACAgIAAxkBAAICX2op1UeQlAHV1paxoV-VTsexjGHQAALGYQACXfoYSPxWVr6Y12R-OwQ"),
            ("12-qism","BAACAgIAAxkBAAICYWop1UzVoXcLNyDr19t29ncKds0AA-ZhAAJd-hhIOkv_kUW6z0k7BA"),
            ("13-qism","BAACAgIAAxkBAAICY2op1VL2zWOEnjxZAihzunO2JJYjAAL0YQACXfoYSEk8VGWm3cMaOwQ"),
            ("14-qism","BAACAgIAAxkBAAICZWop1VcLgyaFb9DhoQUBUX1rQjmoAANiAAJd-hhIgESocC0W5YA7BA"),
            ("15-qism","BAACAgIAAxkBAAICZ2op1VsFSRSM_C_JKpNn4sVkq-GIAAIEYgACXfoYSHjdBxoAAersAzsE"),
            ("16-qism","BAACAgIAAxkBAAICaWop1WGDQVAeieiWSnsyPdTSnWceAAIFYgACXfoYSH0R1y97gn87OwQ"),
            ("17-qism","BAACAgIAAxkBAAICa2op1ePAj9CDKlJfkLBaNhm-_ry2AAIJYgACXfoYSMhx_O4sndYXOwQ"),
            ("18-qism","BAACAgIAAxkBAAICbWop1ej7rbtHtcDfxcoVJ_BIhsm9AAIMYgACXfoYSAQuIc60nFk2OwQ"),
            ("19-qism","BAACAgIAAxkBAAICb2op1eysab-7-05fzyyryEiFruyXAAIOYgACXfoYSHBROt74dXSYOwQ"),
            ("20-qism","BAACAgIAAxkBAAICcWop1fG2jCDsCQJdCr1hZqhuwUxAAAIQYgACXfoYSMOZ09mtJbMuOwQ"),
            ("21-qism","BAACAgIAAxkBAAICc2op1fbnyrjmaGjFExsc9la2HZOfAAISYgACXfoYSMnJnm4S9MDnOwQ"),
            ("22-qism","BAACAgIAAxkBAAICdWop1fvV41XBR97wnb2JtnCWFSGIAAITYgACXfoYSFdJd0foYjgWOwQ"),
            ("23-qism","BAACAgIAAxkBAAICd2op1gAB4cnBgrIzsU4vBOGFWgqWRQACFWIAAl36GEiAuc2mU3IoKjsE"),
            ("24-qism","BAACAgIAAxkBAAICeWop1gaIW9P4Lm9NJWOWpuZQ1pydAAIWYgACXfoYSOyW0HEZHDBCOwQ"),
        ],
    },
    
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 4 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2026",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIDPmoyVMA8uqNSYTVMWhxvLtx0fC0BAALGGWsb6huQSeCDCz0T-ggcAQADAgADeQADPAQ",  # ← botga rasm yuboring, file_id ni shu yerga kiriting
        "qismlar": [
            ("1-qism","BAACAgQAAxkBAAIDXmoyXppvApUqAdFQ7N9X0VND0BAGAAIIHgAC3LWxUgSNea-cxv1UPAQ"),
            ("2-qism","BAACAgIAAxkBAAIDYmoyXzXgDc3KfRCegG-6UeOmhotpAAI7owACeDnIStwpcFcdwzDvPAQ"),
            ("3-qism","BAACAgQAAxkBAAIDZGoyX5kjAAFxgQ7CNCVMWRSEtw3oGQAC8RsAAhEpSFOXZdTxtpC2iDwE"),
            ("4-qism","BAACAgQAAxkBAAIDZmoyX6MvCn17aXnFOo7hA_VesFDWAAIBHQACAsuZU_8MG9joplePPAQ"),
            ("5-qism","BAACAgQAAxkBAAIDaGoyX6ko9ZmVEA9M6uVzxbQDLYY_AAJeHgACZW1BUE8Kt6vxxWVkPAQ"),
            ("6-qism","BAACAgQAAxkBAAIDamoyX67KgME6nU_zHdNBnot16PVyAAJFHQACcotoUJ6YMfb0ab67PAQ"),
            ("7-qism","BAACAgQAAxkBAAIDbGoyX7QmTue1iJAfLbvGI5FKkO8bAAK5HQACn-a4UMg4OJhADlchPAQ"),
            ("8-qism","BAACAgQAAxkBAAIDbmoyX7jGsB__GzyzY9BsnWxy0gEuAAJvHQACNskYUY9RvxMhLkbJPAQ"),
            ("9-qism","BAACAgQAAxkBAAIDcGoyX7283ez6nIn9E5u22mzWdqGJAAKpHwACls5QUXsqR1uO3MTXPAQ"),
            ("10-qism","BAACAgQAAxkBAAIDcmoyX8JqgTW-cdTOw-pNoKwDpgrzAAJJHQACdAABYVHd7EEHh6f7jzwE"),
            # ("11-qism","BAACAgIAAxkBAAICX2op1UeQlAHV1paxoV-VTsexjGHQAALGYQACXfoYSPxWVr6Y12R-OwQ"),
            # ("12-qism","BAACAgIAAxkBAAICYWop1UzVoXcLNyDr19t29ncKds0AA-ZhAAJd-hhIOkv_kUW6z0k7BA"),
            # ("13-qism","BAACAgIAAxkBAAICY2op1VL2zWOEnjxZAihzunO2JJYjAAL0YQACXfoYSEk8VGWm3cMaOwQ"),
            # ("14-qism","BAACAgIAAxkBAAICZWop1VcLgyaFb9DhoQUBUX1rQjmoAANiAAJd-hhIgESocC0W5YA7BA"),
            # ("15-qism","BAACAgIAAxkBAAICZ2op1VsFSRSM_C_JKpNn4sVkq-GIAAIEYgACXfoYSHjdBxoAAersAzsE"),
            # ("16-qism","BAACAgIAAxkBAAICaWop1WGDQVAeieiWSnsyPdTSnWceAAIFYgACXfoYSH0R1y97gn87OwQ"),
            # ("17-qism","BAACAgIAAxkBAAICa2op1ePAj9CDKlJfkLBaNhm-_ry2AAIJYgACXfoYSMhx_O4sndYXOwQ"),
            # ("18-qism","BAACAgIAAxkBAAICbWop1ej7rbtHtcDfxcoVJ_BIhsm9AAIMYgACXfoYSAQuIc60nFk2OwQ"),
            # ("19-qism","BAACAgIAAxkBAAICb2op1eysab-7-05fzyyryEiFruyXAAIOYgACXfoYSHBROt74dXSYOwQ"),
            # ("20-qism","BAACAgIAAxkBAAICcWop1fG2jCDsCQJdCr1hZqhuwUxAAAIQYgACXfoYSMOZ09mtJbMuOwQ"),
            # ("21-qism","BAACAgIAAxkBAAICc2op1fbnyrjmaGjFExsc9la2HZOfAAISYgACXfoYSMnJnm4S9MDnOwQ"),
            # ("22-qism","BAACAgIAAxkBAAICdWop1fvV41XBR97wnb2JtnCWFSGIAAITYgACXfoYSFdJd0foYjgWOwQ"),
            # ("23-qism","BAACAgIAAxkBAAICd2op1gAB4cnBgrIzsU4vBOGFWgqWRQACFWIAAl36GEiAuc2mU3IoKjsE"),
            # ("24-qism","BAACAgIAAxkBAAICeWop1gaIW9P4Lm9NJWOWpuZQ1pydAAIWYgACXfoYSOyW0HEZHDBCOwQ"),
        ],
    },
        {
        "nomi": "Tayoq va qilich 1 fasl",
        "janrlari": "Janrlari: Sarguzasht, Ramantik",
        "yili": "2025",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIDPmoyVMA8uqNSYTVMWhxvLtx0fC0BAALGGWsb6huQSeCDCz0T-ggcAQADAgADeQADPAQ",  # ← botga rasm yuboring, file_id ni shu yerga kiriting
        "qismlar": [
            ("1-qism","BAACAgQAAxkBAAIDXmoyXppvApUqAdFQ7N9X0VND0BAGAAIIHgAC3LWxUgSNea-cxv1UPAQ"),
            ("2-qism","BAACAgIAAxkBAAIDYmoyXzXgDc3KfRCegG-6UeOmhotpAAI7owACeDnIStwpcFcdwzDvPAQ"),
            ("3-qism","BAACAgQAAxkBAAIDZGoyX5kjAAFxgQ7CNCVMWRSEtw3oGQAC8RsAAhEpSFOXZdTxtpC2iDwE"),
            ("4-qism","BAACAgQAAxkBAAIDZmoyX6MvCn17aXnFOo7hA_VesFDWAAIBHQACAsuZU_8MG9joplePPAQ"),
            ("5-qism","BAACAgQAAxkBAAIDaGoyX6ko9ZmVEA9M6uVzxbQDLYY_AAJeHgACZW1BUE8Kt6vxxWVkPAQ"),
            ("6-qism","BAACAgQAAxkBAAIDamoyX67KgME6nU_zHdNBnot16PVyAAJFHQACcotoUJ6YMfb0ab67PAQ"),
            ("7-qism","BAACAgQAAxkBAAIDbGoyX7QmTue1iJAfLbvGI5FKkO8bAAK5HQACn-a4UMg4OJhADlchPAQ"),
            ("8-qism","BAACAgQAAxkBAAIDbmoyX7jGsB__GzyzY9BsnWxy0gEuAAJvHQACNskYUY9RvxMhLkbJPAQ"),
            ("9-qism","BAACAgQAAxkBAAIDcGoyX7283ez6nIn9E5u22mzWdqGJAAKpHwACls5QUXsqR1uO3MTXPAQ"),
            ("10-qism","BAACAgQAAxkBAAIDcmoyX8JqgTW-cdTOw-pNoKwDpgrzAAJJHQACdAABYVHd7EEHh6f7jzwE"),
            ("11-qism","BAACAgIAAxkBAAICX2op1UeQlAHV1paxoV-VTsexjGHQAALGYQACXfoYSPxWVr6Y12R-OwQ"),
            ("12-qism","BAACAgIAAxkBAAICYWop1UzVoXcLNyDr19t29ncKds0AA-ZhAAJd-hhIOkv_kUW6z0k7BA"),
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


# ═════════════════════════════════════════════
# 📢 MAJBURIY OBUNA YORDAMCHI FUNKSIYALARI
# ═════════════════════════════════════════════

OBUNA_BOLMAGAN_HOLATLAR = {
    ChatMemberStatus.LEFT,
    ChatMemberStatus.BANNED,
}


async def obunani_tekshir(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> list:
    """
    Foydalanuvchini barcha majburiy kanallarga a'zoligini tekshiradi.
    Qaytaradi: a'zo BO'LMAGAN kanallar ro'yxati (bo'sh ro'yxat = hammasiga a'zo).
    """
    obuna_bolmagan = []

    for kanal in MAJBURIY_KANALLAR:
        try:
            a_zo = await context.bot.get_chat_member(
                chat_id=kanal["channel_id"], user_id=user_id
            )
            if a_zo.status in OBUNA_BOLMAGAN_HOLATLAR:
                obuna_bolmagan.append(kanal)
        except BadRequest as e:
            # Bot kanalda admin emas yoki kanal ID noto'g'ri bo'lsa shu yerga tushadi.
            # Bunday holatda foydalanuvchini bloklab qo'ymaslik uchun
            # ushbu kanalni "tekshirib bo'lmadi" deb belgilab, lekin xatoni logga yozamiz.
            logger.error(
                f"Kanal tekshirishda xatolik (chat_id={kanal['channel_id']}): {e}. "
                f"Bot shu kanalda ADMIN ekanligini va channel_id to'g'riligini tekshiring."
            )
        except Forbidden as e:
            logger.error(
                f"Botga kanal taqiqlangan (chat_id={kanal['channel_id']}): {e}"
            )

    return obuna_bolmagan


def obuna_klaviaturasi(obuna_bolmagan_kanallar: list, tekshir_callback: str):
    """Obuna bo'lmagan kanallar uchun tugmalar va 'Tekshirish' tugmasini yaratadi."""
    keyboard = [
        [InlineKeyboardButton(kanal["name"], url=kanal["url"])]
        for kanal in obuna_bolmagan_kanallar
    ]
    keyboard.append(
        [InlineKeyboardButton("✅ Obuna bo'ldim, tekshirish", callback_data=tekshir_callback)]
    )
    return InlineKeyboardMarkup(keyboard)


async def obuna_talab_qil(message_yoki_query, obuna_bolmagan_kanallar: list, tekshir_callback: str, edit: bool = False):
    """Foydalanuvchiga obuna bo'lish haqida xabar va tugmalarni ko'rsatadi."""
    matn = (
        "🔒 *Botdan foydalanish uchun avval quyidagi kanal(lar)ga obuna bo'ling:*\n\n"
        "Obuna bo'lgach, pastdagi *\"✅ Obuna bo'ldim, tekshirish\"* tugmasini bosing."
    )
    markup = obuna_klaviaturasi(obuna_bolmagan_kanallar, tekshir_callback)

    if edit:
        try:
            await message_yoki_query.edit_text(matn, parse_mode="Markdown", reply_markup=markup)
        except BadRequest:
            # Agar oldingi xabar rasm bo'lsa, edit_text ishlamaydi -> yangi xabar yuboramiz
            await message_yoki_query.reply_text(matn, parse_mode="Markdown", reply_markup=markup)
    else:
        await message_yoki_query.reply_text(matn, parse_mode="Markdown", reply_markup=markup)


# ═════════════════════════════════════════════


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
            f"{a['nomi']}",
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
    user_id = update.effective_user.id
    args = context.args

    # ── Majburiy obunani tekshirish ──
    obuna_bolmagan = await obunani_tekshir(user_id, context)
    if obuna_bolmagan:
        # Keyinroq "Tekshirish" tugmasi bosilganda qaysi anime ochilishi kerakligini eslab qolamiz
        if args:
            context.user_data["pending_start_arg"] = args[0]
        else:
            context.user_data.pop("pending_start_arg", None)

        await obuna_talab_qil(update.message, obuna_bolmagan, tekshir_callback="tekshir_start")
        return
    # ── ───────────────────────── ──

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
    data = query.data
    user_id = update.effective_user.id

    # ── "Tekshirish" tugmasi bosilganda ──
    if data == "tekshir_start":
        obuna_bolmagan = await obunani_tekshir(user_id, context)

        if obuna_bolmagan:
            await query.answer("❌ Hali barcha kanallarga obuna bo'lmadingiz!", show_alert=True)
            await obuna_talab_qil(
                query.message, obuna_bolmagan, tekshir_callback="tekshir_start", edit=True
            )
            return

        await query.answer("✅ Obuna tasdiqlandi!")

        # Agar foydalanuvchi /start anime_<index> orqali kirmoqchi bo'lgan bo'lsa, shuni ochamiz
        pending = context.user_data.pop("pending_start_arg", None)
        if pending and pending.startswith("anime_"):
            try:
                anime_index = int(pending.split("_")[1])
                if 0 <= anime_index < len(ANIMALAR):
                    await query.message.delete()
                    await anime_qismlari_yuborish(query.message, anime_index)
                    return
            except (ValueError, IndexError):
                pass

        await query.message.edit_text(
            "🎌 Anime botiga *xush kelibsiz!*",
            parse_mode="Markdown",
        )
        return
    # ── ───────────────────────────── ──

    # ── Boshqa har qanday tugma uchun ham obunani tekshiramiz ──
    obuna_bolmagan = await obunani_tekshir(user_id, context)
    if obuna_bolmagan:
        await query.answer("❌ Avval kanal(lar)ga obuna bo'ling!", show_alert=True)
        await obuna_talab_qil(
            query.message, obuna_bolmagan, tekshir_callback="tekshir_start", edit=True
        )
        return
    # ── ──────────────────────────────────────────────────── ──

    await query.answer()

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
                    f"Nomi: *{anime['nomi']}*\n\n"
                    f"Qism: {qism_nomi}\n\n"
                    f"Janrlari: *{anime['janrlari']}*\n\n"
                    f"Yili: *{anime['yili']}*\n\n"
                    f"Sifat: *{anime['sifat']}*\n\n"                
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
