KEY_BACKSPACE = "Backspace"
KEY_ENTER = "Enter"


def keys_to_text(keys: list[str]) -> str:
    result: list[str] = []
    for key in keys:
        if key == KEY_BACKSPACE and len(result) > 0:
            result.pop()
        elif key == KEY_ENTER:
            result.append("\n")
        elif len(key) == 1:
            result.append(key)
        # else ignore other keys
    return "".join(result)
