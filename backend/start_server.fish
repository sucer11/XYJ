#!/opt/homebrew/bin/fish
micromamba activate seintro
uvicorn main:app --host '127.0.0.1' --port 13271 --reload

# start db server
# pg_ctl -D backend/database/ -l backend/db_log start
