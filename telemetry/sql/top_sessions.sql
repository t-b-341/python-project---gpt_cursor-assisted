-- Top sessions by score and by survival time.
-- Uses player_performance_summary (view over runs). Adjust LIMIT as needed.

-- Top 10 runs by final score
SELECT '--- Top 10 by score ---' AS section;
SELECT run_id, difficulty, max_level, final_score, seconds_survived,
       enemies_killed, accuracy_pct, dps
FROM player_performance_summary
WHERE final_score IS NOT NULL
ORDER BY final_score DESC
LIMIT 10;

-- Top 10 runs by survival time (seconds)
SELECT '--- Top 10 by survival time ---' AS section;
SELECT run_id, difficulty, max_level, final_score, seconds_survived,
       enemies_killed, accuracy_pct, dps
FROM player_performance_summary
WHERE seconds_survived IS NOT NULL
ORDER BY seconds_survived DESC
LIMIT 10;
