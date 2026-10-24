# Instructions pour l'Agent Hermes : Cron Hebdomadaire d'Audit Chauffage

Ce document définit le contrat d'interface, les accès et le cahier des charges complet pour l'agent **Hermes**, chargé d'exécuter l'analyse hebdomadaire du chauffage **chaque lundi à 09h00**.

---

## 1. Contexte & Caractéristiques de l'Installation

- **Chaudière :** Viessmann Vitrocrossal 300 CU3A (brûleur modulant Matrix ~4-19 kW, régulation Vitotronic 200).
- **Loi d'eau :** Pente 1.1, parallèle 0. Température de départ cible ~38°C à 0°C extérieur.
- **Bâti :** Maison ancienne en pierre de Jaumont (murs de 40 à 50 cm à forte inertie thermique).
- **Préparateur ECS :** Viessmann Vitocell 100 de 200 Litres vertical.
- **Stratégie ECS :** Plage unique 19h00 – 23h00 à 50°C. Cycle anti-légionelle automatique le dimanche de 19h00 à 20h30 à 60°C.
- **Régulation des pièces :** 
  - Chambre : Tête Zigbee Sonoff TRV (`climate.thermostat1`) débridée à +2°C en demande pour garder le clapet ouvert à 100%, sonde murale Sonoff (`sensor.thermo_1_temperature`).
  - Salon : Sonde murale (`sensor.thermo_2_temperature`).
  - Hystérésis Schmitt Trigger : 0.5°C pour éliminer les courts-cycles.

---

## 2. Accès à InfluxDB v2 (Source de Vérité 7 Jours)

L'agent Hermes extrait directement les métriques consolidées sur les 7 derniers jours :

- **URL de l'API Flux :** `http://192.168.1.171:8086/api/v2/query?org=homeassistant`
- **Méthode HTTP :** `POST`
- **Headers :**
  - `Authorization: Token heating-super-token-2026`
  - `Content-Type: application/vnd.flux`
  - `Accept: application/csv`
- **Organisation :** `homeassistant`
- **Bucket :** `heating`

---

## 3. Requêtes Flux Types pour l'Analyse 7 Jours

### A. Consommation Gaz & DJU Hebdomadaire
```flux
from(bucket: "heating")
  |> range(start: -7d)
  |> filter(fn: (r) => r["_measurement"] == "kWh" or r["_measurement"] == "DJU" or r["_measurement"] == "kWh/DJU")
  |> filter(fn: (r) => r["entity_id"] == "sensor.gaz_kwh_jour_effectif" 
                    or r["entity_id"] == "sensor.gaz_kwh_chauffage_jour" 
                    or r["entity_id"] == "sensor.gaz_kwh_ecs_jour" 
                    or r["entity_id"] == "sensor.gaz_dju_jour"
                    or r["entity_id"] == "sensor.heating_kwh_per_dj"
                    or r["entity_id"] == "sensor.gaz_total_kwh_per_dj")
  |> aggregateWindow(every: 1d, fn: max, createEmpty: false)
```

### B. Condensation & Comportement Brûleur
```flux
from(bucket: "heating")
  |> range(start: -7d)
  |> filter(fn: (r) => r["entity_id"] == "sensor.heating_condensing_ratio" 
                    or r["entity_id"] == "sensor.vitrocrossal_duree_moyenne_cycle"
                    or r["entity_id"] == "sensor.heating_short_cycles"
                    or r["entity_id"] == "sensor.vitrocrossal_allumages_jour_2")
  |> mean()
```

### C. Qualité de la Régulation & Écart Consignes
```flux
from(bucket: "heating")
  |> range(start: -7d)
  |> filter(fn: (r) => r["entity_id"] == "sensor.heating_setpoint_gap")
  |> mean()
```

---

## 4. Structure Attendue du Rapport d'Audit (Prompt Hermes)

Hermes doit analyser les corrélations multi-facteurs (météo vs conso réelle, respect de l'inertie, durée des cycles) et produire un rapport markdown au format suivant :

```markdown
# 📊 Rapport Hebdomadaire Chauffage — Semaine [WW] ([Date Début] au [Date Fin])

## 🏆 Score de Performance Globale : [XX] / 100
> **Appréciation :** [Ex: Excellent comportement de la condensation et très bonne tenue thermique de l'inertie pierre.]

---

## 📈 Métriques Clés de la Semaine (vs Semaine Précédente)
| Indicateur | Valeur Semaine | Cible Optimale | Statut |
|---|---|---|---|
| **Gaz Chauffage** | XX kWh | — | 🟢 / 🟡 / 🔴 |
| **Gaz Eau Chaude (ECS)** | XX kWh | ~25 à 30 kWh | 🟢 / 🟡 / 🔴 |
| **Intensité Chauffage** | XX kWh/DJU | < 4.5 kWh/DJU | 🟢 / 🟡 / 🔴 |
| **Intensité Globale** | XX kWh/DJU | < 6.0 kWh/DJU | 🟢 / 🟡 / 🔴 |
| **Taux de Condensation** | XX % | ≥ 92 % | 🟢 / 🟡 / 🔴 |
| **Durée Moyenne Cycles** | XX min | ≥ 20 min | 🟢 / 🟡 / 🔴 |
| **Cycles Courts (< 10 min)** | XX / semaine | 0 | 🟢 / 🟡 / 🔴 |
| **Écart Moyen Consigne** | ± XX °C | ≤ 0.5 °C | 🟢 / 🟡 / 🔴 |

---

## 🔍 Analyse & Corrélations Détectées
- **Comportement Thermique & Inertie :** [Explications sur la réponse du bâtiment]
- **Qualité de la Condensation :** [Analyse des températures de départ]
- **Cycles Brûleur & Usure :** [Analyse des allumages et modulation]
- **Production ECS :** [Respect de la plage 19h-23h et cycle anti-légionelle du dimanche]

---

## 🎯 Top 3 Actions d'Optimisation Prioritaires
1. **[Action 1 - Priorité Haute] :** [Description concrète, ex: ajuster la pente à 1.05 ou réhausser légèrement la consigne éco]
2. **[Action 2 - Priorité Moyenne] :** [...]
3. **[Action 3 - Priorité Basse / Observation] :** [...]
```

---

## 5. Diffusion Multi-Canal du Rapport

Chaque lundi matin à la fin de l'analyse, Hermes effectue 3 actions :

### A. Sauvegarde dans l'Historique Local (Fichier Markdown)
Enregistrer le rapport complet dans le répertoire :
```
/root/config/reports/heating/YYYY-WW_rapport_chauffage.md
```
*(Exemple : `/root/config/reports/heating/2026-W43_rapport_chauffage.md`)*

### B. Notification Persistante dans la WebUI Home Assistant
Appel HTTP REST à Home Assistant :
- **URL :** `http://192.168.1.160:8443/api/services/persistent_notification/create`
- **Méthode :** `POST`
- **Payload JSON :**
  ```json
  {
    "title": "📊 Audit Chauffage Hebdo — Score XX/100",
    "message": "[Texte résumé du rapport avec le Score et le Top 3 des actions]",
    "notification_id": "weekly_heating_audit"
  }
  ```

### C. Alerte Push sur l'iPhone de Loïc
- **URL :** `http://192.168.1.160:8443/api/services/notify/mobile_app_iphone_de_loic`
- **Méthode :** `POST`
- **Payload JSON :**
  ```json
  {
    "title": "🔥 Bilan Chauffage Semaine : XX/100",
    "message": "Condensation à XX%, intensité à XX kWh/DJU. Consultez le rapport complet dans l'application."
  }
  ```

### D. Telegram (Optionnel)
Si un bot Telegram est configuré dans l'environnement de Hermes, transmettre également le markdown complet sur le canal Telegram du domicile.

