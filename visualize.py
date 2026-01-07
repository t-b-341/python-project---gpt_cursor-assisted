import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "game_telemetry.db"

query = """
SELECT x, y
FROM player_positions
WHERE run_id = (
    SELECT MAX(run_id) FROM player_positions
);
"""

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(query, conn)

plt.figure()
plt.plot(df["x"], df["y"])
plt.title("Player movement path (latest run)")
plt.xlabel("x")
plt.ylabel("y")
plt.axis("equal")
plt.tight_layout()
plt.show()
