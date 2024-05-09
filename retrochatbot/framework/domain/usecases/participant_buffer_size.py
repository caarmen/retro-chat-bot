CHARS_PER_LINE = 80


def calculate_participant_buffer_size(participant_count: int) -> int:
    if participant_count == 1:
        lines_per_particpant = 18
    elif participant_count == 2:
        lines_per_particpant = 8
    else:
        lines_per_particpant = 7 - participant_count

    return CHARS_PER_LINE * lines_per_particpant
