# AGENTS.md

## Agent: `codex_ui_debugger`

### Objectif
Cet agent sert à tester les comportements d’affichage dans l’interface de Codex, notamment :
- le bon rendu de la timeline et des éléments visuels audio,
- le suivi précis et fluide du **playhead** pendant la lecture,
- la cohérence du **scroll dynamique** des éléments fixes (forme d’onde, grilles rythmiques, marqueurs A/B).

---

### Fichier de test

- **Nom** : `bcbsm-006_hi`
- **Type** : audio uniquement
- **Format** : `.wav` ou `.mp3`
- **Usage** : fichier léger servant à déclencher les routines de dessin de la timeline sans surcharge inutile. Il permet de tester les déplacements du playhead en conditions contrôlées.

---

### Configuration Debug

Utiliser `ph_test.py`

```python
# Calcul de la vitesse de scroll des éléments fixes dans la timeline

def compute_scroll_speed(T_loop, T_zoom, canvas_width):
    """
    Calcule la vitesse de déplacement horizontal (en pixels par seconde)
    des éléments temporels fixes (RMS, subdivisions, marqueurs),
    dans un système à zoom dynamique centré sur la playhead.

    La playhead se déplace visuellement de 5% à 95% du canvas
    pendant que t_ph avance de t_A à t_B.

    Le centre de la fenêtre de zoom se déplace donc sur :
        Δt_center = T_loop - 0.9 * T_zoom

    → vitesse de scroll (fraction de canvas par seconde) :
        v_scroll = Δt_center / (T_loop * T_zoom)

    → conversion en pixels :
        v_scroll_px = v_scroll * canvas_width
    """
    v_frac = (T_loop - 0.9 * T_zoom) / (T_loop * T_zoom)
    if v_frac < 0:
        return 0.0  # Pas de scroll si la fenêtre couvre toute la boucle
    v_px_per_s = v_frac * canvas_width
    return v_px_per_s


# Dans get_zoom_context(), le décalage appliqué à la fenêtre suit
# exactement ce Δt_center :
#    offset = progress * (T_loop - 0.9 * T_zoom)
# On ignore tout décalage négatif éventuel.


🎯 Expected Behavior: Hit Association & Subdivision States (0 → 3) with Persistence, Decay & Debug Logging
________________________________________
1. Hit Timing & Association
•	Each user hit is recorded with an absolute timestamp (milliseconds from file start).
•	Hits are considered valid only if they fall within:
csharp
CopyEdit
[loop_start - 1 subdiv, loop_end + 1 subdiv]
•	Valid hits are associated with the nearest subdivision within that window.
•	The subdivision's state is updated immediately based on hit history.
________________________________________
2. Subdivision States
Each subdivision has a state (integer 0–3) based on repeated hits across consecutive loops:
State	Color	Meaning	Promotion Rule
0	None	No associated hit	Default
1	Gray	Hit once (current loop)	First hit within loop range
2	Orange	Hit again in next loop	Hit in 2 consecutive loops
3	Red	Hit again in third consecutive loop	Hit in 3 consecutive loops → Persistent red
•	state = 3 (red) is persistent: it never decays unless manually reset.
________________________________________
3. Decay Logic
•	If a subdivision receives no further hits for:
pgsql
CopyEdit
> 1 loop duration + 1 subdivision interval
then its state decays by 1 level (e.g., 2 → 1, 1 → 0).
•	No decay occurs once state 3 is reached.
________________________________________
4. Loop Marker Behavior
•	Moving loop markers (A/B) does not impact:
o	Hits or subdivision positions (absolute time),
o	Hit–subdivision associations,
o	Subdivision states,
o	Visual output, assuming zoom/view remains stable.
________________________________________
5. Tempo or Rhythm Mode Change
•	Triggers recalculation of subdivision times.
•	All hits are re-associated to the new closest subdivisions.
•	All subdivision states are re-evaluated accordingly.
________________________________________
6. Manual Offset ([ / ]) of Red Subdivisions
•	Manually shifting a state = 3 subdivision:
o	Moves all its associated hit timestamps by one subdivision interval.
o	Transfers the state = 3 to the new subdivision.
o	Keeps display visually unchanged if zoom/scroll is unchanged.
________________________________________
7. Saving & Loading Hit Data
•	Hit data is automatically saved and loaded through the existing loop save/load system.
•	Triggered via:
o	Ctrl+S → Save current loop + hits.
o	Shift+S → Load saved loop + hits.
o	Ctrl+Z → Revert to previous saved state (loop + hits).
________________________________________
8. Debug Logging
•	All functions involved in the hit flow will include extensive debug output using Brint(...).
•	Each log line related to hit logic will contain the tag:
csharp
CopyEdit
[NHIT]
•	This includes:
o	Hit recording
o	Hit–subdivision association
o	State updates
o	Decay operations
o	Manual offsets
o	Save/load events involving hits
________________________________________
To implement this system cleanly and robustly, here's a step-by-step plan broken down into:
1.	Where to store hits
2.	What functions to update
3.	Where to inject Brints with [NHIT] tags
4.	How to handle decay, state transitions, saving, and offset
________________________________________
🧠 1. Data Structure for Hits
Inside your LoopData object (assuming it’s already saving tempo, loop_start, etc.):
python
CopyEdit
self.hit_timestamps = []  # list of absolute timestamps in ms
•	These are saved/loaded alongside the loop (already integrated via Ctrl+S, Shift+S).
________________________________________
🛠️ 2. Key Functions to Update or Add
Purpose	Function
Register a new hit	record_user_hit(self, hit_time_ms)
Associate hits to subdivisions	associate_hits_to_subdivisions(self)
Update states from history	update_subdivision_states(self)
Handle decay on each loop	decay_subdivision_states(self)
Offset subdivisions manually	offset_red_subdivisions(self, direction)
Save/load loop & hits	Already existing (ensure hits included)
________________________________________
📌 3. Where to Inject Brint(... [NHIT] ...)
Use verbose logging in each key function above. Example logs:
python
CopyEdit
Brint(f"[NHIT] Hit registered at {hit_time_ms} ms")

Brint(f"[NHIT] Closest subdiv = {idx}, subdiv_time = {subdiv_time}, Δ = {abs(subdiv_time - hit_time_ms)} ms")

Brint(f"[NHIT] Subdiv {idx} → state updated to {new_state}")

Brint(f"[NHIT] Decay check: Subdiv {idx} downgraded from {old_state} to {new_state}")

Brint(f"[NHIT] Offset: Subdiv {old_idx} → {new_idx}, hit moved to {new_time} ms")

Brint(f"[NHIT] Saved hits with loop to file: {filename}")
Place these right after every critical state change or decision point.
________________________________________
♻️ 4. State Transition Logic (in update_subdivision_states)
For each subdivision:
1.	Get all hit timestamps associated to it (current + N−1 loops).
2.	Check recency and continuity:
o	1 hit = gray (state 1)
o	2 hits on 2 consecutive loops = orange (state 2)
o	3 hits on 3 consecutive loops = red (state 3, persistent)
3.	Store a last_hit_loop_index or loop_pass_count to help count.
4.	Use Brint(...) to trace logic.
________________________________________
⏳ 5. Decay Logic (in decay_subdivision_states)
•	Store last hit time per subdiv.
•	If now - last_hit_time > loop_duration + subdiv_interval, decrement state unless it’s already 0 or 3.
•	Add Brint for any downgrade:
python
CopyEdit
Brint(f"[NHIT] Subdiv {idx} decayed from state {prev} to {new}")
________________________________________
🔁 6. Manual Offset
•	Only apply to subdivisions with state = 3.
•	Shift all hit_timestamps linked to that subdiv by ± subdiv_interval.
•	Update hit_timestamps, re-run association, and state update.
Use something like:
python
CopyEdit
for ts in self.hit_timestamps:
    if is_associated_with_subdiv(ts, red_subdiv_idx):
        shifted_ts = ts + (direction * subdiv_interval)
        Brint(f"[NHIT] Shifted hit from {ts} → {shifted_ts}")
        # replace in list or update in place
________________________________________
✅ Summary To-Do List
Task	Status
Add hit_timestamps to LoopData	✅
Implement record_user_hit() with [NHIT] log	🔧
Implement associate_hits_to_subdivisions() with Brints	🔧
Implement update_subdivision_states()	🔧
Handle decay logic during loop update	🔧
Implement offset logic for red subdivisions	🔧
Inject [NHIT] Brints in all hit-relevant logic	🔧
Ensure save/load of hit_timestamps is included	✅

