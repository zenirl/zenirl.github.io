"""
Generate /games/<slug>/ and /apps/<slug>/ index.html for every ZenIRL title.

Run from the zenirl.github.io repo root:
    python3 build_pages.py

The script is the only place per-title metadata lives. Need to edit a tagline?
Touch GAMES (or APPS), re-run, done. Avoids hand-syncing near-identical files.
Games render under /games/, apps (kind="app") under /apps/.
"""

from __future__ import annotations
import os
import textwrap
from dataclasses import dataclass, field
from typing import Optional

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://zenirl.github.io"

@dataclass
class Game:
    slug: str
    name: str
    package: Optional[str]  # None = unpublished
    category: str           # Schema MobileApplication category, plain words
    schema_category: str    # exact value for JSON-LD applicationCategory
    short_desc: str         # ≤160 chars, fits as meta description
    tagline: str            # hero subtitle
    tags: list[str]         # pills (e.g. "Crown", "Arcade")
    accent: str             # CSS color for primary button background
    accent_hover: str
    kind: str = "game"      # "game" → /games/<slug>/, "app" → /apps/<slug>/
    accent_text: str = "#F5F2E8"
    privacy_url: str = ""   # zenirl.github.io/policies/<x>.html
    paragraphs: list[str] = field(default_factory=list)
    features: list[tuple[str, str]] = field(default_factory=list)  # (label, detail)
    screenshot_alts: list[str] = field(default_factory=list)


GAMES: list[Game] = [
    Game(
        slug="asteroid-field",
        name="Asteroid Field",
        package="com.zenirl.asteroids",
        category="Arcade",
        schema_category="GameApplication",
        short_desc="Asteroid arcade for Wear OS. Twist the crown to aim, tap to fire, survive the splitting rocks. Standalone, offline, ad-free.",
        tagline="Asteroid arcade for Wear OS. Crown to aim. Tap to fire. Survive.",
        tags=["Arcade", "Crown control", "Wear OS 3+"],
        accent="#3B82F6", accent_hover="#4F8CF8",
        privacy_url="https://zenirl.github.io/policies/asteroids.html",
        paragraphs=[
            "Classic vector-style asteroids, redesigned for a watch. Your ship sits at the centre of a round play area. Twist the crown to rotate your aim — no thrust, no momentum, just precise rotational control. Tap anywhere to fire in the direction you’re facing.",
            "Large rocks split into mediums; mediums split into smalls. Smalls score the most points but they’re fast, and they all wrap around the bezel — drift off one side, come back on the other. So do your bullets.",
            "Every few destroyed asteroids drops a gold orb. Touch it with your ship and the next eight seconds become triple-shot. Three lives, increasing waves, persistent high score. One round runs sixty to ninety seconds — perfect for a queue, a green light, or a kettle.",
        ],
        features=[
            ("Crown-driven aim", "Analog precision no D-pad can match."),
            ("Vector-style splitting", "Large → 2 medium → 2 small each, just like the original."),
            ("Wave progression", "Each new wave faster and more chaotic."),
            ("Gold power-up orbs", "Eight seconds of triple-shot, dropped randomly."),
            ("Round-screen wrap", "Asteroids and bullets wrap around the bezel."),
            ("Standalone", "No phone, no internet, no permissions beyond the basics."),
        ],
        screenshot_alts=[
            "Asteroid Field gameplay — ship in centre, rocks drifting in from the bezel",
            "Triple-shot power-up active during a wave",
            "Wave clear screen with score and high score",
            "Smaller fast asteroids breaking after a hit",
        ],
    ),
    Game(
        slug="haptic-beat",
        name="Haptic Beat",
        package="com.zenirl.beat",
        category="Music",
        schema_category="GameApplication",
        short_desc="Rhythm game for Wear OS played by feel. The watch buzzes every beat. Tap when it does. No sound, no headphones, no internet.",
        tagline="Haptic rhythm game for Wear OS. Feel each beat on your wrist. No sound needed.",
        tags=["Rhythm", "Haptic", "Touch"],
        accent="#FF6B9D", accent_hover="#FF85B0", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/beat.html",
        paragraphs=[
            "Most rhythm games need audio. This one doesn’t. Your watch buzzes on every beat. A pulse ring contracts toward the centre in time. You tap when the ring meets the inner target. Perfect scores big, good scores some, miss costs you a life.",
            "Trust the haptic and you can play with the screen tucked inside a sleeve. Use the ring as a visual aid while you build the muscle memory. The tempo nudges up every eight beats; by level six or seven you’ll be feeling more than seeing it.",
            "Every level-up grants a power-up: either freeze (next three misses forgiven) or a 2× window for the next five beats. Combo multipliers stack on top of those when you stay perfect. Three lives, persistent high score, no internet permission at all.",
        ],
        features=[
            ("Haptic-first play", "The watch buzzes the beat. You can play without looking."),
            ("Pulse ring visual", "A contracting ring meets the target as the buzz fires."),
            ("Combo multiplier", "Perfect streaks bonus your score."),
            ("Adaptive tempo", "BPM rises with each level-up."),
            ("Two power-ups", "Freeze and 2× score, dropped randomly."),
            ("Quiet by design", "No sound. Perfect for a meeting or a queue."),
        ],
        screenshot_alts=[
            "Haptic Beat gameplay — pulse ring around the target",
            "Score and BPM rising mid-round",
            "Freeze power-up granted between beats",
            "Game over screen with final BPM and high score",
        ],
    ),
    Game(
        slug="sphere-defense",
        name="Sphere Defense",
        package="com.zenirl.defense",
        category="Action",
        schema_category="GameApplication",
        short_desc="Tower defense for Wear OS. Crown rotates your shield, tap to shoot. Three enemy types, bombs, combo multipliers, offline.",
        tagline="Tower defense for Wear OS. Crown rotates your shield. Tap to shoot. Survive.",
        tags=["Action", "Tower defense", "Crown"],
        accent="#00C9A7", accent_hover="#1FD8B8", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/defense.html",
        paragraphs=[
            "Your core sits at the centre. Enemies stream in from the bezel — basic red, slow heavy orange tanks, and fast blue sprinters. The crown rotates a glowing shield arc around your core; tap to fire a bullet in the direction the shield is facing. Two inputs, both used at once.",
            "The shield doesn’t destroy — it bounces. The tap kills. The combination is the whole game: hold the shield against a tank while picking off sprinters with bullets, sweep the shield through clusters to deflect them away from the core, save your bullets for the ones too fast to bounce.",
            "Every ten kills earns a bomb — your next tap detonates everything on screen. Bombs are limited; save them for the moment you can’t. Adaptive difficulty pushes spawn rate and enemy mix higher each wave. Combo multiplier scales from x1 to x8 when you stay alive.",
        ],
        features=[
            ("Twin-input control", "Crown defends, tap attacks."),
            ("Three enemy types", "Red basics, orange tanks (3 HP), blue sprinters."),
            ("Bombs every 10 kills", "Screen-clearing shockwave, on your next tap."),
            ("Combo multiplier", "Scales score from x1 to x8."),
            ("Adaptive waves", "Spawn rate and mix shift as you survive."),
            ("Standalone", "No phone, no internet permission."),
        ],
        screenshot_alts=[
            "Sphere Defense gameplay — shield arc rotated around the core",
            "Mid-wave with multiple enemies inbound",
            "Bomb detonating, screen filled with shockwave particles",
            "Game over screen with high score and wave reached",
        ],
    ),
    Game(
        slug="crown-snake",
        name="Crown Snake",
        package="com.zenirl.snake",
        category="Arcade",
        schema_category="GameApplication",
        short_desc="Classic snake for Wear OS, steered by the rotary crown. Wrap-around round screen, power-ups, persistent high score. Offline.",
        tagline="Snake on your wrist. Twist the crown to steer. A classic for Wear OS.",
        tags=["Arcade", "Crown", "Retro"],
        accent="#66BB6A", accent_hover="#7FCF82", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/snake.html",
        paragraphs=[
            "Snake has been ported to every device with a button. None of them got the control quite right. A rotary crown gives you analog control over heading in a way no D-pad or swipe ever could — it feels like steering, not switching directions.",
            "Eat red apples to grow. Hit a blue orb for five seconds of slow-motion. Grab gold to shrink your tail when it gets unwieldy. The bezel wraps — go off one side, come back on the other. The longer you survive, the faster you move.",
            "One round runs thirty to ninety seconds. The kind of game that fits in the gap between a green light and a coffee being ready. Standalone, offline, no tracking, no internet permission.",
        ],
        features=[
            ("Pure crown control", "No touch, no tilt, no buttons to fight."),
            ("Wrap-around play area", "Uses the entire round screen."),
            ("Three food types", "Grow, slow-mo, and shrink power-ups."),
            ("Adaptive speed", "Gets noticeably faster as you grow."),
            ("Persistent high score", "Survives restarts and reboots."),
            ("Short-burst design", "Built for thirty-second sessions."),
        ],
        screenshot_alts=[
            "Crown Snake mid-game with snake winding around the round arena",
            "Slow-motion power-up active",
            "High-score screen after a long run",
            "Game over with score and previous best",
        ],
    ),
    Game(
        slug="spell-caster",
        name="Spell Caster",
        package="com.zenirl.spell",
        category="Action",
        schema_category="GameApplication",
        short_desc="Glyph-tracing spell game for Wear OS. Draw symbols to destroy enemies before they reach your core. Offline, ad-free, standalone.",
        tagline="Glyph-tracing spell game for Wear OS. Draw symbols. Defend the core.",
        tags=["Action", "Touch", "Brain"],
        accent="#9C27B0", accent_hover="#B040C4",
        privacy_url="https://zenirl.github.io/policies/spell.html",
        paragraphs=[
            "You are the rune. Your finger is the wand. Creatures drift in from the bezel toward your core at the centre. Above each one floats the glyph that destroys it — a circle, a slash, a V. Trace that glyph on your watch face and the matching enemy detonates.",
            "It sounds easy. It isn’t. When three different enemies all head for your core at once, you have to pick which to kill first and trace correctly under pressure. The recognizer is forgiving but not blind. Sloppy circles get rejected. A real V works; a wavy line doesn’t.",
            "Waves 1 and 2 use just two glyphs. Wave 3+ adds the V. Every third wave grants a freeze — enemies stop for a second and a half so you can clear a swarm in calm. Three core hits and the run ends.",
        ],
        features=[
            ("Gesture recognition", "Custom unistroke recogniser, generous but not blind."),
            ("Three glyphs", "Unlocked progressively as you survive waves."),
            ("Combo multiplier", "Chain kills for extra score."),
            ("Freeze power-up", "Every third wave — clear a swarm in calm."),
            ("Atmospheric star-field", "Subtle parallax behind every fight."),
            ("Standalone", "No phone, no internet permission."),
        ],
        screenshot_alts=[
            "Spell Caster gameplay — glyph being traced with finger trail",
            "Multiple enemies inbound, each with floating glyph",
            "Freeze power-up active, enemies suspended",
            "Game over screen with wave reached and high score",
        ],
    ),
    Game(
        slug="crown-lockpick",
        name="Crown Lockpick",
        package="com.zenirl.lockpick",
        category="Puzzle",
        schema_category="GameApplication",
        short_desc="Lockpicking heist for Wear OS, played by haptic feel. Sweep the crown, listen for the buzz, crack five locks before the alarm.",
        tagline="Lockpicking heist for Wear OS. Pick five locks by haptic feel. No looking.",
        tags=["Puzzle", "Crown", "Haptic"],
        accent="#FFB74D", accent_hover="#FFC169", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/lockpick.html",
        paragraphs=[
            "Five locks in a row. Crack them all to breach the vault. Fail one and the alarm trips. Each lock raises the stakes — Padlock with three pins and wide tolerance, Deadbolt with decoys, Safe with narrower zones, Master with pins picked in random order, then Vault: six pins, tightest tolerances, sixty seconds.",
            "Turn the crown to sweep a virtual pick around the dial. When the pick crosses a real pin’s set zone, the watch fires a hot haptic pulse on your wrist. That pulse is the entire game — find that spot again, hold the crown still, and if it keeps pulsing you’ve got the real pin. Tap to commit.",
            "There is no visual marker for where the set zones are. Everything is felt. The decoys exist to teach you the difference between a pin that pulses on every sweep and one that keeps pulsing when you stop. You can crack a lock with the watch face in your sleeve — by feel alone.",
        ],
        features=[
            ("Five lock types", "Padlock, Deadbolt, Safe, Master, Vault."),
            ("Decoy pins", "Some pulse on every sweep; only the real one keeps pulsing."),
            ("Random-order locks", "Master and Vault pick pins in random order."),
            ("Pure haptic feedback", "No visual marker for set zones — feel them."),
            ("Per-lock timers", "Tightening from 30s on the Padlock to 60s on the Vault."),
            ("Standalone", "No phone, no internet."),
        ],
        screenshot_alts=[
            "Crown Lockpick padlock — first lock with three pins",
            "Set pin lit while sweeping the dial",
            "Vault lock with six pins and tight timer",
            "Heist complete screen after five successful picks",
        ],
    ),
    Game(
        slug="morse-tap",
        name="Morse Tap",
        package="com.zenirl.morse",
        category="Puzzle",
        schema_category="GameApplication",
        short_desc="Learn Morse code by feel on Wear OS. The watch buzzes a short word; tap it back dit by dah. A trainer disguised as a puzzle.",
        tagline="Learn Morse code by feel. Watch buzzes a word — tap it back. Wear OS game.",
        tags=["Puzzle", "Trainer", "Haptic"],
        accent="#FFC107", accent_hover="#FFD54F", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/morse.html",
        paragraphs=[
            "A Morse trainer disguised as a tap-back puzzle. The watch buzzes a short word in Morse on your skin. You tap it back — short tap is a dit, long press is a dah. Match every bit and the next round adds a letter. One mistake ends the run.",
            "If you don’t know Morse, you’ll start learning it inside five minutes. The early rounds show the pattern visually as it buzzes, so each tap also lines up with something you can see. By round eight common words like HELP, HOPE, SOS and LOVE begin to feel obvious.",
            "Hard rounds (9+) hide the pattern — the word remains on screen, but you’re tapping from the haptic alone. Playback speeds up by a few milliseconds each round, so by round nineteen you’re tapping at near-real Morse cadence.",
        ],
        features=[
            ("Haptic-first trainer", "Built around the watch’s vibration motor."),
            ("Visual scaffolding", "Pattern shown in early rounds; hidden later."),
            ("Bit-level feedback", "Each correct dit/dah lights green as you nail it."),
            ("Curated word lists", "HELP, HOPE, LOVE, SOS — words you might actually use."),
            ("Adaptive cadence", "Playback speeds up with every hard round."),
            ("Standalone", "No phone, no internet."),
        ],
        screenshot_alts=[
            "Morse Tap easy round showing dits and dahs being tapped",
            "Hard round with word visible but pattern hidden",
            "Bit-level success — correct letter lit green",
            "Run summary with round reached and accuracy",
        ],
    ),
    Game(
        slug="crown-pinball",
        name="Crown Pinball",
        package="com.zenirl.pinball",
        category="Arcade",
        schema_category="GameApplication",
        short_desc="Pinball for Wear OS. The crown is the paddle. Real ball physics, coloured bumpers, multipliers up to x8. Standalone, offline, ad-free.",
        tagline="Pinball for your watch. Crown is the paddle. Wear OS arcade, no phone needed.",
        tags=["Arcade", "Crown", "Physics"],
        accent="#FF7043", accent_hover="#FF8A65",
        privacy_url="https://zenirl.github.io/policies/pinball.html",
        paragraphs=[
            "Pinball redesigned for a round screen and a rotary crown. The crown rotates a glowing paddle around the bottom arc of the bezel — the kind of analog control idea you can only really pull off on a watch. The entire round face is the table; no wasted real estate.",
            "Three bumpers cluster in the upper half — yellow standard, red hot for big points, blue cool. Hit the same bumper repeatedly and your multiplier climbs from x1 all the way to x8. Chain five bumpers without losing the ball and the paddle widens for six seconds. The only second chance you get.",
            "The ball has real gravity, real bounce, and a slight after-image trail so you can read its arc. Three balls per game, score-chase progression, persistent personal best. One game runs sixty to one-eighty seconds.",
        ],
        features=[
            ("Crown paddle", "Smooth analog control along the drain arc."),
            ("Real ball physics", "Gravity, bounce, after-image trail."),
            ("Three coloured bumpers", "Yellow standard, red hot, blue cool."),
            ("Multiplier x1–x8", "Climbs as you keep the ball alive."),
            ("Wide-paddle bonus", "Chain five bumpers; paddle widens for 6s."),
            ("Standalone", "No phone, no internet permission."),
        ],
        screenshot_alts=[
            "Crown Pinball table with paddle on the bottom arc and ball in flight",
            "Multiplier climbing after consecutive bumper hits",
            "Wide-paddle bonus active after a five-chain",
            "Score-chase summary at end of round",
        ],
    ),
    Game(
        slug="safecracker",
        name="Safecracker",
        package="com.zenirl.safecracker",
        category="Puzzle",
        schema_category="GameApplication",
        short_desc="Combination-lock puzzle for Wear OS. Spin the crown, feel the gate buzz, crack five safes before the alarm. Haptic-first, offline.",
        tagline="Combination-lock puzzle for Wear OS. Spin the crown. Feel the gate buzz.",
        tags=["Puzzle", "Crown", "Haptic"],
        accent="#B0BEC5", accent_hover="#CFD8DC", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/safecracker.html",
        paragraphs=[
            "The crown is your dial. The vibration motor is your tell. Five safes between you and the vault, each meaner than the last — Wall Safe with ten numbers, Bank with twenty narrower clicks, Time with thirty and a four-digit combo, Vault with forty, then the Museum: forty numbers, four digits, dial-tick haptic muted.",
            "Spin the crown to turn the dial. Every number you cross fires a tiny tick haptic, like a real combination spindle. When you cross the secret number for the current digit, while moving in the right direction, the watch fires a soft gate buzz. That gate buzz is the only signal you get.",
            "Real combination locks have a slight feel-change at the gate. This game uses the haptic motor to recreate that exact moment on your wrist. After each digit, the expected direction flips — first clockwise, second counter, third clockwise, just like a real spindle. Spin the wrong way and gate buzz won’t fire at all.",
        ],
        features=[
            ("Five safe types", "Wall, Bank, Time, Vault, Museum."),
            ("Gate-buzz haptic", "Recreates the feel-change of a real combination lock."),
            ("Direction discipline", "After each digit the expected direction flips."),
            ("Per-safe timers", "Wall 35s up to Museum 90s."),
            ("Silent finale", "Museum strips the per-number tick — gate buzz only."),
            ("Standalone", "No phone, no internet."),
        ],
        screenshot_alts=[
            "Safecracker wall safe — ten numbers on the dial",
            "Vault safe with finer ticks and four-digit combo",
            "Locked digit indicator showing direction flip",
            "Heist complete after all five safes cracked",
        ],
    ),
]


APPS: list[Game] = [
    Game(
        slug="step-pet",
        name="Step Pet",
        package="com.zenirl.stepapp",
        kind="app",
        category="Health & Fitness",
        schema_category="HealthApplication",
        short_desc="Walk to raise a tiny pet on your watch — a step counter that's actually fun. Your steps grow it, dress it, and send it on adventures. Offline, ad-free.",
        tagline="Walk to raise a tiny pet on your wrist. A step counter that's actually fun.",
        tags=["Health & Fitness", "Steps", "Virtual pet"],
        accent="#43A047", accent_hover="#58B45B", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/steppet.html",
        paragraphs=[
            "Your watch already counts your steps. Step Pet gives them a point. Every walk feeds a tiny creature that lives on your wrist — earning coins, sending it on little adventures, and slowly raising it from a speckled egg into a fully grown companion. No phone required.",
            "Spend the coins you earn in a shop of hats, scarves, glasses and crowns. Hit your daily step goal to send your pet on an adventure — it comes back with a short story and a treasure. Keep a daily streak going for bonus rewards. Your pet grows through five stages — Egg, Baby, Kid, Teen, Adult — and reaching Adult takes about a month of real walking. Raise all six species; once one grows up, adopt the next.",
            "Gentle by design: there’s no failure state and no nagging — your pet never dies, and you’ll get at most one friendly notification a day. A glanceable Tile shows your pet, today’s steps and progress to goal; a watch-face complication gives you a steps-to-goal ring you can tap to open the app. Drawn entirely in code, so it stays crisp on any round screen. Works completely offline — no internet permission, no accounts, no ads, no tracking.",
        ],
        features=[
            ("Steps raise your pet", "Real step count from your watch — no phone needed."),
            ("Coins & shop", "Earn coins as you walk; spend them on hats, scarves, glasses and crowns."),
            ("Daily adventures", "Hit your step goal to send your pet off — it returns with a story and treasure."),
            ("Growth & streaks", "Five stages from Egg to Adult, six species to raise, streak rewards for showing up."),
            ("Tile + complication", "A glanceable Tile and a tappable steps-to-goal ring on your watch face."),
            ("Private & offline", "No internet permission, no accounts, no ads, no tracking."),
        ],
        screenshot_alts=[
            "Step Pet home — your pet with today’s steps and progress to goal",
            "The shop — cosmetics you can buy with earned coins",
            "An adventure result with a short story and treasure",
            "The species family — six pets to raise",
        ],
    ),
]


def render_game(g: Game) -> str:
    base = "apps" if g.kind == "app" else "games"          # URL + asset namespace
    nav_href, nav_label = ("/#apps", "Apps") if g.kind == "app" else ("/#available", "Games")
    all_label = "All apps" if g.kind == "app" else "All games"
    play_url = f"https://play.google.com/store/apps/details?id={g.package}" if g.package else None
    canonical = f"{BASE_URL}/{base}/{g.slug}/"
    icon_url = f"{BASE_URL}/assets/{base}/{g.slug}/icon.png"
    feature_url = f"{BASE_URL}/assets/{base}/{g.slug}/feature.png"
    title = f"{g.name} — {g.category} for Wear OS · ZenIRL"

    # JSON-LD MobileApplication. Conditionally include offers for published apps.
    schema_offers = ""
    if g.package:
        schema_offers = ''',
      "downloadUrl": "''' + play_url + '''",
      "installUrl": "''' + play_url + '''",
      "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" }'''

    schema = textwrap.dedent(f'''
    {{
      "@context": "https://schema.org",
      "@type": "MobileApplication",
      "name": "{g.name}",
      "description": "{g.short_desc}",
      "operatingSystem": "Wear OS 3+",
      "applicationCategory": "{g.schema_category}",
      "image": "{icon_url}",
      "url": "{canonical}",
      "author": {{
        "@type": "Organization",
        "name": "ZenIRL",
        "url": "{BASE_URL}/"
      }}{schema_offers}
    }}''').strip()

    cta_block = (
        f'<a class="btn" href="{play_url}" rel="noopener" target="_blank">Get on Google Play</a>'
        if play_url
        else '<span class="btn btn-coming">Coming soon</span>'
    )
    if g.privacy_url:
        cta_block += f'\n        <a class="btn btn-secondary" href="{g.privacy_url}">Privacy policy</a>'

    tag_pills = "\n          ".join(f'<span class="tag">{t}</span>' for t in g.tags)

    paragraphs = "\n      ".join(f"<p>{p}</p>" for p in g.paragraphs)

    feature_items = "\n        ".join(
        f"<li><strong>{label}</strong>{detail}</li>" for label, detail in g.features
    )

    screenshots = "\n          ".join(
        f'<figure class="bezel"><img loading="lazy" src="/assets/{base}/{g.slug}/screenshot-{i+1}.png" alt="{alt}" width="220" height="220"></figure>'
        for i, alt in enumerate(g.screenshot_alts)
    )

    return textwrap.dedent(f'''\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{g.short_desc}">
  <link rel="canonical" href="{canonical}">
  <link rel="stylesheet" href="/assets/css/styles.css">
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">

  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{g.short_desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{feature_url}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{g.short_desc}">
  <meta name="twitter:image" content="{feature_url}">

  <script type="application/ld+json">
{schema}
  </script>

  <style>
    :root {{
      --game-accent: {g.accent};
      --game-accent-hover: {g.accent_hover};
      --game-accent-text: {g.accent_text};
    }}
  </style>
</head>
<body>
  <a href="#main" class="skip-link">Skip to content</a>

  <header class="site-header">
    <div class="container">
      <div class="brand"><a href="/">ZenIRL</a></div>
      <nav aria-label="Primary">
        <a href="{nav_href}">{nav_label}</a>
      </nav>
    </div>
  </header>

  <main id="main">
    <section class="container game-hero">
      <img class="game-icon" src="/assets/{base}/{g.slug}/icon.png" alt="{g.name} app icon" width="160" height="160">
      <div>
        <h1>{g.name}</h1>
        <p class="tagline">{g.tagline}</p>
        <div class="tag-row">
          {tag_pills}
        </div>
        <div class="cta-row">
        {cta_block}
        </div>
      </div>
    </section>

    <article class="container prose">
      {paragraphs}

      <h2>Features</h2>
      <ul>
        {feature_items}
      </ul>
    </article>

    <section class="container gallery">
      <h2 class="section-heading">Screenshots</h2>
      <div class="gallery-row">
          {screenshots}
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>&copy; 2026 ZenIRL · <a href="mailto:zencandev@gmail.com">zencandev@gmail.com</a></p>
      <p><a href="/">{all_label}</a></p>
    </div>
  </footer>
</body>
</html>
''')


def main() -> None:
    for g in GAMES + APPS:
        base = "apps" if g.kind == "app" else "games"
        out_dir = os.path.join(ROOT, base, g.slug)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(render_game(g))
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
