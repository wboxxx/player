# AGENTS.md

## Agent: `codex_ui_debugger`

### Objectif
Cet agent sert à tester les comportements d’affichage dans l’interface de Codex, notamment :
- le bon rendu de la timeline et des éléments visuels audio,
- le suivi précis et fluide du **playhead** pendant la lecture.

---

### Fichier de test

- **Nom** : `bcbsm-006_hi`
- **Type** : audio uniquement
- **Format** : `.wav` ou `.mp3`
- **Usage** : fichier léger servant à déclencher les routines de dessin de la timeline sans surcharge inutile. Il permet de tester les déplacements du playhead en conditions contrôlées.

---

### Configuration Debug

Pour observer les mises à jour du **playhead** sans activer tous les logs internes, configure les flags comme suit :

```python
DEBUG_FLAGS = {
    ...
    "PH": True,
    "BRINT": False,
    ...
}
Use the provided stub environment to avoid full VLC/ALSA dependencies.

Load the bcbsm-006_hi.wav file.

Set DEBUG_FLAGS["PH"] = True and DEBUG_FLAGS["BRINT"] = False.

Create a minimal canvas or dummy VideoPlayer object and repeatedly call update_playhead_by_time() with increasing timestamps (for example, in 100 ms steps).

Watch the console for [PH DRAW] messages showing x coordinates. This confirms that the playhead’s x positions are being drawn in sequence.

If the playhead stops appearing when playback is paused, ensure the update_playhead_by_time() function no longer exits early on self.player.is_playing() so that the canvas still refreshes.
```
