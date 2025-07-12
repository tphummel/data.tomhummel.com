#!/bin/bash
set -euo pipefail

echo "➡️ Using pre-installed asdf"
. /opt/buildhome/.asdf/asdf.sh
asdf version

echo "➡️ Installing hugo plugin if needed"
asdf plugin add hugo https://github.com/asdf-community/asdf-hugo.git || true

echo "➡️ Installing hugo from .tool-versions"
asdf install
asdf global hugo "$(awk '/^hugo / {print $2}' .tool-versions)"

echo "✅ Hugo version: $(hugo version)"

export ASDF_DIR=/opt/buildhome/.asdf
export PATH="$ASDF_DIR/bin:$ASDF_DIR/shims:$PATH"
