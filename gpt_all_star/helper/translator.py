import gettext
import os


class Translator:
    DEFAULT_LOCALE_PATH = "gpt_all_star/locales"

    def __init__(self, lang, locale_dir):
        full_locale_dir = os.path.join(os.getcwd(), locale_dir)
        self.translator = gettext.translation(
            "messages", full_locale_dir, languages=[lang], fallback=True
        )
        self.translator.install()

    def translate(self, msg):
        return self.translator.gettext(msg)


def setup_i18n(lang, path=Translator.DEFAULT_LOCALE_PATH):
    translator = Translator(lang, path)

    def _(message):
        return translator.translate(message)

    return _


def create_translator(lang):
    if lang == "ja":
        return setup_i18n("ja_JP")
    else:
        return setup_i18n("en")
