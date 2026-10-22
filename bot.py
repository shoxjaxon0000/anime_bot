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
    "channel_id": "@Animezonauz",
    "url": "https://t.me/Animezonauz",
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
            ("1-qism","BAACAgIAAxkBAAIBUmrZ4C3LT2GR5hV4xOz1DWxQh-PgAALplQACeHP5SgS-fENf4TY-PQQ"),
            ("2-qism","BAACAgIAAxkBAAIBVGrZ4DKfYSyCN1y-v0Q1QEXABYOjAALLkQACEoUISzqH1k5FGfBgPQQ"),
            ("3-qism","BAACAgIAAxkBAAIBVmrZ4DnIvzvA6ZyYrrWmM30TnoUWAAJHlgACLXkYS7eW3b5Pku-XPQQ"),
            ("4-qism","BAACAgIAAxkBAAIBWGrZ4EFSZSNLKIok_FGxOE44b1j7AAKUkwACcL45S9pdeVD07SXuPQQ"),
            ("5-qism","BAACAgIAAxkBAAIBWmrZ4Enx7-bP-pTuGacOZQteZVEIAAOWAAL2_0FLBUG7SaMkuFI9BA"),
            ("6-qism","BAACAgIAAxkBAAIBXGrZ4E6-BFZCIMZv80qfrV3CYcUtAAKmjwAC9v9JS6TfJBmyJV2ePQQ"),
            ("7-qism","BAACAgIAAxkBAAIBXmrZ4FmgyUA5d6KYMlG1q0E09cxtAAIsjQAC8drRS-xk6ND33RnmPQQ"),
            ("8-qism","BAACAgIAAxkBAAIBYGrZ4F45n9jAB20_PecGfbqfar1CAALvkAAChNvRS293oWqkfYJdPQQ"),
            ("9-qism","BAACAgIAAxkBAAIBYmrZ4GjsU4zo6fpYqciDDsgauZrEAALphwAChNvZS8aLPB1VIpQRPQQ"),
            ("10-qism","BAACAgIAAxkBAAIBZGrZ4G8d9xhj84YSXJ9r1HEtPQTEAAIriwAC1YIRSHG0iAiSBKLMPQQ"),
            ("11-qism","BAACAgIAAxkBAAIBZmrZ4HRuKVIB-rfBOu1xbOCzyXujAAL6kgACSdwQSG_iWC_kN8JlPQQ"),
            ("12-qism","BAACAgIAAxkBAAIBaGrZ4HmqQOr6pm-GURfwWos41xsiAALZmwACSdwQSG9Kh4ikQ_U4PQQ"),
            ("13-qism","BAACAgIAAxkBAAIBamrZ4H5aXx5zkakM0jMrPU6-hZ4sAALziwACAVdZSH68keFmoYWZPQQ"),
            ("14-qism","BAACAgIAAxkBAAIBbGrZ4IVqXZ1t4WCvtShQD_EeP45lAAJLjAACAVdZSHXefYoxyUkOPQQ"),
            ("15-qism","BAACAgIAAxkBAAIBbmrZ4IsFnj2EhpBnCYqxKZtvgC4iAAJTkQACAVdhSEz98NoLAjO1PQQ"),
            ("16-qism","BAACAgIAAxkBAAIBcGrZ4JDZncV_CpPmUJq4naVzXBxYAAKMiwACj2mgSCwnG37T3iPTPQQ"),
            ("17-qism","BAACAgIAAxkBAAIBcmrZ4JX0UM-XQqr9mUDiRRQSZcVKAAJLkAACj2moSJPZeR2csL75PQQ"),
            ("18-qism","BAACAgIAAxkBAAIBdGrZ4Jl8FTb-0BwXftw0wB9-isfqAAL7oAAC33GwSOQiR22cgpN8PQQ"),
            ("19-qism","BAACAgIAAxkBAAIBdmrZ4LKty7CMdEVHSQjrVpSbV9IhAALJlAAC13zpSK9dtTuHY_tOPQQ"),
            ("20-qism","BAACAgIAAxkBAAIBeGrZ4LbvD5smID-Mm5ap5pDcvFWGAAIFlQAC13zpSFsoxxEGFM3NPQQ"),
            ("21-qism","BAACAgIAAxkBAAIBemrZ4LqHVQqvZwKY4uwxKJ017cAKAAJ5nQAC13zpSDrHVB2zE26hPQQ"),
            ("22-qism","BAACAgIAAxkBAAIBfGrZ4L99IDzKRYR6Ze2CiOir-_MpAAJMogACg505SQERKxv31hl1PQQ"),
            ("23-qism","BAACAgIAAxkBAAIBfmrZ4MSEoUYfSDV1-0dpVAABqqF0NwACpqIAAoOdOUm5IJt4EXmE6T0E"),
            ("24-qism","BAACAgIAAxkBAAIBgGrZ4Mr-aIRoqSVYmaWCxINZb-y6AAL2igAC4NxJSRvYK4cgcC3cPQQ"),
        ],
    },
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida ovli 2 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2023",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIBD2rY3kn69yoP_Nm6AAGvBC9UOlJP6AACZhVrG7vp0Upht7c7rkzH3QEAAwIAA3kAAz0E",
        "qismlar": [
            ("1-qism","BAACAgIAAxkBAAIBgmrZ4bbVyqwTdlv4Ivdqt0J1EXKCAAJAQAACyGuRSm12_9jVsJk0PQQ"),
            ("2-qism","BAACAgIAAxkBAAIBhGrZ4b_rxQJbJIIqBrtHdyqe4ZblAALWPAAC03WpSuwidgMRhTShPQQ"),
            ("3-qism","BAACAgIAAxkBAAIBhmrZ4cR0fE0M7CX3i7GQzsWDhcXTAALGQAACyznBSpwaZ4km7CHKPQQ"),
        ],
    },
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 1-film",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2024",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIBEWrY3k6p56T5LhWw6gpcosaKz49IAAJtFWsbu-nRSibZqr8uw3WKAQADAgADeQADPQQ",
        "qismlar": [
            ("1-flim","BAACAgIAAxkBAAIBiGrZ4lLkRYgB8q2kn5EWvAjmBLglAAJtYQACXfoYSHkd6zBpQPvHPQQ"),
        ],
    },
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 3 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2024",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIBumrZ5gM595pSfIpI3J0ls0glCyDmAAJ2FWsbu-nRSlK5Dq30fmh6AQADAgADeQADPQQ",
        "qismlar": [
            ("1-qism","BAACAgIAAxkBAAIBimrZ4xHY5EcnQwE3GLuyeoY39XYOAAIzPwACXIuISIUXLdFzl7ztPQQ"),
            ("2-qism","BAACAgIAAxkBAAIBjGrZ4xY3EEYjC2vqAAHEOAlwzO1DNQACDUoAAljk0UiRSDJIMd_bxj0E"),
            ("3-qism","BAACAgIAAxkBAAIBjmrZ4x3Y4UzKcG6n8kjSxS_UNPydAAI7QgACxB4gSaU0kW89EolSPQQ"),
            ("4-qism","BAACAgIAAxkBAAIBkGrZ4yPYvcy1yR2-iCTIm1R8M_iHAAIiSwACSPNoSUNjCKVLRgFxPQQ"),
            ("5-qism","BAACAgIAAxkBAAIBkmrZ4yqCdmyUTJ7Ly63ecE_hFlp9AAJfSgACm6qoSYaV51JkknxQPQQ"),
            ("6-qism","BAACAgIAAxkBAAIBlGrZ4zPxKkaJ_IkkGroisA0Jzr4mAAJ_TQAC74EoSh6noA29nMwHPQQ"),
            ("7-qism","BAACAgIAAxkBAAIBlmrZ4zmQ6NQJCsJpBsW9prcW0m2eAALoTgACy39ASpCUgt5NlmG5PQQ"),
            ("8-qism","BAACAgIAAxkBAAIBmGrZ4z9Z5GzpkSNI7Lpv-uDOqju9AAI1UwACLlSJSmFD0UNQVBB1PQQ"),
            ("9-qism","BAACAgIAAxkBAAIBmmrZ40bNfWICS43h0sxxBzfC7tYFAALZUQACVEjRSr3sXfrvSZiZPQQ"),
            ("10-qism","BAACAgIAAxkBAAIBnGrZ40uimh3iN2WJ-RMgmO9D9CMiAAJYVQACGiwYS-HVQ7jvL5gIPQQ"),
            ("11-qism","BAACAgIAAxkBAAIBnmrZ41Img2JMqsF6AAG_fUbQaE8qjwACdVEAAuBBaEu6mxahcJ3Kgj0E"),
            ("12-qism","BAACAgIAAxkBAAIBoGrZ41nAAyrtwY52KWwVnN8jyxDSAAIgSgACgd-wSzo_dmWqnwt7PQQ"),
            ("13-qism","BAACAgIAAxkBAAIBomrZ415JobpTHwKk7aCvsHOzerq6AAJyTQAC8v4BSBdkRjdkNkliPQQ"),
            ("14-qism","BAACAgIAAxkBAAIBpGrZ42Z4Ucql2w1ttWs4MqWMCVc7AALSSgACFStISIg5lo-FZ3mkPQQ"),
            ("15-qism","BAACAgIAAxkBAAIBpmrZ42ubQxKCW1kuhKHe4ZP-VY3rAALJUQAC2M7QSPDrR7rxENxlPQQ"),
            ("16-qism","BAACAgIAAxkBAAIBqGrZ43Aom9pA9NDRZyd2NDC3ZRF-AAIyVQACQJQpScEbEa8p8vnKPQQ"),
            ("17-qism","BAACAgIAAxkBAAIBqmrZ43gIGX2tK1w8RUkFYr40hYQEAAJyWwACxRdoSbRFIAUlnzDdPQQ"),
            ("18-qism","BAACAgIAAxkBAAIBrGrZ437xeWCCwU5HDpe0pPjWMpr9AAJwWgACedUBSuNFriJsRPzyPQQ"),
            ("19-qism","BAACAgIAAxkBAAIBrmrZ44VUbfRBUiXJ5XuTGJRIss4mAALhUAACX_NISrUgE09qbd31PQQ"),
            ("20-qism","BAACAgIAAxkBAAIBsGrZ44prbDiysEqqHynnWqMW_dbOAAKGVwACCMGRSvrXPbj50dXaPQQ"),
            ("21-qism","BAACAgIAAxkBAAIBsmrZ449xu4m3KPTQX4xwjY09hMibAAIOZgACpM0JS0Sunwy1wmiePQQ"),
            ("22-qism","BAACAgIAAxkBAAIBtGrZ45XlXycdiNjcRimx0egcJLSdAAKmVgACD9goS_ct90VdvheGPQQ"),
            ("23-qism","BAACAgIAAxkBAAIBtmrZ45ve4b5t1S-qiYuZzPq3mwsmAAK-YAACEQFxSy1dcyWAr-ROPQQ"),
            ("24-qism","BAACAgIAAxkBAAIBuGrZ46CY7pBMRkjVOr8bLLorWET2AAJhXQAC4G-4SyT5kOpAQS4NPQQ"),
        ],
    },
    {
        "nomi": "Shilliq sifatida qayta tug'ilganim haqida 4 fasl",
        "janrlari": "Janrlari: Isekai, Sarguzasht, Comedy, Drama, Fantasy, Action",
        "yili": "2026",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAIBvGrZ5gxc1-N8v5O60xxmd4uWxJ0hAALGGWsb6huQSXUktKB37jlVAQADAgADeQADPQQ",
        "qismlar": [
            ("1-qism","BAACAgIAAxkBAAIBvmrZ5k-hpu1pgrhwIvlhReVjhv7HAAJdngACyW2BSrJ-4nsAAZnMEj0E"),
            ("2-qism","BAACAgIAAxkBAAIBwGrZ5lU32IVWuZg2rxN9UfRB70u4AAI7owACeDnISt46DW9uGsIiPQQ"),
            ("3-qism","BAACAgIAAxkBAAIBwmrZ5luUoaAmGAzWCUHSTVvV56dmAAI3nwACoO0QSxOQKz3nfyXmPQQ"),
            ("4-qism","BAACAgIAAxkBAAIBxGrZ5mArpv5MkBpIZvotbj0uuhbjAAI_kwAC92VxS64LPE_FbZ2rPQQ"),
            ("5-qism","BAACAgIAAxkBAAIBxmrZ5mUw5KwhTmrLX5Ayklr9zDl3AAIrlgACPOb5Sz-CI5McZ27rPQQ"),
            ("6-qism","BAACAgIAAxkBAAIByGrZ5m1cXim4MNA_1YdJpnQMvKHOAALAnQACospgSPCiNs22IkRpPQQ"),
            ("7-qism","BAACAgIAAxkBAAIBymrZ5nOleMjlQ8DDI2VSdJkQ0HJFAALmmwACC5yISPOSI0CTwElTPQQ"),
            ("8-qism","BAACAgIAAxkBAAIBzGrZ5nkAAeb7PxIpOqKoY0dXx35QPwACjMoAAhsb0Ej_vdgdYE2oJD0E"),
            ("9-qism","BAACAgIAAxkBAAIBzmrZ5n9hIUw8bIq36faIZI8ffIAYAAJTnwACXUMhSTb-VRMSbhCXPQQ"),
            ("10-qism","BAACAgIAAxkBAAIB0GrZ5oRblpSN7J8nQTD7flSOIL_OAAJvqQACJWJpSUS7g6-GceMyPQQ"),
            ("11-qism","BAACAgIAAxkBAAIB0mrZ5opDNF8pGfef-kiFqj1cq8OxAALXnQACTmjZSQYyk30ZrqFmPQQ"),
            ("12-qism","BAACAgIAAxkBAAIB1GrZ5o94SyiOc_lINKmR_XBdItwOAALpqAAC8VFBSkOerQu9Qc6zPQQ"),
            ("13-qism","BAACAgIAAxkBAAIB1mrZ5paDJAtpTi-QiB2nFoHr8R2LAAIjsAAC8VFJSgGA9vSwpUtbPQQ"),
            ("14-qism","BAACAgIAAxkBAAIB2GrZ5p3Nbb5ErI57OdKptN4ft-WDAAJcoQAC4nuhSnBRVbv7obSePQQ"),
            ("15-qism","BAACAgIAAxkBAAIB2mrZ5qbKz76IOkicFmI14jL3whXnAAKIngACT2cpS-kZyU8z9bULPQQ"),
            ("16-qism","BAACAgIAAxkBAAIB3GrZ5qq3Jb2AkLkxv2aWURhOmnMLAALfpwACTOtZSx6u30pnojexPQQ"),
            ("17-qism","BAACAgIAAxkBAAIB3mrZ5rDXF32JCko3de6K5V9C7xBkAAIkoQACWH_JS5kTbzfen4qAPQQ"),
            ("18-qism","BAACAgIAAxkBAAIB4GrZ5rgHBIrWBYDSoEaJCbbNQ1ZBAAI5qQACTt35S3spUuJKLcUtPQQ"),
            ("19-qism","BAACAgIAAxkBAAIB4mrZ5r-Wu-dyL8BDWWxRDTe4QvnkAALWpwACIuVJSJWPl2MIAVlZPQQ"),
            ("20-qism","BAACAgIAAxkBAAIB5GrZ5sQ5ftYgi20FELmdpbLb8_g7AALlpwACntWQSBYCyUVsXsAwPQQ"),
            ("21-qism","BAACAgIAAxkBAAIB5mrZ5sqHcb0vdiSPTiU5arE57tyqAAIWpwAC_0vZSCgrRGofuFYlPQQ"),
            ("22-qism","BAACAgIAAxkBAAIB6GrZ5tGYjnl4A09hN2SwKmaKAkmcAALJsgACikYxSe5NIPy2rSQiPQQ"),
            ("23-qism","BAACAgIAAxkBAAIB6mrZ5tjRcSg7PRlfhBpnA3RskmqUAAJqsQACNqloSSH1yWeMo227PQQ"),
            ("24-qism","BAACAgIAAxkBAAIB7GrZ5t-LQpcNuxRrf-6R2lsZ2DW6AAK3ogACkYKxSWUnRleZVmzoPQQ"),
        ],
    },
    {
        "nomi": "Tayoq va qilich 1 fasl",
        "janrlari": "Janrlari: Sarguzasht, Comedy, Fantasy, Ramantik",
        "yili": "2025",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAICHmrZ634-baSgoQrfSYEh6DC7GZw_AAKFG2sb6huYScQCKfQsskBOAQADAgADeQADPQQ",
        "qismlar": [
            ("1-qism","BAACAgIAAxkBAAIB7mrZ6WWBEMxbcyiStDcy0_2PvSv5AAKkTwAC9GZgSFrlDqGG8CffPQQ"),
            ("2-qism","BAACAgIAAxkBAAIB8GrZ6Wof94Ny2DKPenhOJhJnugrhAAIEVgACPS_5SMTl1xVYriyBPQQ"),
            ("3-qism","BAACAgIAAxkBAAIB8mrZ6W_kzUMnl6GGNM-SJk72qdP-AAIHVgACPS_5SM0ytvGgWIBzPQQ"),
            ("4-qism","BAACAgIAAxkBAAIB9GrZ6XVH3eWKrRSUVsXifO93mUu-AAI-TQACgzfBSebiF6mo41qUPQQ"),
            ("5-qism","BAACAgEAAxkBAAIB9mrZ6Xmjl4KFFZOjW33OGp-t0uZlAAJ5BQACCnEYRsKNFnbXLjjOPQQ"),
            ("6-qism","BAACAgEAAxkBAAIB-GrZ6X2OP8cD_Ntt4KorhcFoYAyRAAKIAwACfp0gRsVGE3pGZl1KPQQ"),
            ("7-qism","BAACAgEAAxkBAAIB-mrZ6YJ9bllJK4_qlG0hhJDC9pZgAAIqBQACoHVoRgKF6qwoiIn0PQQ"),
            ("8-qism","BAACAgEAAxkBAAIB_GrZ6Yb8n5_Q22tA88IxzjsdEcMCAAJ4AwACvXZZR834ZE_pHgh_PQQ"),
            ("9-qism","BAACAgEAAxkBAAIB_mrZ6YveGhnGgINzoLw4JqpXwrCnAALlBAACmb2oR7uJN8QPMx17PQQ"),
            ("10-qism","BAACAgEAAxkBAAICAAFq2emPhyFR740PJvuKq-_fOYo9wwACtAQAApm9uEeRhIjAGCcLGT0E"),
            ("11-qism","BAACAgEAAxkBAAICAmrZ6ZOZ8ybtUgiSF1exQFvth5-lAALvCAACixvJR6hV-pPCKJD4PQQ"),
            ("12-qism","BAACAgEAAxkBAAICBGrZ6ZhHtVdTS-9C487T4cigTwbDAAL6CAACixvJRzdC57dXHa3APQQ"),
        ],
    },
    {
        "nomi": "Tayoq va qilich 2 fasl",
        "janrlari": "Janrlari: Sarguzasht, Comedy, Fantasy, Ramantik",
        "yili": "2026",
        "sifat": "720p, 1080p",
        "rasm": "AgACAgIAAxkBAAICIGrZ64KeX8NB9hdpZLhKhF3oGx-wAAKGG2sb6huYSWEWkt4NP7NYAQADAgADeQADPQQ",
        "qismlar": [
            ("1-qism","BAACAgQAAxkBAAICBmrZ6oZPMrKmlx2nSsh5jd57LOydAAI_HAACXMXpUvz-mBMdKtSVPQQ"),
            ("2-qism","BAACAgIAAxkBAAICCGrZ6orP56qYO0LBfcjg3JFOq_UBAAJ5lQAC-l4oS110qMYYGMqxPQQ"),
            ("3-qism","BAACAgIAAxkBAAICCmrZ6o6fVXEWnjCLnSbuAZAdO__fAAI4pAACwaFxS_lSlXz-VBpmPQQ"),
            ("4-qism","BAACAgIAAxkBAAICDGrZ6pzwY8H94gIVGG5Mmmfle1vFAAI4mgACZlu4S9MVXu5dRJFUPQQ"),
            ("5-qism","BAACAgIAAxkBAAICDmrZ6r-LcEhUuQEVR2ZZ9G-8L6siAAI6nQACe_YJSCJOFmkWsqvMPQQ"),
            ("6-qism","BAACAgIAAxkBAAICEGrZ6sUShCDrhzuUC59LzVNz6EtyAAI8ngACMDtYSOKxKEw6vs5BPQQ"),
            ("7-qism","BAACAgQAAxkBAAICEmrZ6tMDyfby7_0B7NRH4-nHxwm5AAIlIQAC02yhUAzHjDcNnaUpPQQ"),
            ("8-qism","BAACAgQAAxkBAAICFGrZ6tYKEWoS6OYbug2UEayoehdtAAKxIAAC1hrpUMYwhtSJMlgdPQQ"),
            ("9-qism","BAACAgQAAxkBAAICFmrZ6tpF95u_MA3_mwfkv9sMoXX_AAKgHAACZBxAUfFyYI4i2Kz6PQQ"),
            ("10-qism","BAACAgQAAxkBAAICGGrZ6t4-pnBG8XpJZ3MV7P7lk9B5AALMIAACazGIUVlYZX9aF1_BPQQ"),
            ("11-qism","BAACAgQAAxkBAAICGmrZ6uP4H2t8EKm5K6oo78sRE5GmAAKEHwACm0DQUaOyr_DEyS3yPQQ"),
            ("12-qism","BAACAgIAAxkBAAICHGrZ6uhFuMpMY3EQEYvfgIzRTeK1AAK4ngAC2QQZSgzSJ8To88jcPQQ"),
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
    obuna_bolmagan = []

    for kanal in MAJBURIY_KANALLAR:
        try:
            a_zo = await context.bot.get_chat_member(
                chat_id=kanal["channel_id"], user_id=user_id
            )
            holat = a_zo.status
            azo_emas = holat in (ChatMemberStatus.LEFT, ChatMemberStatus.BANNED) or (
                holat == ChatMemberStatus.RESTRICTED and not a_zo.is_member
            )
            if azo_emas:
                obuna_bolmagan.append(kanal)
        except (BadRequest, Forbidden) as e:
            logger.error(
                f"Kanal tekshirishda xatolik (chat_id={kanal['channel_id']}): {e}"
            )
            obuna_bolmagan.append(kanal)

    return obuna_bolmagan


def obuna_klaviaturasi(obuna_bolmagan_kanallar: list, tekshir_callback: str):


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
