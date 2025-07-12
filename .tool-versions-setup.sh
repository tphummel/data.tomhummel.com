#!/bin/bash
set -euo pipefail

echo "➡️ Installing asdf"
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.13.1
. ~/.asdf/asdf.sh

echo "➡️ Installing asdf-hugo plugin"
asdf plugin add hugo https://github.com/asdf-community/asdf-hugo.git || true

echo "➡️ Installing Hugo via asdf"
asdf install
asdf global hugo "$(awk '/^hugo / {print $2}' .tool-versions)"

echo "✅ Hugo version: $(hugo version)"
