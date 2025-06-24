import sqlite3

conn = sqlite3.connect("world_series.db")
cursor = conn.cursor()

print("All records (limit 10):")
cursor.execute("SELECT * FROM world_series LIMIT 10")
for row in cursor.fetchall():
    print(row)

print("Total World Series wins by team:")
cursor.execute("""
    SELECT winner, COUNT(*) AS wins
    FROM world_series
    GROUP BY winner
    ORDER BY wins DESC
""")

for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} wins")


print("\nYears the Chicago Cubs won:")
cursor.execute("""
    SELECT year, winner_games, loser
    FROM world_series
    WHERE winner = 'Chicago Cubs'
""")
for row in cursor.fetchall():
    print(row)

conn.close()
