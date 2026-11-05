#!/bin/sh
# Generate the web-optimised derivatives the pages use. PNG originals stay as the source of truth.
#   screenshot-N.png -> screenshot-N.webp (480x480, q82)
#   icon.png         -> icon-176.webp     (2x of the 88px card badge)
# Needs ImageMagick with WebP support:  sh make_webp.sh
cd "$(dirname "$0")/assets" || exit 1
for d in games/* apps/*; do
  for f in "$d"/screenshot-*.png; do [ -e "$f" ] && magick "$f" -quality 82 "${f%.png}.webp"; done
  [ -e "$d/icon.png" ] && magick "$d/icon.png" -resize 176x176 -quality 85 "$d/icon-176.webp"
done
