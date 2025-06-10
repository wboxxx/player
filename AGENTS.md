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
----------------



🎯 Expected Behavior: Hit Association & Subdivision States (0 → 3) with Persistence, Decay & Debug Logging
________________________________________
1. Hit Timing & Association
•	Each user hit is recorded with an absolute timestamp (milliseconds from file start).
•	Hits are considered valid only if they fall within:

[loop_start - 1 subdiv, loop_end + 1 subdiv]
•	Valid hits are associated with the nearest subdivision within that window.
•	subdivision state can rise only once per loop, additinal hits are discarded 
•	The subdivision's state is updated immediately based on hit history.
________________________________________
2. Subdivision States
Each subdivision has a state (integer 0–3) based on repeated hits across consecutive loops:
State	Color	Meaning	Promotion Rule
0	None	No associated hit	Default
1	Dark Gray	Hit once (current loop)	First hit within loop range
2	Orange	Hit again in next loop	Hit in 2 consecutive loops
3	Red	Hit again in third consecutive loop	Hit in 3 consecutive loops → Persistent red
•	state = 3 (red) is persistent: it never decays unless manually reset.
________________________________________
3. Decay Logic
•	If a subdivision receives no further hits for:

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
7. Saving & Loading Hit Data and Subdivision states
•	Hit data(absolute timestamps of hits) for state 3 subdivisions is automatically saved and loaded through the existing loop save/load system.
* from this data we can regenerate subdivision state upon loading
•	Save and Loads are Triggered via:
o	Ctrl+S → Save current loop + hits.
o	Shift+S → Load saved loop + hits.
o	Ctrl+Z → Revert to previous saved state (loop + hits).

________________________________________
8. Debug Logging
•	All functions involved in the hit flow will include extensive debug output using Brint([NHIT]...with added  A, B and PH position in H:M:S.1).
•	Each new log line related to hit logic will contain the tag:

[NHIT]
•	This includes:
o	Hit recording
o	Hit–subdivision association
o	State updates
o	Decay operations
o	Manual offsets
o	Save/load events involving hits

___________________________
 Decay Logic (in decay_subdivision_states)
•	Store last hit time per subdiv.
•	If now - last_hit_time > loop_duration + subdiv_interval, decrement state unless it’s already 0 or 3.
•	Add Brint for any downgrade:
python
CopyEdit
Brint(f"[NHIT] Subdiv {idx} decayed from state {prev} to {new}")
________________________________________
 Manual Offset
•	Only apply to subdivisions with state = 3.
•	Shift the 3  hit_timestamps linked to that subdiv by ± subdiv_interval.
•	Update hit_timestamps, re-run association, and state update.

