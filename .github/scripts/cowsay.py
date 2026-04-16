#!/usr/bin/env python3
"""Generate cowsay SVG with random programming quotes."""

import random
import html
import os

QUOTES = [
    "Code is like humor. When you have to explain it, it's bad. - Cory House",
    "First, solve the problem. Then, write the code. - John Johnson",
    "Talk is cheap. Show me the code. - Linus Torvalds",
    "Any fool can write code that a computer can understand. Good programmers write code that humans can understand. - Martin Fowler",
    "Make it work, make it right, make it fast. - Kent Beck",
    "Simplicity is the soul of efficiency. - Austin Freeman",
    "Fix the cause, not the symptom. - Steve Maguire",
    "Code never lies, comments sometimes do. - Ron Jeffries",
    "Don't comment bad code - rewrite it. - Brian W. Kernighan",
    "The best error message is the one that never shows up. - Thomas Fuchs",
    "Programs must be written for people to read, and only incidentally for machines to execute. - Harold Abelson",
    "Truth can only be found in one place: the code. - Robert C. Martin",
    "Experience is the name everyone gives to their mistakes. - Oscar Wilde",
    "Perfection is achieved not when there is nothing more to add, but rather when there is nothing more to take away. - Antoine de Saint-Exupery",
    "Java is to JavaScript what car is to carpet. - Chris Heilmann",
    "Programming isn't about what you know; it's about what you can figure out. - Chris Pine",
    "Give a man a program, frustrate him for a day. Teach a man to program, frustrate him for a lifetime. - Muhammad Waseem",
    "Debugging is twice as hard as writing the code in the first place. - Brian W. Kernighan",
    "The only way to learn a new programming language is by writing programs in it. - Dennis Ritchie",
    "Measuring programming progress by lines of code is like measuring aircraft building progress by weight. - Bill Gates",
]


def wrap_text(text, max_width=48):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 <= max_width:
            current += (" " if current else "") + word
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def make_cowsay(text):
    lines = wrap_text(text)
    max_len = max(len(l) for l in lines)
    lines = [l.ljust(max_len) for l in lines]

    result = [" " + "_" * (max_len + 2)]
    if len(lines) == 1:
        result.append(f"< {lines[0]} >")
    else:
        result.append(f"/ {lines[0]} \\")
        for l in lines[1:-1]:
            result.append(f"| {l} |")
        result.append(f"\\ {lines[-1]} /")
    result.append(" " + "-" * (max_len + 2))
    result.extend([
        "        \\   ^__^",
        "         \\  (oo)\\_______",
        "            (__)\\       )\\/\\",
        "                ||----w |",
        "                ||     ||",
    ])
    return result


def generate_svg(lines, bg, text_color, border, title_color, filename):
    line_height = 20
    pad_x, pad_y = 24, 20
    title = "~ Moo! Daily Dev Quote ~"
    title_y = pad_y + 16
    art_start_y = title_y + 28

    char_width = 8.4
    max_chars = max(len(l) for l in lines)
    content_width = max_chars * char_width
    title_width = len(title) * char_width
    width = int(max(content_width, title_width) + pad_x * 2)
    height = int(art_start_y + len(lines) * line_height + pad_y)

    tspans = ""
    for i, line in enumerate(lines):
        y = art_start_y + i * line_height
        tspans += f'    <tspan x="{pad_x}" y="{y}">{html.escape(line)}</tspan>\n'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect fill="{bg}" width="{width}" height="{height}" rx="12" stroke="{border}" stroke-width="1"/>
  <text fill="{title_color}" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="15" font-weight="bold" text-anchor="middle" x="{width // 2}" y="{title_y}">{html.escape(title)}</text>
  <text fill="{text_color}" font-family="'Courier New', Courier, monospace" font-size="14" xml:space="preserve">
{tspans}  </text>
</svg>'''

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(svg)


if __name__ == "__main__":
    quote = random.choice(QUOTES)
    lines = make_cowsay(quote)

    generate_svg(lines, "#0d1117", "#58a6ff", "#30363d", "#A9FEF7", "dist/cowsay-dark.svg")
    generate_svg(lines, "#ffffff", "#24292e", "#d0d7de", "#0969da", "dist/cowsay.svg")

    print("Generated cowsay SVGs!")
    for line in lines:
        print(line)
