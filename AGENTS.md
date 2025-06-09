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



🎯 Expected Behavior: Hit Association & Subdivision States (state = 2)
1. Hit Timing & Association
Chaque hit utilisateur est stocké avec un timestamp absolu (en millisecondes depuis le début du fichier).

Lors de son enregistrement :

Le hit est immédiatement associé à la subdivision la plus proche en temps.

La subdivision correspondante met immédiatement à jour son state selon les règles définies ci-dessous.

2. Subdivision States (Computed from Hit History)
Les subdivisions ont un champ state reflétant l'historique des hits reçus :

state = 0 : aucun hit associé,

state = 1 : hit associé dans une boucle récente (gris),

state = 2 : deux hits consécutifs (sur deux loops consécutives sans interruption, devient rouge et persistant).

Les hits eux-mêmes n'ont pas de state : seul leur association influence celui de la subdivision.

3. Loop Marker Behavior
Déplacer les marqueurs A et B :

N’affecte pas la position des subdivisions ni celle des hits (temps absolus),

Ne déclenche pas de réassociation,

N’affecte pas les states,

Ne modifie pas l'affichage visuel, tant que le zoom et le viewport restent constants.

4. Changing Tempo or Rhythm Mode
Modifier le tempo ou le mode rythmique (e.g., binaire → ternaire) :

Recalcule la position temporelle des subdivisions,

Déclenche une réassociation des hits vers la subdivision la plus proche dans le nouveau mode,

Nécessite un recalcul du state de chaque subdivision affectée.

5. Manual Subdivision Offset ([ / ])
Lorsqu'une subdivision rouge (state = 2) est décalée manuellement :

Les timestamps des hits associés sont déplacés d’un intervalle de subdivision (calculé selon le tempo et le mode courant),

Le state = 2 est conservé sur la nouvelle subdivision cible,

L'affichage reste inchangé si le zoom et le défilement sont constants.

6. Realtime Visual Feedback
Au moment de l'enregistrement d’un hit, la subdivision la plus proche :

Est immédiatement mise à jour visuellement,

Son state est recalculé en temps réel pour refléter l’impact du hit.


