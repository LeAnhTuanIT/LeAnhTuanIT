#!/usr/bin/env python3
"""Generate daily developer horoscope SVG."""

import html
import os
import random
from datetime import datetime, timezone, timedelta

SIGNS = [
    ("Mass JavaScript", "♐", "#F7DF1E"),
    ("Massa Python", "♒", "#3776AB"),
    ("Ma TypeScript", "♓", "#3178C6"),
    ("Song Go", "♊", "#00ADD8"),
    ("Su Docker", "♌", "#2496ED"),
    ("Xu Rust", "♑", "#CE422B"),
    ("Bao React", "♈", "#61DAFB"),
    ("Thien Git", "♎", "#F05032"),
    ("Kim Linux", "♉", "#FCC624"),
    ("Nhan SQL", "♍", "#4169E1"),
    ("Ho NestJS", "♏", "#E0234E"),
    ("Cua Redis", "♋", "#DC382D"),
]

PREDICTIONS = [
    "Today your code will compile on the first try. Buy a lottery ticket.",
    "Mercury is in retrograde. Avoid `git push --force` at all costs.",
    "The stars align for a major refactor. Your future self will thank you.",
    "A mysterious bug from 2 sprints ago will finally reveal itself.",
    "Today is NOT the day to update your dependencies.",
    "Your pull request will be approved with zero comments. Legendary.",
    "A Stack Overflow answer from 2014 will save your entire afternoon.",
    "Beware: a colleague will suggest rewriting everything in Rust.",
    "The universe grants you permission to delete legacy code. Go forth.",
    "An unexpected `undefined` awaits you around line 42.",
    "Your Docker container will build perfectly. The deploy? Not so much.",
    "You will produce 3x more features than yesterday. Legendary energy!",
    "A senior dev will approve your PR without reading it. Cherish this.",
    "Your CI pipeline will pass, but only after the 4th retry.",
    "Today you will discover a new VS Code shortcut that changes your life.",
    "The coffee machine and your code will both work flawlessly today.",
    "Your regex will actually do what you think it does. Miracles happen.",
    "A customer will report a bug that is actually a feature. You win.",
    "You will write documentation today. Just kidding. No one does that.",
    "The stars say: take a break. Close the laptop. Touch some grass.",
    "A wild production incident appears! But you have the hotfix ready.",
    "NPM install will complete in under 10 seconds. A true miracle.",
    "Your database query will return exactly the results you expect.",
    "Today is a great day to learn a new language. Or just take a nap.",
]

LUCKY_ITEMS = [
    "Lucky framework: Next.js",
    "Lucky command: git stash",
    "Lucky number: 200 OK",
    "Lucky key: Ctrl+Z",
    "Lucky drink: Double espresso",
    "Lucky time: 2:00 AM",
    "Lucky method: console.log",
    "Lucky port: 3000",
    "Lucky status: 418 I'm a teapot",
    "Lucky editor: the one you're using",
    "Lucky commit: the next one",
    "Lucky branch: not main, please",
]


def wrap_text(text, max_width=50):
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


def generate_svg(sign_name, sign_symbol, sign_color, prediction, lucky, bg, text_color, border, accent, filename):
    pred_lines = wrap_text(prediction)
    line_height = 20
    pad_x, pad_y = 28, 20

    title = "Developer Horoscope"
    char_width = 8.8

    all_text_lines = pred_lines + [lucky]
    max_chars = max(len(l) for l in all_text_lines + [title, sign_name])
    width = int(max(max_chars * char_width + pad_x * 2, 480))

    title_y = pad_y + 18
    sign_y = title_y + 36
    divider1_y = sign_y + 16
    pred_start_y = divider1_y + 26
    divider2_y = pred_start_y + len(pred_lines) * line_height + 10
    lucky_y = divider2_y + 22
    height = int(lucky_y + pad_y + 8)

    pred_tspans = ""
    for i, line in enumerate(pred_lines):
        y = pred_start_y + i * line_height
        pred_tspans += f'    <tspan x="{pad_x}" y="{y}">{html.escape(line)}</tspan>\n'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="hgrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{bg};stop-opacity:0.95" />
    </linearGradient>
  </defs>
  <rect fill="url(#hgrad)" width="{width}" height="{height}" rx="12" stroke="{border}" stroke-width="1"/>
  <text fill="{accent}" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" x="{width // 2}" y="{title_y}">🔮 {html.escape(title)}</text>
  <text font-family="'Segoe UI', Ubuntu, sans-serif" text-anchor="middle" x="{width // 2}" y="{sign_y}">
    <tspan fill="{sign_color}" font-size="20">{sign_symbol}</tspan>
    <tspan fill="{text_color}" font-size="15" font-weight="bold" dx="8">{html.escape(sign_name)}</tspan>
  </text>
  <line x1="{pad_x}" y1="{divider1_y}" x2="{width - pad_x}" y2="{divider1_y}" stroke="{accent}" stroke-width="1" opacity="0.3"/>
  <text fill="{text_color}" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="14">
{pred_tspans}  </text>
  <line x1="{pad_x}" y1="{divider2_y}" x2="{width - pad_x}" y2="{divider2_y}" stroke="{accent}" stroke-width="1" stroke-dasharray="4,4" opacity="0.3"/>
  <text fill="{sign_color}" font-family="'Segoe UI', Ubuntu, sans-serif" font-size="13" font-style="italic" text-anchor="middle" x="{width // 2}" y="{lucky_y}">✨ {html.escape(lucky)}</text>
</svg>'''

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(svg)


if __name__ == "__main__":
    # Use today's date as seed so it changes daily but is consistent within the day
    vn_tz = timezone(timedelta(hours=7))
    today = datetime.now(vn_tz).strftime("%Y-%m-%d")
    rng = random.Random(today)

    sign_name, sign_symbol, sign_color = rng.choice(SIGNS)
    prediction = rng.choice(PREDICTIONS)
    lucky = rng.choice(LUCKY_ITEMS)

    generate_svg(
        sign_name, sign_symbol, sign_color, prediction, lucky,
        bg="#0d1117", text_color="#c9d1d9", border="#30363d", accent="#A9FEF7",
        filename="dist/horoscope-dark.svg",
    )
    generate_svg(
        sign_name, sign_symbol, sign_color, prediction, lucky,
        bg="#ffffff", text_color="#24292e", border="#d0d7de", accent="#0969da",
        filename="dist/horoscope.svg",
    )

    print(f"Generated horoscope: {sign_symbol} {sign_name}")
    print(f"Prediction: {prediction}")
    print(f"{lucky}")
