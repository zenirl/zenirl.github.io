"""
Generate /games/<slug>/ and /apps/<slug>/ index.html for every ZenIRL title.

Run from the zenirl.github.io repo root:
    python3 build_pages.py

The script is the only place per-title metadata lives. Need to edit a tagline?
Touch GAMES (or APPS), re-run, done. Avoids hand-syncing near-identical files.
Games render under /games/, apps (kind="app") under /apps/.
"""

from __future__ import annotations
import html
import os
import textwrap
from dataclasses import dataclass, field
from typing import Optional

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://zenirl.github.io"


def _lum(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    ch = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        ch.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def _contrast(a: str, b: str) -> float:
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def readable_text(bg: str, preferred: str) -> str:
    """Keep the configured button text colour if it meets WCAG AA (4.5:1), otherwise pick dark/light."""
    if _contrast(bg, preferred) >= 4.5:
        return preferred
    dark, light = "#161616", "#F5F2E8"
    return dark if _contrast(bg, dark) >= _contrast(bg, light) else light

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
    hero_shot: int = 1       # which screenshot (1-based) leads the page + home showcase
    title_name: str = ""     # name used in <title>/og/JSON-LD when it differs from the short display name (Play title)


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
    Game(
        slug="brick-breaker",
        name="Brick Breaker",
        package=None,
        category="Arcade",
        schema_category="GameApplication",
        short_desc="Brick breaker for Wear OS. The crown orbits the paddle around the rim; tap to launch. Concentric brick rings, power-ups, offline.",
        tagline="Brick breaker for Wear OS. The crown is your paddle, all the way around.",
        tags=["Arcade", "Crown", "Breakout"],
        accent="#4FC3F7", accent_hover="#6FD0F9", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/brick.html",
        paragraphs=[
            "Breakout, rebuilt for a round screen. The bricks sit in the centre as concentric coloured rings; the crown sweeps your paddle all the way around the bezel. Tap to launch the ball and keep it alive.",
            "The whole circle is the wall — except where your paddle is. Let the ball reach the rim where you aren’t and you lose one of three lives. Clear every ring to advance: faster ball, more rings. Broken bricks sometimes drop multi-ball, a wider paddle, or a slow-ball window.",
        ],
        features=[
            ("Crown paddle", "Orbits the full rim — analog control a phone can’t match."),
            ("Round-screen bricks", "Concentric rings fill the watch face."),
            ("Three power-ups", "Multi-ball, wide paddle, slow ball."),
            ("Rising difficulty", "Each level adds rings and ball speed."),
            ("Standalone", "No phone, no internet permission."),
        ],
        screenshot_alts=[
            "Brick Breaker gameplay — concentric brick rings with paddle and ball",
            "A fresh level with full rings of bricks",
            "Title screen with the crown paddle on the rim",
            "How to play — the crown moves the paddle",
        ],
    ),
    Game(
        slug="crown-darts",
        name="Crown Darts",
        package="com.zenirl.darts",
        category="Arcade",
        schema_category="GameApplication",
        short_desc="Darts for Wear OS. The crown aims around a real dartboard; a power marker times your throw. Nine darts, score big on triples and the bull.",
        tagline="Darts for Wear OS. Crown to aim, time the power, hit the bullseye.",
        tags=["Arcade", "Sports", "Crown"],
        accent="#E53935", accent_hover="#EF5350",
        privacy_url="https://zenirl.github.io/policies/darts.html",
        paragraphs=[
            "A full dartboard on your wrist — twenty sectors in the right order, double and triple rings, outer and inner bull. The crown swings your aim around the board while a power marker sweeps from centre to edge. Tap at the right instant and the dart lands where aim meets power.",
            "Score Attack gives you nine darts to rack up the highest total. Triple-twenty and the bullseye are there for the taking — if your timing is sharp. Persistent best score, fully offline.",
        ],
        features=[
            ("Crown aim + timed power", "Two-part skill on every throw."),
            ("Real dartboard scoring", "Sectors, doubles, triples, outer and inner bull."),
            ("Score Attack", "Nine darts to maximise your total."),
            ("Persistent best", "Your top nine-dart total survives reboots."),
            ("Standalone", "No phone, no internet permission."),
        ],
        screenshot_alts=[
            "Crown Darts gameplay — a dart landed with the score on the board",
            "The full dartboard, ready to aim",
            "How to play — the crown aims around the board",
        ],
    ),
    Game(
        slug="helix-drop",
        name="Helix Drop",
        package="com.zenirl.helix",
        category="Arcade",
        schema_category="GameApplication",
        short_desc="Helix ball-drop for Wear OS. The ball falls on its own; spin the crown to line up the gaps and thread it inward. Avoid the red rings.",
        tagline="Helix for Wear OS. The ball drops — spin the crown to thread the gaps.",
        tags=["Arcade", "Crown", "Reflex"],
        accent="#1DE9B6", accent_hover="#4DEFC6", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/helix.html",
        paragraphs=[
            "A crown-native take on the helix games you know. A ball descends from the rim toward a glowing core, locked to the top of the screen. Spin the crown to rotate the concentric rings so a gap lines up the instant the ball arrives — thread it through to the next ring.",
            "Miss the gap, or hit a red hazard arc, and the run ends. Reach the core to clear the level; deeper levels add more rings, tighter gaps, and rings that drift on their own. Pure crown skill, fully offline.",
        ],
        features=[
            ("Crown is the control", "Rotate the rings; the ball falls on its own."),
            ("Thread the gaps", "Line a gap up at the top before the ball lands."),
            ("Hazard rings", "Red arcs end the run — read them fast."),
            ("Escalating levels", "More rings, smaller gaps, auto-rotation."),
            ("Standalone", "No phone, no internet permission."),
        ],
        screenshot_alts=[
            "Helix Drop gameplay — ball at the top, spiral rings around the core",
            "Title screen with the falling ball",
            "How to play — spin the crown to thread the gaps",
        ],
    ),
    Game(
        slug="crown-fishing",
        name="Crown Fishing",
        package=None,
        category="Casual",
        schema_category="GameApplication",
        short_desc="Fishing game for Wear OS. Tap to cast, feel the bite, then spin the crown to reel — ease off when the line strains or it snaps.",
        tagline="Fishing for Wear OS. The crown is your reel. Feel the bite.",
        tags=["Casual", "Simulation", "Crown"],
        accent="#29B6F6", accent_hover="#4FC3F7", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/reel.html",
        paragraphs=[
            "Cast with a tap, then wait — the watch buzzes the moment a fish bites. Now the crown becomes your reel: spin to bring the fish in, watching a progress bar climb toward landing it and a tension bar climb toward snapping the line.",
            "Fish run when you least expect it; reel through a run and the tension spikes fast, so you ease off, let it settle, then resume. Land it before the line snaps. Every catch is a different species and size, and the session ends when a line finally snaps. Offline, with distinctive bite and snap haptics.",
        ],
        features=[
            ("The crown is the reel", "Spin to reel — the most natural control there is."),
            ("Feel the bite", "A distinctive buzz the instant a fish strikes."),
            ("Tension vs progress", "Ease off during a run or the line snaps."),
            ("Catch and collect", "Random species and sizes, chasing your best."),
            ("Standalone", "No phone, no internet permission."),
        ],
        screenshot_alts=[
            "Crown Fishing — line cast over the water, waiting for a bite",
            "Title screen with the water scene",
            "How to play — tap to cast, spin the crown to reel",
        ],
    ),
    Game(
        slug="memory-buzz",
        name="Memory Buzz",
        package="com.zenirl.memory",
        category="Puzzle",
        schema_category="GameApplication",
        short_desc="Memory game for Wear OS with a twist — each colour has its own haptic, so you can follow the sequence by feel. Watch, feel, tap it back.",
        tagline="Memory game for Wear OS. Each colour buzzes differently — play by feel.",
        tags=["Puzzle", "Brain", "Haptic"],
        accent="#43A047", accent_hover="#58B45B", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/memory.html",
        paragraphs=[
            "Simon, reimagined for the wrist. Four coloured quadrants ring the screen, and each one has its own vibration signature — so you can follow the growing sequence partly by feel, not just by sight.",
            "Watch and feel the pattern, then tap the colours back in order. Get it right and the sequence grows by one; a single wrong tap ends the run. How long a sequence can you hold? Offline, with a persistent high score.",
        ],
        features=[
            ("A haptic per colour", "Each quadrant buzzes differently — play by feel."),
            ("Classic Simon loop", "Watch, repeat, the sequence grows."),
            ("One-mistake tension", "A single wrong tap ends the run."),
            ("Persistent high score", "Your longest sequence is saved."),
            ("Standalone", "No phone, no internet permission."),
        ],
        screenshot_alts=[
            "Memory Buzz — four coloured quadrants around the title",
            "Your turn — tapping the sequence back",
            "How to play — watch and feel the colour sequence",
        ],
    ),
    Game(
        slug="crown-ace",
        name="Crown Ace",
        package=None,
        category="Arcade",
        schema_category="GameApplication",
        short_desc="Vertical space shooter for Wear OS. Turn the crown to fly, weave rocks and laser gates, graze bullets, beat the bosses. Free and offline.",
        tagline="Space shooter for Wear OS. Turn the crown to fly. Weave rocks and lasers, beat the bosses.",
        tags=["Arcade", "Action", "Shooter"],
        accent="#FF7043", accent_hover="#FF8A65", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/ace.html",
        paragraphs=[
            "A vertical space shooter built for the crown. Turn it to slide your jet left and right. Your guns fire on their own, so your whole job is flying: threading rocks, slipping through laser gates and staying alive.",
            "Six sectors, each with its own sky: Kepler Drift, Crimson Rift, Emerald Deep, Solar Storm, Frost Moon and the Fleet Graveyard. Each opens with a title card, throws waves of enemies at you, adds a hazard stretch, and ends in a boss. Then the next sector begins, a little harder.",
            "Skim past bullets without being hit to fill the graze meter. A full meter earns a nova. Tap the screen for a nova bomb that wipes bullets and damages everything near you. Each hit burns one weapon level, so staying clean keeps you strong.",
            "Free, offline, no ads, no in-app purchases, no tracking. Wear OS 3+.",
        ],
        features=[
            ("Crown flight", "Turn the crown to slide left and right. Guns fire on their own."),
            ("Six sectors", "Waves, a hazard stretch, then a boss. Each sector is a little harder."),
            ("Seven enemy types", "Drones, swoopers, kamikazes, gunships, mines, lancers and shielded ships."),
            ("Hazards", "Indestructible asteroids, laser gates with sliding gaps, canyon walls and debris corridors."),
            ("Graze and nova", "Skim bullets to fill the meter. A full meter earns a nova; tap for a nova bomb."),
            ("Eight bosses", "Four mini-bosses and four big ones. Shoot the armour off to expose the core."),
            ("Power-up orbs", "Overcharged guns, a shield, a spare bomb, an extra life."),
            ("Standalone", "Offline. Best score saved on the watch. Mute button on the title screen."),
        ],
        screenshot_alts=[
            "Crown Ace title card over a ringed planet, with the best score and a nova-bomb hint",
            "Sector 5: the jet fires up the screen at a rock and a cratered moon",
            "Dreadnought boss: a wide armoured ship with turrets, an orange blast and a bullet stream",
            "Star Lance boss: a glowing blue core ship above the player's jet in a green nebula",
        ],
        hero_shot=3,
    ),
    Game(
        slug="rewind",
        name="Rewind",
        title_name="Rewind: Crown Time Courier",
        package=None,
        category="Puzzle",
        schema_category="GameApplication",
        short_desc="Puzzle platformer for Wear OS. Turn the crown to move time, rewind the traps and reach the exit. 30 levels in five chapters. Free and offline.",
        tagline="Puzzle platformer for Wear OS. The crown is time. Rewind the traps, reach the exit.",
        tags=["Puzzle", "Arcade", "Casual"],
        accent="#42A5F5", accent_hover="#64B5F6", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/rewind.html",
        paragraphs=[
            "A puzzle platformer where the crown is time. Turn it forward and the world runs. Turn it back and everything rewinds: blades, doors, moving platforms, you. Tap to hold still while time runs on, and tap again to walk.",
            "Rewinding costs charge. It drains the blue bar, and walking refills it slowly, so you cannot simply undo everything. Plan your steps, wait out a trap, then rewind only the moment that went wrong. A hit costs an hourglass. Finish under par time to earn three stars.",
            "30 levels in five chapters: Tick, Swing, Locks, Unbound and Collapse. Each has its own place and its own rule. Every sixth level is a boss.",
            "Free, offline, no ads, no in-app purchases, no tracking. Wear OS 3+.",
        ],
        features=[
            ("Crown is time", "Forward runs the world. Back rewinds traps, doors, platforms and you."),
            ("Rewind has a cost", "The blue bar drains as you rewind and refills slowly as you walk."),
            ("30 levels, five chapters", "Tick, Swing, Locks, Unbound, Collapse. Each adds its own rule."),
            ("Boss levels", "Every sixth level. The final Timekeeper uses everything you have learned."),
            ("Three stars", "Finish under par time."),
            ("Short hints", "Every level starts with a hint, so a new rule never catches you cold."),
            ("Standalone", "Offline. Sound effects with a mute button on the title screen."),
        ],
        screenshot_alts=[
            "Rewind title card: the crown is time, with 77 of 90 stars and a tap-to-begin prompt",
            "Level 1.2: a glowing red blade sweeps around a hub, with the rewind charge bar and the hourglasses above",
            "Boss level 12, Clockmaster: moons circle between a spinning blade and the edge of the screen",
            "Chapter select: the Timekeeper boss level inside a ring of coloured level dots",
        ],
        hero_shot=2,
    ),
    Game(
        slug="beacon",
        name="Beacon",
        package=None,
        category="Puzzle",
        schema_category="GameApplication",
        short_desc="Lighthouse puzzle for Wear OS. Swing the beam with the crown and guide ships safely to the quay. 24 nights, four seas. Free and offline.",
        tagline="Lighthouse puzzle for Wear OS. Swing the beam. Bring every ship home.",
        tags=["Puzzle", "Strategy", "Casual"],
        accent="#FFCA28", accent_hover="#FFD54F", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/beacon.html",
        paragraphs=[
            "You are in the lighthouse. Ships steer for whatever your beam lights up, and your job is to bring every one of them home to the quay. Turn the crown to swing the beam, or touch and drag on the sea.",
            "A lit ship steers for the quay. Leave it in the dark and it holds its course only so long, shown by a ring around the ship. Light it again before it runs out. Tap the lighthouse to sound the horn and slow every ship. Blasts are few: dock five ships to earn one.",
            "24 nights across four seas: Home Waters, The Northern Sound, The Deep Reach and The Black Gale. Every sixth night is a boss night.",
            "Free, offline, no ads, no in-app purchases, no tracking. Wear OS 3+.",
        ],
        features=[
            ("Crown-swung beam", "Or touch and drag on the sea."),
            ("Hold the course", "A ring shows how long an unlit ship keeps its heading."),
            ("Horn", "Slows every ship. Dock five ships to earn one blast."),
            ("24 nights, four seas", "Each sea adds new hazards and rules."),
            ("Boss nights", "Every sixth night. Some are beaten only by holding the beam on them."),
            ("Three stars per night", "Based on how many ships you bring in."),
            ("Standalone", "Offline. Sound and music with a mute button on the title screen."),
        ],
        screenshot_alts=[
            "Beacon title card: Night 18, Leviathan, a boss level with 51 of 72 stars",
            "A lighthouse in the centre throws a pale beam across dark water towards a ship",
            "Two ships on the water, one inside a pink targeting ring as the beam swings towards it",
            "A segmented green sea creature crosses the top of the screen in a red-tinted night",
        ],
        hero_shot=3,
    ),
    Game(
        slug="orbital",
        name="Orbital",
        package=None,
        category="Puzzle",
        schema_category="GameApplication",
        short_desc="Slingshot puzzle for Wear OS. Orbit planets, let go at the right moment and fly your comet home. 24 star systems. Free and offline.",
        tagline="Slingshot puzzle for Wear OS. Orbit, release, fly the comet home.",
        tags=["Puzzle", "Arcade", "Space"],
        accent="#AB47BC", accent_hover="#BA68C8", accent_text="#F5F2E8",
        privacy_url="https://zenirl.github.io/policies/orbital.html",
        paragraphs=[
            "A one-finger slingshot puzzle for the crown. You are a comet circling a planet. Turn the crown, or drag up and down, to widen or tighten your orbit: a tighter orbit is faster. Tap to let go. A trail of dots shows exactly where you will fly, so the game is about timing, not guessing.",
            "Fly to the next world and your comet freezes on its new orbit. Grab stardust to refreeze your comet on the way, dodge rocks and moons, and dive into the wormhole to finish the system. You get three comets. Each crash costs one.",
            "24 star systems in four sectors: Cradle, Drift, Furnace and Abyss. The sixth system in each sector is a boss.",
            "Free, offline, no ads, no in-app purchases, no tracking. Wear OS 3+.",
        ],
        features=[
            ("Crown orbit control", "Or drag up and down. Tighter orbit, faster comet."),
            ("Trajectory preview", "A dotted trail shows where you will fly."),
            ("24 star systems", "Four sectors, each opening with a twist shown on its arrival card."),
            ("Hazards", "Rocks, moons, drifting and collapsing worlds, black holes, flares."),
            ("Boss systems", "Collect every red key before the wormhole opens."),
            ("Three comets", "Each crash costs one. Lose all and the sector restarts."),
            ("Standalone", "Offline. Sound effects with a mute button on the title screen."),
        ],
        screenshot_alts=[
            "Orbital title card: Furnace sector, systems 13 to 18, star count and a tap-to-launch prompt",
            "Level 19, Undertow: a comet with a white tail leaves a planet orbit, with black holes and star targets around it",
            "Sector 4, The Abyss: a banner explains that portals fling you across space",
            "Sector 3, The Furnace: a banner explains that exits open and shut, over a red sun",
        ],
        hero_shot=2,
    ),
    Game(
        slug="echo",
        name="Echo",
        package=None,
        category="Puzzle",
        schema_category="GameApplication",
        short_desc="Sonar dive for Wear OS. Steer a tiny sub through a black abyss by sonar, touch and sound. 24 dives across four depth zones. Free and offline.",
        tagline="Sonar dive for Wear OS. The screen is black until you ping.",
        tags=["Puzzle", "Adventure", "Atmospheric"],
        accent="#26C6DA", accent_hover="#4DD0E1", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/echo.html",
        paragraphs=[
            "A dive into total darkness. Your submersible drifts forward on its own. Turn the crown to steer, or press and drag. The screen stays black until you tap. Each tap sends out a sonar ping that rolls through the tunnels and draws the rock it touches in glowing outlines. Then the outlines fade, and you are steering from memory.",
            "Your wrist is the second instrument. Soft ticks quicken as rock closes in, so you can feel a wall before you see it. A heavier heartbeat means something with teeth is near.",
            "Find the relics hidden in each cave, then reach the exit vent before your air runs out. Pings are limited; each relic gives two back. Hull is never repaired mid-dive.",
            "24 dives across four zones: Twilight, Midnight, Abyssal and Hadal. Every sixth dive is a boss dive.",
            "Free, offline, no ads, no IAP, no tracking. Wear OS 3+.",
        ],
        features=[
            ("Sonar-only vision", "Tap to ping. Outlines fade, so you steer from memory."),
            ("Haptic proximity", "Ticks quicken near rock. A heartbeat means a hunter is close."),
            ("Limited pings", "A fixed number per dive. Each relic gives two back."),
            ("Four depth zones", "Twilight, Midnight, Abyssal, Hadal. Each announces its twist."),
            ("Hunters and boss dives", "Hunters follow your pings. Every sixth dive has a leviathan."),
            ("Three stars per dive", "Hull intact and air to spare. Caves are the same every time."),
            ("Crown or touch", "Hold the centre of the screen to pause."),
            ("Standalone", "Offline. All sound is synthesised on the watch, with a mute button."),
        ],
        screenshot_alts=[
            "Echo title card: dive 12, Leviathan, midnight zone at 4870 metres, a boss dive",
            "A yellow submarine at 5182 metres sees sonar-drawn cave walls in blue and a pink anglerfish",
            "The same dive at 5163 metres with the anglerfish closer, 10 pings used and a relic marker",
            "A deeper dive at 10,295 metres with a red-tinted screen and an anglerfish beside the sub",
        ],
        hero_shot=2,
    ),
    Game(
        slug="firefly",
        name="Firefly",
        package=None,
        category="Casual",
        schema_category="GameApplication",
        short_desc="Night-time herding game for Wear OS. Walk a lantern and lead a swarm of fireflies into their jars. 24 nights, four scenes. Free and offline.",
        tagline="Herding game for Wear OS. Carry the lantern. Lead the fireflies to their jars.",
        tags=["Casual", "Puzzle", "Relaxing"],
        accent="#C0CA33", accent_hover="#D4E157", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/firefly.html",
        paragraphs=[
            "A gentle night-time herding game. You carry the lantern. A swarm of fireflies follows its glow, and every night your job is to lead them into the jars before the dark takes them.",
            "Tap the meadow and the lantern walks there, with the swarm drifting after it. The crown steers too. Tap the lantern to flare: a burst of light that holds the swarm together in a gust and can scare off the owl. Flares are few, and a full jar earns one back.",
            "Webs, frogs, bats, wind and rain all take fireflies. Lose too many and the night is over. 24 nights in four scenes: Summer Meadow, Rainy Marsh, Dark Forest and Moonlit Pond. Every sixth night a boss hunts the swarm.",
            "Free, offline, no ads, no in-app purchases, no tracking. Wear OS 3+.",
        ],
        features=[
            ("Lantern herding", "Tap to walk the lantern; the swarm follows. The crown steers too."),
            ("Flare", "A burst of light that holds the swarm together. A full jar earns one back."),
            ("Real dangers", "Webs, frogs, bats, wind and rain."),
            ("24 nights, four scenes", "Each brings in a new rule on its first night."),
            ("Boss nights", "Bullfrog, Owl, Spider Queen and the King of the Pond."),
            ("Three stars per night", "Based on how many fireflies you bring home."),
            ("Standalone", "Offline. Sound and music with a mute button on the title screen."),
        ],
        screenshot_alts=[
            "Firefly title card: Summer Meadow, night 6 of 24, The Bullfrog, with a moon over the field",
            "A lantern glowing yellow in a meadow with three empty jars, a spider web and fireflies trailing it",
            "Night pond: a frog sits on a lily pad under a full moon while the lantern leads the swarm",
            "A dark forest night with two glowing swarms of fireflies, a jar at the bottom and 18 spare",
        ],
        hero_shot=3,
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
    Game(
        slug="bubble-level",
        name="Bubble Level",
        package="com.zenirl.level",
        kind="app",
        category="Tools",
        schema_category="UtilitiesApplication",
        short_desc="A precision bubble level for Wear OS. Lay your watch flat — the bubble centres and turns green when level. Tap to zero on any surface. Offline.",
        tagline="A spirit level on your wrist. Lay the watch flat — green means level.",
        tags=["Tools", "Utility", "Sensor"],
        accent="#34D399", accent_hover="#5BE0AD", accent_text="#1A1A1A",
        privacy_url="https://zenirl.github.io/policies/level.html",
        paragraphs=[
            "Your watch already has an accelerometer; this turns it into a precise two-axis spirit level. Lay it flat on a shelf, a frame, a table — the bubble drifts to show the tilt and snaps green the instant you’re level, with a gentle haptic tick to confirm.",
            "A live pitch/roll readout shows the exact angle. Tap to zero against any surface (tap again to reset to true level). No ads, no accounts, and it works entirely offline — the accelerometer is read on-device and nothing ever leaves your watch.",
        ],
        features=[
            ("Two-axis bubble level", "Pitch and roll at a glance on the round screen."),
            ("Green when level", "A clear colour flip plus a haptic tick."),
            ("Tap to zero", "Calibrate against any surface; tap again to reset."),
            ("Live angle readout", "Exact pitch and roll in degrees."),
            ("Private and offline", "Accelerometer read on-device; no data leaves the watch."),
        ],
        screenshot_alts=[
            "Bubble Level — level and green, the bubble centred",
            "A tilted reading with pitch and roll in degrees",
            "How to use — lay the watch flat on a surface",
        ],
    ),
]


def clip_exists(g: Game) -> bool:
    base = "apps" if g.kind == "app" else "games"
    return os.path.exists(os.path.join(ROOT, "assets", base, g.slug, "clip.mp4"))


def render_game(g: Game) -> str:
    base = "apps" if g.kind == "app" else "games"          # URL + asset namespace
    nav_href, nav_label = ("/#apps", "Apps") if g.kind == "app" else ("/#available", "Games")
    all_label = "All apps" if g.kind == "app" else "All games"
    play_url = f"https://play.google.com/store/apps/details?id={g.package}" if g.package else None
    canonical = f"{BASE_URL}/{base}/{g.slug}/"
    icon_url = f"{BASE_URL}/assets/{base}/{g.slug}/icon.png"
    feature_url = f"{BASE_URL}/assets/{base}/{g.slug}/feature.png"
    full_name = g.title_name or g.name
    title = f"{full_name} — {g.category} for Wear OS · ZenIRL"
    asset = f"/assets/{base}/{g.slug}"
    n_shots = len(g.screenshot_alts)
    hero_i = min(max(g.hero_shot, 1), n_shots)
    hero_alt = html.escape(g.screenshot_alts[hero_i - 1], quote=True)
    accent_text = readable_text(g.accent, g.accent_text)
    accent_hover_text = readable_text(g.accent_hover, accent_text)
    if accent_hover_text != accent_text:      # hover colour must stay legible too
        accent_text = accent_hover_text
    has_clip = clip_exists(g)

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
      "name": "{full_name}",
      "description": "{g.short_desc}",
      "operatingSystem": "Wear OS 3+",
      "applicationCategory": "{g.schema_category}",
      "image": "{icon_url}",
      "url": "{canonical}",
      "author": {{
        "@type": "Organization",
        "name": "ZenIRL",
        "url": "{BASE_URL}/",
        "sameAs": ["https://x.com/zenIRL_"]
      }}{schema_offers}
    }}''').strip()

    cta_block = (
        f'<a class="btn" href="{play_url}" rel="noopener" target="_blank">Get on Google Play<span class="visually-hidden"> (opens in a new tab)</span></a>'
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
        f'<figure class="bezel"><img loading="lazy" decoding="async" src="{asset}/screenshot-{i+1}.webp" alt="{html.escape(alt, quote=True)}" width="480" height="480"><span class="sheen"></span></figure>'
        for i, alt in enumerate(g.screenshot_alts)
    )

    clip_block = ""
    clip_script = ""
    if has_clip:
        clip_block = f'''
    <section class="container clip" aria-labelledby="clip-h">
      <h2 class="section-heading" id="clip-h">In motion</h2>
      <figure class="bezel">
        <video muted loop playsinline preload="none" width="480" height="480" poster="{asset}/screenshot-1.webp" aria-label="{g.name} gameplay clip, no sound" data-clip>
          <source src="{asset}/clip.mp4" type="video/mp4">
        </video><span class="sheen"></span>
      </figure>
      <p>Silent gameplay clip. Plays while on screen.</p>
    </section>'''
        clip_script = """
  <script>
  (function () {
    var v = document.querySelector('video[data-clip]');
    if (!v) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { v.controls = true; return; }
    if (!('IntersectionObserver' in window)) { v.controls = true; return; }
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { v.preload = 'auto'; var p = v.play(); if (p && p.catch) p.catch(function (err) { if (err && err.name === 'NotAllowedError') v.controls = true; }); }
        else v.pause();
      });
    }, { threshold: 0.35 }).observe(v);
  })();
  </script>"""

    sticky = ""
    sticky_script = ""
    body_cls = ""
    if play_url:
        body_cls = ' class="has-sticky"'
        sticky = f'''
  <div class="sticky-cta" id="sticky-cta">
    <span class="sticky-name">{g.name}</span>
    <a class="btn" href="{play_url}" rel="noopener" target="_blank">Get on Google Play<span class="visually-hidden"> (opens in a new tab)</span></a>
  </div>'''
        sticky_script = """
  <script>
  (function () {
    var bar = document.getElementById('sticky-cta'), hero = document.querySelector('.game-hero .cta-row');
    if (!bar || !hero || !('IntersectionObserver' in window)) return;
    new IntersectionObserver(function (es) {
      bar.classList.toggle('is-visible', !es[0].isIntersecting && es[0].boundingClientRect.top < 0);
    }).observe(hero);
  })();
  </script>"""

    gallery_hint = '<p class="gallery-hint" aria-hidden="true">Swipe for more</p>' if n_shots > 1 else ""

    return textwrap.dedent(f'''\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{g.short_desc}">
  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#1A1A1A">
  <link rel="stylesheet" href="/assets/css/styles.css">
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
  <link rel="preload" as="image" href="{asset}/screenshot-{hero_i}.webp" type="image/webp" fetchpriority="high">

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
      --game-accent-text: {accent_text};
    }}
  </style>
</head>
<body{body_cls}>
  <a href="#main" class="skip-link">Skip to content</a>

  <header class="site-header">
    <div class="container">
      <div class="brand"><a href="/">ZenIRL</a></div>
      <nav aria-label="Primary">
        <a href="{nav_href}">{nav_label}</a>
        <a href="/#coming-soon">Coming soon</a>
        <a href="/about/">About</a>
        <a href="https://x.com/zenIRL_" rel="noopener" target="_blank" aria-label="ZenIRL on X (opens in a new tab)">@zenIRL_</a>
      </nav>
    </div>
  </header>

  <main id="main">
    <div class="game-hero-wrap">
      <section class="container game-hero">
        <div>
          <div class="title-row">
            <img class="game-icon" src="{asset}/icon.png" alt="{g.name} app icon" width="84" height="84">
            <h1>{g.name}</h1>
          </div>
          <p class="tagline">{g.tagline}</p>
          <div class="tag-row">
            {tag_pills}
          </div>
          <div class="cta-row">
          {cta_block}
          </div>
        </div>
        <div class="hero-bezel">
          <figure class="bezel"><img src="{asset}/screenshot-{hero_i}.webp" alt="{hero_alt}" width="480" height="480" fetchpriority="high" decoding="async"><span class="sheen"></span></figure>
        </div>
      </section>
    </div>

    <section class="container gallery" aria-labelledby="shots-h">
      <h2 class="section-heading" id="shots-h">Screenshots</h2>
      <div class="gallery-row" role="region" aria-label="{g.name} screenshots, scrollable" tabindex="0">
          {screenshots}
      </div>
      {gallery_hint}
    </section>
{clip_block}
    <article class="container prose">
      {paragraphs}

      <h2>Features</h2>
      <ul>
        {feature_items}
      </ul>
    </article>
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>&copy; 2026 ZenIRL, a <a href="https://helpivy.com/" rel="noopener">Helpivy</a> label · <a href="mailto:help@helpivy.com">help@helpivy.com</a></p>
      <p><a href="/">{all_label}</a> · <a href="/about/">About</a></p>
      <p>Follow on X: <a href="https://x.com/zenIRL_" rel="noopener" target="_blank" aria-label="ZenIRL on X (opens in a new tab)">@zenIRL_</a></p>
    </div>
  </footer>
{sticky}{sticky_script}{clip_script}
</body>
</html>
''')


def write_sitemap() -> None:
    rows = [f"""  <url>
    <loc>{BASE_URL}/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>""", f"  <url><loc>{BASE_URL}/about/</loc><changefreq>monthly</changefreq><priority>0.4</priority></url>"]
    for g in GAMES + APPS:
        base = "apps" if g.kind == "app" else "games"
        prio = "0.8" if g.package else "0.5"
        rows.append(f"  <url><loc>{BASE_URL}/{base}/{g.slug}/</loc><changefreq>monthly</changefreq><priority>{prio}</priority></url>")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n"
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"wrote sitemap.xml ({len(GAMES) + len(APPS) + 2} urls)")


def main() -> None:
    for g in GAMES + APPS:
        base = "apps" if g.kind == "app" else "games"
        out_dir = os.path.join(ROOT, base, g.slug)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(render_game(g))
        print(f"wrote {out_path}")
    write_sitemap()


if __name__ == "__main__":
    main()
