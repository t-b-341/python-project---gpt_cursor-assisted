# Telemetry & Visualization Improvements for SQL Learning

## 🎯 Goals
1. **Better SQL Learning**: More opportunities for JOINs, CTEs, window functions, aggregations
2. **Better Visualizations**: More interesting charts showcasing SQL techniques
3. **Normalized Structure**: Proper relationships and foreign keys
4. **Performance**: Strategic indexes and query optimization

---

## 📊 Database Structure Improvements

### 1. **Add Junction Tables (Many-to-Many Relationships)**

#### **player_weapon_usage** (Junction Table)
```sql
CREATE TABLE player_weapon_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    weapon_mode TEXT NOT NULL,
    start_time REAL NOT NULL,
    end_time REAL,
    shots_fired INTEGER DEFAULT 0,
    kills INTEGER DEFAULT 0,
    damage_dealt INTEGER DEFAULT 0,
    FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
);
```
**SQL Learning Opportunities:**
- Self-JOINs to find weapon transitions
- Window functions for time calculations
- Aggregations with GROUP BY

#### **enemy_weapon_associations** (Junction Table)
```sql
CREATE TABLE enemy_weapon_associations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enemy_type TEXT NOT NULL,
    weapon_type TEXT NOT NULL,
    usage_count INTEGER DEFAULT 0,
    UNIQUE(enemy_type, weapon_type)
);
```
**SQL Learning Opportunities:**
- Many-to-many relationships
- JOINs across multiple tables

### 2. **Add Zone/Area Tracking**

#### **zones** (Reference Table)
```sql
CREATE TABLE zones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_name TEXT NOT NULL UNIQUE,
    zone_type TEXT NOT NULL,  -- "health_recovery", "overshield", "combat", "safe"
    x_min INTEGER NOT NULL,
    x_max INTEGER NOT NULL,
    y_min INTEGER NOT NULL,
    y_max INTEGER NOT NULL
);
```

#### **player_zone_visits**
```sql
CREATE TABLE player_zone_visits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    zone_id INTEGER NOT NULL,
    entry_time REAL NOT NULL,
    exit_time REAL,
    time_spent REAL,
    FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE,
    FOREIGN KEY(zone_id) REFERENCES zones(id) ON DELETE CASCADE
);
```
**SQL Learning Opportunities:**
- JOINs with reference tables
- Time calculations
- Subqueries for zone statistics

### 3. **Add Player Action Events**

#### **player_actions**
```sql
CREATE TABLE player_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    t REAL NOT NULL,
    action_type TEXT NOT NULL,  -- "jump", "boost", "slow", "dash", "weapon_switch"
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    duration REAL,  -- for boost/slow
    success INTEGER DEFAULT 1,  -- 0/1 for failed actions
    FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
);
```
**SQL Learning Opportunities:**
- Filtering with WHERE
- Aggregations by action type
- Time-series analysis

### 4. **Add Combat Sessions**

#### **combat_sessions**
```sql
CREATE TABLE combat_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    wave_number INTEGER,
    start_time REAL NOT NULL,
    end_time REAL,
    enemies_engaged INTEGER DEFAULT 0,
    damage_dealt INTEGER DEFAULT 0,
    damage_taken INTEGER DEFAULT 0,
    kills INTEGER DEFAULT 0,
    shots_fired INTEGER DEFAULT 0,
    shots_hit INTEGER DEFAULT 0,
    FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
);
```
**SQL Learning Opportunities:**
- Window functions for session analysis
- Correlated subqueries
- Performance metrics

### 5. **Add Enemy Relationships**

#### **enemy_spawn_groups**
```sql
CREATE TABLE enemy_spawn_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    wave_number INTEGER NOT NULL,
    spawn_time REAL NOT NULL,
    group_size INTEGER NOT NULL,
    FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
);
```

#### **enemy_spawns** (Enhanced)
Add `spawn_group_id` foreign key to link enemies spawned together.

**SQL Learning Opportunities:**
- GROUP BY with aggregations
- JOINs to find spawn patterns
- Window functions for group analysis

### 6. **Add Views for Common Queries**

#### **player_performance_summary** (View)
```sql
CREATE VIEW player_performance_summary AS
SELECT 
    r.id AS run_id,
    r.difficulty,
    r.max_level,
    r.final_score,
    r.seconds_survived,
    r.enemies_killed,
    r.damage_dealt,
    r.damage_taken,
    CASE 
        WHEN r.shots_fired > 0 
        THEN CAST(r.hits AS REAL) / r.shots_fired * 100.0 
        ELSE 0.0 
    END AS accuracy_pct,
    CASE 
        WHEN r.seconds_survived > 0 
        THEN CAST(r.enemies_killed AS REAL) / r.seconds_survived 
        ELSE 0.0 
    END AS kills_per_second
FROM runs r;
```
**SQL Learning Opportunities:**
- CASE statements
- Calculated columns
- View usage

#### **wave_performance** (View)
```sql
CREATE VIEW wave_performance AS
SELECT 
    w.run_id,
    w.wave_number,
    w.enemies_spawned,
    w.hp_scale,
    w.speed_scale,
    COUNT(DISTINCT e.id) AS enemies_killed,
    SUM(eh.damage) AS damage_dealt,
    MIN(CASE WHEN w.event_type = 'start' THEN w.t END) AS start_time,
    MIN(CASE WHEN w.event_type = 'end' THEN w.t END) AS end_time
FROM waves w
LEFT JOIN enemy_spawns e ON e.run_id = w.run_id
LEFT JOIN enemy_hits eh ON eh.run_id = w.run_id
GROUP BY w.run_id, w.wave_number;
```
**SQL Learning Opportunities:**
- Complex JOINs
- Aggregations with GROUP BY
- Conditional aggregations

### 7. **Add Time-Based Partitioning**

#### **time_windows** (Helper Table)
```sql
CREATE TABLE time_windows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    window_start REAL NOT NULL,
    window_end REAL NOT NULL,
    window_duration REAL NOT NULL,
    window_type TEXT NOT NULL,  -- "combat", "exploration", "pickup_collection"
    FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
);
```
**SQL Learning Opportunities:**
- Time-based JOINs
- Window functions
- Temporal queries

---

## 📈 New Visualization Functions

### 1. **Complex JOIN Examples**

#### **draw_weapon_effectiveness_comparison**
```python
def draw_weapon_effectiveness_comparison(ax, conn, run_id):
    """Compare weapons using JOINs across multiple tables."""
    df = read_df(conn, """
        SELECT 
            w.weapon_mode,
            COUNT(DISTINCT s.id) AS shots_fired,
            COUNT(DISTINCT eh.id) AS hits,
            SUM(eh.damage) AS total_damage,
            COUNT(DISTINCT CASE WHEN eh.killed = 1 THEN eh.id END) AS kills
        FROM weapon_switches w
        LEFT JOIN shots s ON s.run_id = w.run_id 
            AND s.t BETWEEN w.t AND COALESCE(
                (SELECT MIN(t) FROM weapon_switches w2 
                 WHERE w2.run_id = w.run_id AND w2.t > w.t), 
                (SELECT seconds_survived FROM runs WHERE id = w.run_id)
            )
        LEFT JOIN enemy_hits eh ON eh.run_id = w.run_id 
            AND eh.t BETWEEN w.t AND COALESCE(
                (SELECT MIN(t) FROM weapon_switches w2 
                 WHERE w2.run_id = w.run_id AND w2.t > w.t),
                (SELECT seconds_survived FROM runs WHERE id = w.run_id)
            )
        WHERE w.run_id = ?
        GROUP BY w.weapon_mode
        ORDER BY total_damage DESC;
    """, (run_id,))
    # ... visualization code
```
**SQL Techniques:**
- Multiple LEFT JOINs
- Correlated subqueries
- Conditional aggregations

### 2. **CTE Examples**

#### **draw_player_action_patterns**
```python
def draw_player_action_patterns(ax, conn, run_id):
    """Use CTEs to analyze action sequences."""
    df = read_df(conn, """
        WITH action_sequences AS (
            SELECT 
                action_type,
                t,
                LAG(action_type) OVER (ORDER BY t) AS prev_action,
                LEAD(action_type) OVER (ORDER BY t) AS next_action,
                t - LAG(t) OVER (ORDER BY t) AS time_since_prev
            FROM player_actions
            WHERE run_id = ?
        ),
        action_transitions AS (
            SELECT 
                prev_action || ' -> ' || action_type AS transition,
                COUNT(*) AS frequency,
                AVG(time_since_prev) AS avg_time
            FROM action_sequences
            WHERE prev_action IS NOT NULL
            GROUP BY transition
        )
        SELECT * FROM action_transitions
        ORDER BY frequency DESC
        LIMIT 10;
    """, (run_id,))
    # ... visualization code
```
**SQL Techniques:**
- Common Table Expressions (CTEs)
- Window functions (LAG, LEAD)
- String concatenation

### 3. **Window Function Examples**

#### **draw_running_statistics**
```python
def draw_running_statistics(ax, conn, run_id):
    """Show running totals and averages using window functions."""
    df = read_df(conn, """
        SELECT 
            t,
            score,
            SUM(score_change) OVER (ORDER BY t) AS running_score,
            AVG(score_change) OVER (
                ORDER BY t 
                ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
            ) AS moving_avg_10,
            COUNT(*) OVER (ORDER BY t) AS event_count
        FROM score_events
        WHERE run_id = ?
        ORDER BY t;
    """, (run_id,))
    # ... visualization code
```
**SQL Techniques:**
- Window functions with frames
- Running totals
- Moving averages

### 4. **Subquery Examples**

#### **draw_zone_effectiveness**
```python
def draw_zone_effectiveness(ax, conn, run_id):
    """Compare zones using correlated subqueries."""
    df = read_df(conn, """
        SELECT 
            z.zone_name,
            z.zone_type,
            COUNT(pzv.id) AS visit_count,
            AVG(pzv.time_spent) AS avg_time_spent,
            (SELECT COUNT(*) 
             FROM player_actions pa 
             WHERE pa.run_id = ? 
             AND pa.action_type = 'boost'
             AND pa.x BETWEEN z.x_min AND z.x_max
             AND pa.y BETWEEN z.y_min AND z.y_max
            ) AS boost_actions_in_zone
        FROM zones z
        LEFT JOIN player_zone_visits pzv ON pzv.zone_id = z.id AND pzv.run_id = ?
        GROUP BY z.id, z.zone_name, z.zone_type
        ORDER BY visit_count DESC;
    """, (run_id, run_id))
    # ... visualization code
```
**SQL Techniques:**
- Correlated subqueries
- Spatial queries
- Multiple aggregations

### 5. **Pivot/Cross-Tab Examples**

#### **draw_weapon_by_wave_matrix**
```python
def draw_weapon_by_wave_matrix(ax, conn, run_id):
    """Create a heatmap showing weapon usage by wave."""
    df = read_df(conn, """
        SELECT 
            w.wave_number,
            ws.weapon_mode,
            COUNT(*) AS usage_count
        FROM waves w
        JOIN weapon_switches ws ON ws.run_id = w.run_id
        WHERE w.run_id = ? 
        AND w.event_type = 'start'
        AND ws.t BETWEEN w.t AND COALESCE(
            (SELECT MIN(t) FROM waves w2 
             WHERE w2.run_id = w.run_id 
             AND w2.wave_number = w.wave_number + 1
             AND w2.event_type = 'start'),
            (SELECT seconds_survived FROM runs WHERE id = w.run_id)
        )
        GROUP BY w.wave_number, ws.weapon_mode;
    """, (run_id,))
    # Pivot and create heatmap
    # ... visualization code
```
**SQL Techniques:**
- Complex JOINs with time ranges
- Pivot operations (in Python)
- Heatmap visualization

### 6. **Recursive CTE Examples**

#### **draw_enemy_spawn_chains**
```python
def draw_enemy_spawn_chains(ax, conn, run_id):
    """Track enemy spawn sequences using recursive CTEs."""
    df = read_df(conn, """
        WITH RECURSIVE spawn_chain AS (
            -- Base case: first spawn in each group
            SELECT 
                esg.id,
                esg.spawn_time,
                esg.group_size,
                1 AS chain_level
            FROM enemy_spawn_groups esg
            WHERE esg.run_id = ?
            AND esg.spawn_time = (
                SELECT MIN(spawn_time) 
                FROM enemy_spawn_groups 
                WHERE run_id = esg.run_id
            )
            
            UNION ALL
            
            -- Recursive case: next spawn in sequence
            SELECT 
                esg.id,
                esg.spawn_time,
                esg.group_size,
                sc.chain_level + 1
            FROM enemy_spawn_groups esg
            JOIN spawn_chain sc ON sc.run_id = esg.run_id
            WHERE esg.spawn_time > sc.spawn_time
            AND esg.spawn_time - sc.spawn_time < 5.0  -- Within 5 seconds
        )
        SELECT * FROM spawn_chain;
    """, (run_id,))
    # ... visualization code
```
**SQL Techniques:**
- Recursive CTEs
- Hierarchical queries
- Time-based sequences

---

## 🔧 Implementation Priority

### Phase 1: High Impact, Easy Implementation
1. ✅ Add `player_actions` table
2. ✅ Add `zones` and `player_zone_visits` tables
3. ✅ Create `player_performance_summary` view
4. ✅ Add 3-4 new visualization functions using JOINs

### Phase 2: Medium Complexity
1. ✅ Add `combat_sessions` table
2. ✅ Add `player_weapon_usage` junction table
3. ✅ Create `wave_performance` view
4. ✅ Add CTE-based visualizations

### Phase 3: Advanced Features
1. ✅ Add recursive CTE examples
2. ✅ Add time window partitioning
3. ✅ Add complex pivot visualizations

---

## 📚 SQL Learning Path

### Beginner Level
- Simple SELECT with WHERE
- Basic aggregations (COUNT, SUM, AVG)
- Simple JOINs

### Intermediate Level
- Multiple JOINs
- GROUP BY with aggregations
- Subqueries
- Window functions (ROW_NUMBER, RANK)

### Advanced Level
- CTEs (WITH clauses)
- Recursive CTEs
- Complex window functions (LAG, LEAD, frames)
- Correlated subqueries
- Pivot operations

---

## 🎨 Visualization Ideas

1. **Action Heatmap**: Where actions occur on the map
2. **Weapon Transition Graph**: Network diagram of weapon switches
3. **Zone Efficiency**: Time spent vs. benefits gained per zone
4. **Combat Session Analysis**: Performance per combat session
5. **Spawn Pattern Analysis**: Enemy spawn timing and grouping
6. **Running Statistics**: Moving averages and trends
7. **Correlation Matrix**: Relationships between game metrics
8. **Timeline Visualization**: Multiple metrics overlaid on time axis

---

## 💡 Additional Recommendations

1. **Add Sample Queries File**: Create `sample_queries.sql` with commented examples
2. **Add Query Performance Tracking**: Log slow queries for optimization
3. **Add Data Validation**: Constraints and triggers for data integrity
4. **Add Export Functions**: Export data to CSV/JSON for external analysis
5. **Add Query Builder Helper**: Python functions that generate SQL safely
