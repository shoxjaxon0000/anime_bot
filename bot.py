import os
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

BOT_TOKEN = os.environ["BOT_TOKEN"]
BOT_USERNAME = "@Animezona1_bot"

# ─────────────────────────────────────────────
# 📢 MAJBURIY OBUNA SOZLAMALARI
# Bot kanalga ADMIN qilib qo'shilgan bo'lishi SHART.
# ─────────────────────────────────────────────

MAJBURIY_KANALLAR = [
    {
        "channel_id": -1003817068566,
        "url": "https://t.me/Animeztv1",
        "name": "📢 Kanalimiz",
    },
    {
        "channel_id": -1004095884973,
        "url": "https://t.me/homeproduct1566",
        "name": "📢 Kanalimiz",
    },
]

# ─────────────────────────────────────────────
# RASM FILE_ID OLISH:
# Botga rasm yuboring → bot PHOTO FILE_ID ni beradi
# ─────────────────────────────────────────────

ANIMALAR = [
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 1 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2018",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAMMatTBtVnHLvvmv52LkxHlwynEhiQAAg7oMRv6ByFI3G0cU7lMoucBAAMCAAN5AAM9BA",
        "qismlar": [
            ("1-qism","BAACAgIAAxkBAAMJatTBSqjMq4Bh2e1EXst5H_Btf_YAAs5BAAKwWAhL3B66thRqcy09BA"),
            ("2-qism","BAACAgIAAxkBAAMVatTGlStz9hCzT1-89TAwfvHsx2MAAl9FAALgASFLwf_a9uVZaeI9BA"),
            ("3-qism","BAACAgIAAxkBAAMXatTHRMMzHStOYt_JO_egiFVwT9QAAoNHAAJS_jlLbLW-fRbnpO89BA"),
            ("4-qism","BAACAgIAAxkBAAMZatTH33DCqB531CjIqLkLYgLKgOsAAvpHAAJdkUlLtBxuCn-HypE9BA"),
            ("5-qism","BAACAgIAAxkBAAMbatTH5U3pa1-kUoB9UJB-1Mp3GK0AAqBGAAL10FhLxRKVg64Zztk9BA"),
            ("6-qism","BAACAgIAAxkBAAMdatTH7TF_AAEGVVULo3E4PzQBAYaVAAJeRQAC9dBgS0tbdWq9TLxhPQQ"),
            ("7-qism","BAACAgIAAxkBAAMfatTH85u9-G9vOXtvMusCG0ebw4YAAldCAAJ7UXhL_tRkT-dbGXM9BA"),
            ("8-qism","BAACAgIAAxkBAAMhatTH-c83mCQvT_EthVt89NyDMRgAAtpDAAJilYhLdwVP-5lb2aA9BA"),
            ("9-qism","BAACAgIAAxkBAAMjatTIAAFbXLgm7PbEqbJWPPMYVkR8AAKdQAACfUigS2edqrHC7XSDPQQ"),
            ("10-qism","BAACAgIAAxkBAAMlatTIBjPRjQ2hq0a_D4UmxWAUSpsAArJFAAK587FL93rQ0TRJV6E9BA"),
            ("11-qism","BAACAgIAAxkBAAMnatTIDiCfqMEapA1ABtJTBCKZV0YAAh1KAALiq7lL3EfQD_GAuwE9BA"),
            ("12-qism","BAACAgIAAxkBAAMpatTIFDoLyIVhWcHlUzSdCXkG1VQAAkFHAAJp29BLBhLaf9oiDkM9BA"),
            ("13-qism","BAACAgIAAxkBAAMratTIG46bYl6-kTboRDrBrTvGZ2MAAq9NAAKr6NlLUUs2cA95qAM9BA"),
            ("14-qism","BAACAgIAAxkBAAMtatTJB3R61dn7cyr--z_ZwyPECGoAAmZHAALqSuBLpi1n6VrNaVg9BA"),
            ("15-qism","BAACAgIAAxkBAAMvatTJGh11c9m0nOHDR3hsXc6hMKQAAoI_AAKtHvFLufh6XTCp2PA9BA"),
            ("16-qism","BAACAgIAAxkBAAMwatTJGkYfrg6fZ7kuwYf2Tj3R8msAAv9GAAIlbPlLiASLO-3i5bs9BA"),
            ("17-qism","BAACAgIAAxkBAAM5atTJ8eHYISPyUFyR8IoifFXzbnsAAqFLAAIOaQABSGTt0M2NGJobPQQ"),
            ("18-qism","BAACAgIAAxkBAAM7atTJ-53jA-3-d1ZQ_YSFJkYyQMEAAj08AAIjfxlIn2795jnoH8g9BA"),
            ("19-qism","BAACAgIAAxkBAAM9atTKBMGF95qll1DsfnvVXWtonQoAAjFAAAIjfyFI2s5JDkvUeB09BA"),
            ("20-qism","BAACAgIAAxkBAAM_atTKEevcj5Lqo-0f53RBW_mE98cAAuhDAAISFiBI4znleU0CfjQ9BA"),
            ("21-qism","BAACAgIAAxkBAANBatTKGPiMF8qW3DVZ1Y2BiW2Uc60AAiBAAALiODFI_NJRqLA9L3g9BA"),
            ("22-qism","BAACAgIAAxkBAANDatTKIFuYLmEc3MT45eoMi-7okGAAAvZPAAJQk0hIYarln3BacrU9BA"),
            ("23-qism","BAACAgIAAxkBAANFatTKKJtEcMqO4PgziA-KuiIPnzYAAqdDAAJN71hI7eSUHqUtZWU9BA"),
            ("24-qism","BAACAgIAAxkBAANHatTK1dhop6D45Pu6I0Cqge7ysekAAr2aAAL4HLFKCYLzFqNGHUo9BA"),
        ],
    },
    {
        "nomi": "Shilliq kundaligi",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2018",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAP9atjciDv3wf54e_7xb9X4mZ9gntQAArcVaxtGOjBJNLNQ7_36ZuMBAAMCAAN5AAM9BA",
        "qismlar": [
            ("1-qism","BAACAgIAAxkBAAPjatja93N7s51sakYSdjlPmpSnYcUAAmIoAALCFBBLF9fu7OuoljA9BA"),
            ("2-qism","BAACAgIAAxkBAAPlatjbKfWbPILkNFRNxt6zNtACD9EAAsopAAI-ehBL5DW7Dtr81js9BA"),
            ("3-qism","BAACAgIAAxkBAAPnatjbM7fBWkQluTHI-y5pCXucf3YAAg0nAAIKX0lLd61tbYE72FE9BA"),
            ("4-qism","BAACAgIAAxkBAAPpatjbOekUOjh3ZIRR0DI94q_YjLMAAo4lAAJ2k7BL4A_5vsfXpZ89BA"),
            ("5-qism","BAACAgIAAxkBAAPratjbPn4JJZ1ufA_c1CBpz_QAAdtVAAJZKwACkElQSlFsx9PDLxevPQQ"),
            ("6-qism","BAACAgIAAxkBAAPtatjbRFxLcb8QDOdaC50RZcUAAY6cAAJRKgACsHbQSpmMDmfWKELMPQQ"),
            ("7-qism","BAACAgIAAxkBAAPvatjbc5EPmUA9MpW9eOyAFKfEYmoAAsEsAAJP53lLR6wbQ_d1INE9BA"),
            ("8-qism","BAACAgIAAxkBAAPxatjb4PPyOpk2M8gBHOrxEgW3lz4AAmkzAAKWYwhJB0WC4hS09Vc9BA"),
            ("9-qism","BAACAgIAAxkBAAPzatjb5hqoJlsGnYWclhA4O8ksytsAAmc8AALN6-hJY1ssiKlk9nw9BA"),
            ("10-qism","BAACAgIAAxkBAAP1atjb6tA5f0I90NBKpMU0z6ULo3gAAno5AALbpAFKkKsbqSE8lUY9BA"),
            ("11-qism","BAACAgIAAxkBAAP3atjb71aiYQABSJmX3pVLUSgmIlzMAAKbMgAC4ScYSvd2kf_8aCDzPQQ"),
            ("12-qism","BAACAgIAAxkBAAP5atjb9PXVpPLOHn56kcTaEICq4bgAAmg3AALOeSFKC2jBM538DOI9BA"),
        ],
    },
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida ovil",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2018 kuz",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAP_atjcnHb0IUnS-22MITwjmXjnD6YAAkUdaxtNXklJ4V3PO9osuJUBAAMCAAN5AAM9BA",
        "qismlar": [
            ("1-qism","BAACAgIAAxkBAAIBAWrY3TKhY7tl88zjCF0ejmMZfPQ3AAKsXwACXfoYSMBcOyX6uL2YPQQ"),
            ("2-qism","BAACAgIAAxkBAAIBA2rY3Tl0AaG14rLdiSFHxHIRB3iiAAK0XwACXfoYSE6GQWE-qXhWPQQ"),
            ("3-qism","BAACAgIAAxkBAAIBBWrY3T40On8M9sjbm2jNcfJwDicXAAK5XwACXfoYSBpRb8qVlU6DPQQ"),
            ("4-qism","BAACAgIAAxkBAAIBB2rY3USX-IWpArDF7MGzP4VmIYY0AAK-XwACXfoYSMc_1TSq3IiVPQQ"),
            ("5-qism","BAACAgIAAxkBAAIBCWrY3UnEL9qD4-9eDh2JFB-fQLQ7AALFXwACXfoYSOCJFvIr25ITPQQ"),
            ("6-qism","BAACAgIAAxkBAAIBC2rY3U_pod-N9oPF8426AUvK76o1AALLXwACXfoYSE5Trm43I3l8PQQ"),
        ],
    },
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 2 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2021",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIBDWrY3kMz6YQMwESk7P8f8e0R2P5AAAJIHWsbTV5JSXx8z8CxNt1WAQADAgADeQADPQQ",
        "qismlar": [
            ("1-qism",""),
            ("2-qism",""),
            ("3-qism",""),
            ("4-qism",""),
            ("5-qism",""),
            ("6-qism",""),
            ("7-qism",""),
            ("8-qism",""),
            ("9-qism",""),
            ("10-qism",""),
            ("11-qism",""),
            ("12-qism",""),
            ("13-qism",""),
            ("14-qism",""),
            ("15-qism",""),
            ("16-qism",""),
            ("17-qism",""),
            ("18-qism",""),
            ("19-qism",""),
            ("20-qism",""),
            ("21-qism",""),
            ("22-qism",""),
            ("23-qism",""),
            ("24-qism",""),
        ],
    },
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida ovli 2 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2023",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIBD2rY3kn69yoP_Nm6AAGvBC9UOlJP6AACZhVrG7vp0Upht7c7rkzH3QEAAwIAA3kAAz0E",
        "qismlar": [
            ("1-qism",""),
            ("2-qism",""),
            ("3-qism",""),
        ],
    },
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 1-film",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2024",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIBEWrY3k6p56T5LhWw6gpcosaKz49IAAJtFWsbu-nRSibZqr8uw3WKAQADAgADeQADPQQ",
        "qismlar": [
            ("1-flim",""),
        ],
    },
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 3 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2024",
        "sifat": "720p, 1080p",
        "rasm": "",
        "qismlar": [
            ("1-qism",""),
            ("2-qism",""),
            ("3-qism",""),
            ("4-qism",""),
            ("5-qism",""),
            ("6-qism",""),
            ("7-qism",""),
            ("8-qism",""),
            ("9-qism",""),
            ("10-qism",""),
            ("11-qism",""),
            ("12-qism",""),
            ("13-qism",""),
            ("14-qism",""),
            ("15-qism",""),
            ("16-qism",""),
            ("17-qism",""),
            ("18-qism",""),
            ("19-qism",""),
            ("20-qism",""),
            ("21-qism",""),
            ("22-qism",""),
            ("23-qism",""),
            ("24-qism",""),
        ],
    },
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 4 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2026",
        "sifat": "720p, 1080p",
        "rasm": "",
        "qismlar": [
            ("1-qism",""),
            ("2-qism",""),
            ("3-qism",""),
            ("4-qism",""),
            ("5-qism",""),
            ("6-qism",""),
            ("7-qism",""),
            ("8-qism",""),
            ("9-qism",""),
            ("10-qism",""),
            ("11-qism",""),
        ],
    },
    {
        "nomi": "Tayoq va qilich 1 fasl",
        "janrlari": "Janrlari: Sarguzasht, Comedy, Fantasy, Ramantik",
        "yili": "2025",
        "sifat": "720p, 1080p",
        "rasm": "",
        "qismlar": [
            ("1-qism",""),
            ("2-qism",""),
            ("3-qism",""),
            ("4-qism",""),
            ("5-qism",""),
            ("6-qism",""),
            ("7-qism",""),
            ("8-qism",""),
            ("9-qism",""),
            ("10-qism",""),
            ("11-qism",""),
            ("12-qism",""),
        ],
    },
    {
        "nomi": "Tayoq va qilich 2 fasl",
        "janrlari": "Janrlari: Sarguzasht, Comedy, Fantasy, Ramantik",
        "yili": "2026",
        "sifat": "720p, 1080p",
        "rasm": "",
        "qismlar": [
            ("1-qism",""),
            ("2-qism",""),
            ("3-qism",""),
            ("4-qism",""),
            ("5-qism",""),
            ("6-qism",""),
            ("7-qism",""),
            ("8-qism",""),
            ("9-qism",""),
            ("10-qism",""),
        ],
    },
    {
        "nomi": "Oy Sayohati O'zga Dunyo 1 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2022",
        "sifat": "720p, 1080p",
        "rasm": "",
        "qismlar": [
            ("1-qism",""),
            ("2-qism",""),
            ("3-qism",""),
            ("4-qism",""),
            ("5-qism",""),
            ("6-qism",""),
            ("7-qism",""),
            ("8-qism",""),
            ("9-qism",""),
            ("10-qism",""),
            ("11-qism",""),
            ("12-qism",""),
        ],
    },
    {
        "nomi": "Oy Sayohati O'zga Dunyo 2 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2025",
        "sifat": "720p, 1080p",
        "rasm": "",
        "qismlar": [
            ("1-qism",""),
            ("2-qism",""),
            ("3-qism",""),
            ("4-qism",""),
            ("5-qism",""),
            ("6-qism",""),
            ("7-qism",""),
            ("8-qism",""),
            ("9-qism",""),
            ("10-qism",""),
            ("11-qism",""),
            ("12-qism",""),
            ("13-qism",""),
            ("14-qism",""),
            ("15-qism",""),
            ("16-qism",""),
            ("17-qism",""),
            ("18-qism",""),
            ("19-qism",""),
            ("20-qism",""),
            ("21-qism",""),
            ("22-qism",""),
            ("23-qism",""),
            ("24-qism",""),
            ("25-qism",""),
        ],
    },
    {
        "nomi": "Iblislar Qotili 1 fasl",
        "janrlari": "Janrlari: Sarguzasht, Fantastika, Komediya, Iblislar, Tarixiy",
        "yili": "2019",
        "sifat": " 480, 720p",
        "rasm": "",
        "qismlar": [
            ("1-qism","),
            ("2-qism",""),
            ("3-qism",""),
            ("4-qism",""),
            ("5-qism",""),
            ("6-qism",""),
            ("7-qism",""),
            ("8-qism",""),
            ("9-qism",""),
            ("10-qism",""),
            ("11-qism",""),
            ("12-qism",""),
            ("13-qism",""),
            ("14-qism",""),
            ("15-qism",""),
            ("16-qism",""),
            ("17-qism",""),
            ("18-qism",""),
            ("19-qism",""),
            ("20-qism",""),
            ("21-qism",""),
            ("22-qism",""),
            ("23-qism",""),
            ("24-qism",""),
            ("25-qism",""),
            ("26-qism",""),
        ],
    },
    {
        "nomi": "Iblislar Qotili Cheksiz poezd 1 film",
        "janrlari": "Janrlari: Sarguzasht, Fantastika, Komediya, Iblislar, Tarixiy",
        "yili": "2020",
        "sifat": "720p, 1080p",
        "rasm": "",
        "qismlar": [
            ("1-film",""),
        ],
    },
    {
        "nomi": "Iblislar Qotili 2 fasl",
        "janrlari": "Janrlari: Sarguzasht, Fantastika, Komediya, Iblislar, Tarixiy",
        "yili": "2021",
        "sifat": "720p, 1080p",
        "rasm": "",
        "qismlar": [
            ("1-qism",""),
            ("2-qism",""),
            ("3-qism",""),
            ("4-qism",""),
            ("5-qism",""),
            ("6-qism",""),
            ("7-qism",""),
            ("8-qism",""),
            ("9-qism",""),
            ("10-qism",""),
            ("11-qism",""),
        ],
    },
    {
        "nomi": "Iblislar Qotili 3 fasl",
        "janrlari": "Janrlari: Sarguzasht, Fantastika, Komediya, Iblislar, Tarixiy",
        "yili": "2023",
        "sifat": "720p, 1080p",
        "rasm": "",
        "qismlar": [
            ("1-qism",""),
            ("2-qism",""),
            ("3-qism",""),
            ("4-qism",""),
            ("5-qism",""),
            ("6-qism",""),
            ("7-qism",""),
            ("8-qism",""),
            ("9-qism",""),
            ("10-qism",""),
            ("11-qism",""),
        ],
    },
    {
        "nomi": "Iblislar Qotili 4 fasl",
        "janrlari": "Janrlari: Sarguzasht, Fantastika, Komediya, Iblislar, Tarixiy",
        "yili": "2025",
        "sifat": "720p, 1080p",
        "rasm": "",
        "qismlar": [
            ("1-qism",""),
            ("2-qism",""),
            ("3-qism",""),
            ("4-qism",""),
            ("5-qism",""),
            ("6-qism",""),
            ("7-qism",""),
            ("8-qism",""),
        ],
    },
    {
        "nomi": "Iblislar Qotili Cheksiz poezd 2 film",
        "janrlari": "Janrlari: Sarguzasht, Fantastika, Komediya, Iblislar, Tarixiy",
        "yili": "2026",
        "sifat": "720p, 1080p",
        "rasm": "",
        "qismlar": [
            ("2-film",""),
        ],
    },
    {
        "nomi": "Qalqon qahramon 1 fasl",
        "janrlari": "Janrlari: Ekshen, Romantika, Boshqa dunyo, Drama, Sarguzasht",
        "yili": "2025",
        "sifat": "720p, 1080p",
        "rasm": "",
        "qismlar": [
            ("1-qism",""),
            ("2-qism",""),
            ("3-qism",""),
            ("4-qism",""),
            ("5-qism",""),
            ("6-qism",""),
            ("7-qism",""),
            ("8-qism",""),
            ("9-qism",""),
            ("10-qism",""),
            ("11-qism",""),
            ("12-qism",""),
            ("13-qism",""),
            ("14-qism",""),
            ("15-qism",""),
            ("16-qism",""),
            ("17-qism",""),
            ("18-qism",""),
            ("19-qism",""),
            ("20-qism",""),
            ("21-qism",""),
            ("22-qism",""),
            ("23-qism",""),
            ("24-qism",""),
            ("25-qism",""),
        ],
    },
    # Keyingi anime qo'shish uchun:
    # {
    #     "nomi": "Boshqa Anime",
    #     "janrlari": "Janrlari: ...",
    #     "yili": "2026",
    #     "sifat": "720p, 1080p",
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
            # Oldingi xabar rasm bo'lsa yoki matn o'zgarmagan bo'lsa -> yangi xabar yuboramiz
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
    # Vercel'da xotira saqlanmaydi, shuning uchun anime raqamini tugma ichiga yozamiz.
    obuna_bolmagan = await obunani_tekshir(user_id, context)
    if obuna_bolmagan:
        cb = f"tekshir_{args[0]}" if args else "tekshir_"
        await obuna_talab_qil(update.message, obuna_bolmagan, tekshir_callback=cb)
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
    if data.startswith("tekshir_"):
        obuna_bolmagan = await obunani_tekshir(user_id, context)

        if obuna_bolmagan:
            await query.answer("❌ Hali barcha kanallarga obuna bo'lmadingiz!", show_alert=True)
            await obuna_talab_qil(
                query.message, obuna_bolmagan, tekshir_callback=data, edit=True
            )
            return

        await query.answer("✅ Obuna tasdiqlandi!")

        pending = data[len("tekshir_"):]
        if pending.startswith("anime_"):
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
            query.message, obuna_bolmagan, tekshir_callback="tekshir_", edit=True
        )
        return
    # ── ──────────────────────────────────────────────────── ──

    await query.answer()

    if data.startswith("video_"):
        try:
            parts = data.split("_")
            anime_index = int(parts[1])
            qism_index = int(parts[2])

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


def build_application():
    """Vercel (webhook) uchun: updater=None, chunki Vercel doimiy server emas."""
    app = ApplicationBuilder().token(BOT_TOKEN).updater(None).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.VIDEO | filters.PHOTO, get_file_id))
    return app
