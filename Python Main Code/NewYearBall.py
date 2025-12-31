import turtle
import math
import random
import time


def clamp(value: float, low: float, high: float) -> float:
    return low if value < low else high if value > high else value


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def lerp_color(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t = clamp(t, 0.0, 1.0)
    return (
        int(lerp(c1[0], c2[0], t)),
        int(lerp(c1[1], c2[1], t)),
        int(lerp(c1[2], c2[2], t)),
    )


def brighten(color: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    # amount: 0..1, pushes toward white
    amount = clamp(amount, 0.0, 1.0)
    return (
        int(color[0] + (255 - color[0]) * amount),
        int(color[1] + (255 - color[1]) * amount),
        int(color[2] + (255 - color[2]) * amount),
    )


# Screen
screen = turtle.Screen()
screen.title("Holiday New Year Ball")
screen.setup(width=980, height=720)
screen.colormode(255)
screen.bgcolor(8, 10, 18)


def make_layer() -> turtle.Turtle:
    t = turtle.Turtle(visible=False)
    t.speed(0)
    t.penup()
    t.hideturtle()
    return t


bg = make_layer()
ball_layer = make_layer()
lights_layer = make_layer()
fx_layer = make_layer()
snow_layer = make_layer()
text_layer = make_layer()


# Visual params
BALL_RADIUS = 105
BALL_CENTER_X = 0
BALL_START_Y = 260
BALL_GROUND_Y = -40
STRING_TOP_Y = 315

BASE_OUTER = (55, 8, 18)       # deep holiday red
BASE_INNER = (245, 55, 75)     # bright red core
HIGHLIGHT = (255, 210, 220)    # warm glossy highlight
OUTLINE = (255, 235, 240)      # soft light rim

LED_PALETTE = [
    (255, 70, 70),
    (80, 255, 150),
    (90, 160, 255),
    (255, 230, 120),
    (210, 140, 255),
    (255, 160, 70),
]


def build_stars(count: int = 220, seed: int = 7) -> list[tuple[int, int, int, tuple[int, int, int]]]:
    rng = random.Random(seed)
    stars: list[tuple[int, int, int, tuple[int, int, int]]] = []
    for _ in range(count):
        x = rng.randint(-480, 480)
        y = rng.randint(-320, 340)
        if y < -120 and abs(x) < 240:
            continue
        size = rng.choice([1, 1, 1, 2, 2, 3])
        tint = rng.choice([(200, 210, 255), (255, 240, 200), (200, 255, 240)])
        stars.append((x, y, size, tint))
    return stars


STARS = build_stars(240)


def build_garland(seed: int = 11) -> list[tuple[float, float, tuple[int, int, int]]]:
    rng = random.Random(seed)
    bulbs: list[tuple[float, float, tuple[int, int, int]]] = []
    y_base = 300
    for i in range(26):
        x = -470 + i * (940 / 25)
        y = y_base + 18 * math.sin(i * 0.55)
        col = rng.choice(LED_PALETTE)
        bulbs.append((x, y, col))
    return bulbs


GARLAND_BULBS = build_garland()


def build_snowflakes(count: int = 120, seed: int = 101) -> list[dict]:
    rng = random.Random(seed)
    flakes: list[dict] = []
    for _ in range(count):
        flakes.append(
            {
                "x": rng.uniform(-500, 500),
                "y": rng.uniform(-360, 360),
                "speed": rng.uniform(0.8, 2.6),
                "size": rng.choice([1, 1, 2, 2, 3]),
                "drift": rng.uniform(0.8, 2.4),
                "phase": rng.uniform(0.0, math.tau),
            }
        )
    return flakes


SNOWFLAKES = build_snowflakes()


def draw_starfield(count: int = 220) -> None:
    bg.clear()
    bg.penup()
    for (x, y, size, tint) in STARS[:count]:
        bg.goto(x, y)
        bg.dot(size, tint)

    # Garland (holiday-ish)
    bg.pensize(3)
    bg.pencolor((30, 90, 55))
    bg.penup()
    first = True
    for (x, y, _col) in GARLAND_BULBS:
        if first:
            bg.goto(x, y)
            bg.pendown()
            first = False
        else:
            bg.goto(x, y)
    bg.penup()

    for (x, y, col) in GARLAND_BULBS:
        bg.goto(x, y)
        bg.dot(10, brighten(col, 0.25))
        bg.dot(6, col)


def draw_shadow(cx: float, ground_y: float, radius: float, intensity: float) -> None:
    # Soft faux-ellipse using dots.
    intensity = clamp(intensity, 0.0, 1.0)
    if intensity <= 0:
        return
    base = (10, 10, 16)
    shade = lerp_color(base, (0, 0, 0), 0.55)
    width = radius * (1.25 + 0.45 * intensity)
    steps = 38
    for i in range(steps):
        t = i / (steps - 1)
        x = lerp(cx - width, cx + width, t)
        dist = abs(t - 0.5) * 2
        dot_size = max(1, int((radius * 0.55) * (1 - dist * dist)))
        # Fade the edges
        fade = 1 - dist
        color = lerp_color(shade, base, 0.6 * (1 - fade))
        bg.goto(x, ground_y - int(radius * 0.62))
        bg.dot(dot_size, color)


def draw_gradient_ball(cx: float, cy: float, radius: int) -> None:
    ball_layer.clear()

    # Concentric circles = gradient
    ball_layer.penup()
    for r in range(radius, 0, -2):
        t = 1 - (r / radius)
        base = lerp_color(BASE_OUTER, BASE_INNER, t)
        ball_layer.goto(cx, cy - r)
        ball_layer.pendown()
        ball_layer.pensize(2)
        ball_layer.pencolor(base)
        ball_layer.circle(r)
        ball_layer.penup()

    # Highlight "gloss" (offset small circles)
    hx = cx - radius * 0.22
    hy = cy + radius * 0.18
    for r in range(int(radius * 0.55), 0, -3):
        t = 1 - (r / (radius * 0.55))
        c = lerp_color(brighten(HIGHLIGHT, 0.25), brighten(HIGHLIGHT, 0.85), t)
        ball_layer.goto(hx, hy - r)
        ball_layer.pendown()
        ball_layer.pensize(2)
        ball_layer.pencolor(c)
        ball_layer.circle(r)
        ball_layer.penup()

    # Outer outline
    ball_layer.pensize(3)
    ball_layer.pencolor(OUTLINE)
    ball_layer.goto(cx, cy - radius)
    ball_layer.pendown()
    ball_layer.circle(radius)
    ball_layer.penup()

    # Cap + string
    cap_w = radius * 0.34
    cap_h = radius * 0.16
    cap_y = cy + radius * 0.9
    ball_layer.pencolor((220, 220, 235))
    ball_layer.pensize(5)
    ball_layer.goto(cx - cap_w, cap_y)
    ball_layer.pendown()
    ball_layer.goto(cx + cap_w, cap_y)
    ball_layer.penup()

    ball_layer.pencolor((160, 170, 190))
    ball_layer.pensize(3)
    ball_layer.goto(cx - cap_w * 0.9, cap_y + cap_h)
    ball_layer.pendown()
    ball_layer.goto(cx + cap_w * 0.9, cap_y + cap_h)
    ball_layer.penup()

    ball_layer.pencolor((200, 200, 220))
    ball_layer.pensize(2)
    ball_layer.goto(cx, cap_y + cap_h)
    ball_layer.pendown()
    ball_layer.goto(cx, STRING_TOP_Y)
    ball_layer.penup()


def points_in_circle(cx: float, cy: float, radius: float, n: int) -> list[tuple[float, float, float]]:
    pts: list[tuple[float, float, float]] = []
    for _ in range(n):
        # rejection sample
        while True:
            x = random.uniform(cx - radius, cx + radius)
            y = random.uniform(cy - radius, cy + radius)
            if (x - cx) ** 2 + (y - cy) ** 2 <= (radius * 0.88) ** 2:
                pts.append((x, y, random.uniform(0, math.tau)))
                break
    return pts


random.seed(42)
SPARKLES = points_in_circle(0, 0, BALL_RADIUS, 75)


def draw_twinkles(cx: float, cy: float, radius: float, phase: float) -> None:
    lights_layer.clear()

    # LED ring
    count = 24
    for i in range(count):
        angle = (math.tau / count) * i
        # Slight wobble so it feels alive
        wobble = 1.6 * math.sin(phase * 1.7 + i * 0.8)
        rr = radius * (0.92 + 0.03 * math.sin(phase + i))
        x = cx + rr * math.cos(angle)
        y = cy + rr * math.sin(angle)

        base = LED_PALETTE[i % len(LED_PALETTE)]
        tw = (math.sin(phase * 2.6 + i * 1.35) + 1) / 2
        col = brighten(base, 0.15 + 0.55 * tw)

        size = int(5 + 6 * tw)
        lights_layer.goto(x + wobble, y)
        lights_layer.dot(size + 6, lerp_color(col, (255, 255, 255), 0.25))
        lights_layer.dot(size, col)

    # Inner sparkles
    for (sx, sy, seed) in SPARKLES:
        tw = (math.sin(phase * 3.2 + seed) + 1) / 2
        if tw < 0.35:
            continue
        # Map sparkle point to current ball center
        x = cx + sx
        y = cy + sy
        size = 1 if tw < 0.65 else 2
        lights_layer.goto(x, y)
        lights_layer.dot(size, (255, 255, 255))


def draw_snow(phase: float) -> None:
    snow_layer.clear()
    snow_layer.penup()
    for flake in SNOWFLAKES:
        # Update
        flake["y"] -= flake["speed"]
        flake["x"] += math.sin(phase * 0.9 + flake["phase"]) * (0.35 * flake["drift"])

        if flake["y"] < -370:
            flake["y"] = 370
            flake["x"] = random.uniform(-510, 510)

        if flake["x"] < -520:
            flake["x"] = 520
        elif flake["x"] > 520:
            flake["x"] = -520

        # Draw (slightly blue-white)
        tint = lerp_color((210, 225, 255), (255, 255, 255), (math.sin(phase + flake["phase"]) + 1) / 2 * 0.45)
        snow_layer.goto(flake["x"], flake["y"])
        snow_layer.dot(flake["size"], tint)


def draw_scene(ball_y: float, phase: float) -> None:
    # Subtle night-sky breathing
    sky = lerp_color((8, 10, 18), (12, 14, 30), (math.sin(phase * 0.6) + 1) / 2 * 0.35)
    screen.bgcolor(sky)

    bg.clear()
    draw_starfield(220)
    # Shadow strengthens as it gets closer to ground
    closeness = clamp((BALL_START_Y - ball_y) / (BALL_START_Y - BALL_GROUND_Y), 0.0, 1.0)
    draw_shadow(BALL_CENTER_X, BALL_GROUND_Y, BALL_RADIUS, closeness)

    draw_gradient_ball(BALL_CENTER_X, ball_y, BALL_RADIUS)
    draw_twinkles(BALL_CENTER_X, ball_y, BALL_RADIUS, phase)
    draw_snow(phase)


def firework_burst(x: float, y: float, base_color: tuple[int, int, int], seed: float) -> None:
    # Animated radial burst on fx_layer
    random.seed(int(seed * 10000))
    rays = 18
    angles = [random.uniform(0, math.tau) for _ in range(rays)]
    lengths = [random.uniform(45, 95) for _ in range(rays)]
    for step in range(1, 15):
        fx_layer.clear()
        phase = time.time()
        draw_scene(BALL_GROUND_Y, phase)

        fx_layer.pensize(2)
        for a, L in zip(angles, lengths):
            t = step / 14
            c = brighten(base_color, 0.35 + 0.55 * (1 - t))
            fx_layer.pencolor(c)
            fx_layer.penup()
            fx_layer.goto(x, y)
            fx_layer.pendown()
            fx_layer.goto(x + math.cos(a) * (L * t), y + math.sin(a) * (L * t))
            fx_layer.penup()
            fx_layer.goto(x + math.cos(a) * (L * t), y + math.sin(a) * (L * t))
            fx_layer.dot(3, brighten(c, 0.35))

        screen.update()
        time.sleep(0.02)


def run_animation() -> None:
    screen.tracer(0, 0)
    draw_starfield(220)

    # Physics-ish drop with bounce
    y = BALL_START_Y
    v = 0.0
    gravity = 0.9
    damp = 0.36
    phase = 0.0

    while True:
        phase += 0.12
        v -= gravity
        y += v
        if y <= BALL_GROUND_Y:
            y = BALL_GROUND_Y
            v = -v * damp
            if abs(v) < 1.2:
                break

        draw_scene(y, phase)
        screen.update()
        time.sleep(0.016)

    # Settle frames
    for _ in range(45):
        phase += 0.12
        draw_scene(BALL_GROUND_Y, phase)
        screen.update()
        time.sleep(0.016)

    # Fireworks
    bursts = [
        (-320, 180, (255, 120, 120)),
        (320, 200, (140, 200, 255)),
        (-120, 260, (255, 230, 140)),
        (140, 280, (190, 140, 255)),
    ]
    for i, (bx, by, col) in enumerate(bursts):
        firework_burst(bx, by, col, seed=0.13 + i * 0.17)

    fx_layer.clear()
    draw_scene(BALL_GROUND_Y, time.time())
    screen.update()

    # Text
    text_layer.clear()
    message = "Here's to a Lousy Christmas and a crappy New Year!"
    text_layer.goto(0, -250)
    text_layer.color((255, 210, 90))
    text_layer.write(message, align="center", font=("Arial", 28, "bold"))
    text_layer.goto(0, -290)
    text_layer.color((210, 210, 230))
    text_layer.write("Have a pizza and a beer maybe!.", align="center", font=("Arial", 16, "normal"))
    screen.update()


run_animation()
turtle.done()
