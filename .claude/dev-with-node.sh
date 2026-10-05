#!/bin/zsh
export PATH="$HOME/.nvm/versions/node/v22.23.2/bin:$PATH"
exec npm run dev -- --host --port 4331
