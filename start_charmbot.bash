#!/bin/bash

# Znajdź i zabij proces girlbot.py
pid=$(pgrep -f "python3.*charmbot.py")
if [ -n "$pid" ]; then
    echo "Zabijam charmbot.py o PID: $pid"
    kill "$pid"
    sleep 1
else
    echo "CharmBot nie działa — nic do zabicia"
fi

# Uruchom bota w tle z nohup
echo "Uruchamiam charmbot.py"
nohup python3 /home/frog/charmbot/charmbot.py > /home/frog/charmbot/charmbot.log 2>&1 &

echo "CharmBot uruchomiony w tle. PID: $!"

