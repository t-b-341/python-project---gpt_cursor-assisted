-- Shots per weapon. Weapon at shot time = latest weapon_switches with t <= shot.t.
-- Per-weapon hit counts are not stored; run-level accuracy is in runs (shots_fired, hits).

SELECT COALESCE(
  (SELECT weapon_mode FROM weapon_switches w
   WHERE w.run_id = s.run_id AND w.t <= s.t
   ORDER BY w.t DESC LIMIT 1),
  'unknown'
) AS weapon_mode,
COUNT(*) AS shots
FROM shots s
GROUP BY 1
ORDER BY shots DESC;
