#!/usr/bin/env python3
"""Generate random dev joke SVG card."""

import html
import os
import random

JOKES = [
    ("Why do programmers prefer dark mode?", "Because light attracts bugs."),
    ("Why do Java developers wear glasses?", "Because they can't C#."),
    ("A SQL query walks into a bar, sees two tables...", "and asks: 'Can I JOIN you?'"),
    ("How many programmers does it take to change a light bulb?", "None. That's a hardware problem."),
    ("Why was the JavaScript developer sad?", "Because he didn't Node how to Express himself."),
    ("What's a programmer's favorite hangout place?", "Foo Bar."),
    ("Why do Python programmers have low self-esteem?", "They're always comparing themselves to others."),
    ("What did the router say to the doctor?", "It hurts when IP."),
    ("Why did the developer go broke?", "Because he used up all his cache."),
    ("What's the object-oriented way to become wealthy?", "Inheritance."),
    ("Why did the functions stop calling each other?", "Because they got into too many arguments."),
    ("There are only 10 types of people in the world:", "Those who understand binary and those who don't."),
    ("A programmer's wife tells him: 'Go to the store and get a loaf of bread. If they have eggs, get a dozen.'", "He came back with 12 loaves of bread."),
    ("Why do programmers always mix up Halloween and Christmas?", "Because Oct 31 == Dec 25."),
    ("What's a programmer's least favorite car?", "A RecursionRecursionRecursionRecursion..."),
    ("Why did the programmer quit his job?", "Because he didn't get arrays. (a raise)"),
    ("How does a programmer open a jar?", "He installs Java."),
    ("What do you call a snake that's 3.14 meters long?", "A Pi-thon."),
    ("Why did the developer become a DJ?", "Because he had mass appeal... I mean, mass a-peal... I mean, he was great at dropping tables."),
    ("!false", "It's funny because it's true."),
]


def wrap_text(text, max_width=52):
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


def generate_joke_svg(setup, punchline, bg, text_color, punch_color, border, accent, filename):
    setup_lines = wrap_text(setup)
    punch_lines = wrap_text(punchline)

    line_height = 22
    pad_x, pad_y = 28, 24
    char_width = 8.8

    all_lines = setup_lines + punch_lines
    max_chars = max(len(l) for l in all_lines)
    width = int(max(max_chars * char_width + pad_x * 2, 460))

    emoji_y = pad_y + 24
    setup_start_y = emoji_y + 36
    divider_y = setup_start_y + len(setup_lines) * line_height + 12
    punch_start_y = divider_y + 28
    height = int(punch_start_y + len(punch_lines) * line_height + pad_y + 8)

    setup_tspans = ""
    for i, line in enumerate(setup_lines):
        y = setup_start_y + i * line_height
        setup_tspans += f'    <tspan x="{pad_x}" y="{y}">{html.escape(line)}</tspan>\n'

    punch_tspans = ""
    for i, line in enumerate(punch_lines):
        y = punch_start_y + i * line_height
        punch_tspans += f'    <tspan x="{pad_x}" y="{y}">{html.escape(line)}</tspan>\n'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{bg};stop-opacity:0.95" />
    </linearGradient>
  </defs>
  <rect fill="url(#grad)" width="{width}" height="{height}" rx="12" stroke="{border}" stroke-width="1"/>
  <text font-size="24" text-anchor="middle" x="{width // 2}" y="{emoji_y}">&#128514;</text>
  <text fill="{text_color}" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="15" font-weight="500">
{setup_tspans}  </text>
  <line x1="{pad_x}" y1="{divider_y}" x2="{width - pad_x}" y2="{divider_y}" stroke="{accent}" stroke-width="1" stroke-dasharray="4,4" opacity="0.5"/>
  <text fill="{punch_color}" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="15" font-weight="700" font-style="italic">
{punch_tspans}  </text>
</svg>'''

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(svg)


if __name__ == "__main__":
    setup, punchline = random.choice(JOKES)

    generate_joke_svg(
        setup, punchline,
        bg="#0d1117", text_color="#c9d1d9", punch_color="#58a6ff",
        border="#30363d", accent="#58a6ff",
        filename="dist/joke-dark.svg",
    )
    generate_joke_svg(
        setup, punchline,
        bg="#ffffff", text_color="#24292e", punch_color="#0969da",
        border="#d0d7de", accent="#0969da",
        filename="dist/joke.svg",
    )

    print("Generated joke SVGs!")
    print(f"Q: {setup}")
    print(f"A: {punchline}")
