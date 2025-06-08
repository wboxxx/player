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
    v_px_per_s = v_frac * canvas_width
    return v_px_per_s
