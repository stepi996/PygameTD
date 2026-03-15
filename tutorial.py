import pygame # type: ignore
import constants
from objects import *

def _wrap_text_lines(text, font, max_text_width):
    """Split text into lines that fit max_text_width for the given font."""
    words = text.split(" ")
    wrapped_lines = []
    current_line = ""

    for word in words:
        candidate = f"{current_line} {word}".strip()
        if font.size(candidate)[0] <= max_text_width:
            current_line = candidate
        else:
            if current_line:
                wrapped_lines.append(current_line)
            current_line = word

    if current_line:
        wrapped_lines.append(current_line)

    return wrapped_lines

def _pick_fitting_font(text, font_path, start_size, min_size, max_text_width, max_text_height):
    """Pick the largest font size that can render wrapped text within max_text_height."""
    for font_size in range(start_size, min_size - 1, -1):
        font = pygame.font.Font(font_path, font_size)
        wrapped_lines = _wrap_text_lines(text, font, max_text_width)
        needed_height = len(wrapped_lines) * font.get_linesize()
        if needed_height <= max_text_height:
            return font
    return pygame.font.Font(font_path, min_size)

def draw_wrapped_text(screen, text, font, color, container_rect, max_bottom, padding=15):
    """Render word-wrapped text inside a container rect without overflowing max_bottom."""
    max_text_width = int(container_rect.width - (padding * 2))
    wrapped_lines = _wrap_text_lines(text, font, max_text_width)

    line_height = font.get_linesize()
    text_x = container_rect.left + padding
    text_y = container_rect.top + 18

    for line in wrapped_lines:
        if text_y + line_height > max_bottom:
            break
        rendered_line = font.render(line, True, color)
        screen.blit(rendered_line, (text_x, text_y))
        text_y += line_height

def basics(screen, next, event):
    # Draw the tutorial screen
    rect = pygame.Rect(0, 0, constants.block_width * 6, constants.block_height * 4)
    next_button = Button.create(0, 0, rect.width - constants.block_width*4, rect.height - constants.block_height*3, "Next", font=pygame.font.Font('freesansbold.ttf', 16))

    tutorial_messages = [
        "Welcome to PygameTD! Click 'Next' to learn how to play.",
        "Build towers to defend against waves of enemies. You earn gold by defeating them.",
        "Click on an empty blue block to build a tower. Each tower costs 100 gold.",
        "Towers can be upgraded up to 3 times. But beware, only one upgrade from the pair can be chosen.",
        "Enemies will follow the path to reach the end. Prevent them from getting through by building towers!",
        "In the bottom right corner, you can see the current wave, your gold, and how many towers you can build. Good luck!",
        "On the third wave, green enemies will start spawning. They are tankier than normal red enemy, but also slower.",
        "On the seventh wave, yellow enemies will start spawning. They can only be hit by towers with 'Yellow Damage' upgrade.",
        "That's all for the basics! Click 'Next' to start playing and good luck defending your base!"
    ]
    message_index = min(max(next, 0), len(tutorial_messages) - 1)
    tutorial_message = tutorial_messages[message_index]

    # Center button inside rect
    rect.center = (constants.width / 2, constants.height / 2)
    next_button.rect.center = (rect.center[0] + rect.width / 3.2, rect.center[1] + rect.height / 3)

    # Draw the tutorial screen UI
    pygame.draw.rect(screen, (65, 74, 89), rect)
    next_button.draw(screen)

    # Draw wrapped text above the button and stop before it would overlap.
    text_padding = 15
    max_text_bottom = next_button.rect.top - 10
    max_text_width = int(rect.width - (text_padding * 2))
    max_text_height = max_text_bottom - (rect.top + 18)
    tutorial_font = _pick_fitting_font(
        tutorial_message,
        'freesansbold.ttf',
        start_size=16,
        min_size=11,
        max_text_width=max_text_width,
        max_text_height=max_text_height,
    )
    draw_wrapped_text(screen, tutorial_message, tutorial_font, (255, 255, 255), rect, max_text_bottom, padding=text_padding)

    # Handle next button click and advance tutorial
    if next_button.is_clicked(event):
        next += 1

    return next