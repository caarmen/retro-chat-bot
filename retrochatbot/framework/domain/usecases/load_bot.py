import importlib

from retrochatbot.botapi.bot_api import Bot


def load_bot(
    full_bot_class_name: str,
    participant_name: str,
) -> Bot:
    module_name, class_name = full_bot_class_name.rsplit(".", 1)

    bot_module = importlib.import_module(module_name)
    bot_class = getattr(bot_module, class_name)
    return bot_class(name=participant_name)
