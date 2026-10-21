# Directives pour l'Agent IA (Antigravity)

Ce répertoire contient la configuration Home Assistant de la maison.

## Accès Home Assistant pour l'Agent

L'agent dispose de **deux méthodes d'accès** complémentaires pour interagir avec Home Assistant :

### 1. Serveur MCP Home Assistant (`homeassistant`)
Configuré dans `mcp_config.json` via l'endpoint MCP `https://ha.typhon0.com/api/mcp`.
Permet d'appeler directement les outils natifs :
- `assist__homeassistant__GetLiveContext` : consulter l'état en direct des appareils, zones ou domaines (ex. `climate`, `light`, `sensor`).
- `assist__climate__HassClimateSetTemperature` : ajuster les consignes des thermostats.
- `assist__intent__HassTurnOn` / `assist__intent__HassTurnOff` : allumer/éteindre des entités.
- `home-assistant-services__HassCallService` : appeler n'importe quel service Home Assistant.
- `assist__todo__*` / `assist__media_player__*` / `assist__llm__GetDateTime`.

### 2. API REST Home Assistant
Accessible en local sur `http://192.168.1.160:8443` via le token configuré dans [`.env`](file://homeassistant/config/.env) et [`secrets.yaml`](file://homeassistant/config/secrets.yaml).
Indispensable pour l'administration et le développement :
1. **Validation syntaxique YAML :** `POST /api/config/core/check_config`
2. **Simulation Jinja2 en temps réel :** `POST /api/template`
3. **Rechargement à chaud des configurations :** `POST /api/services/<domain>/reload` (ex. `automation`, `template`, `input_datetime`)
4. **Lecture directe des états et attributs complets :** `GET /api/states/<entity_id>`

## Documentation Métier & Références

- [`DOCUMENTATION_CHAUFFAGE.md`](file:///root/config/DOCUMENTATION_CHAUFFAGE.md) : Guide de référence exhaustif du chauffage (chaudière Viessmann Vitrocrossal 300, loi d'eau 1.1, régulation, hystérésis, débridage TRV, ECS 19h-23h, anti-légionelle et télémétrie).

## Bonnes pratiques pour l'agent

- **Validation systématique :** Toujours appeler `/api/config/core/check_config` après modification d'un fichier YAML avant de finaliser la réponse.
- **Rechargement à chaud :** Recharger les services concernés immédiatement après modification pour appliquer les changements.
- **Sécurité des secrets :** Ne jamais écrire le token en clair dans les fichiers suivis par Git (`.gitignore` protège `.env` et `secrets.yaml`).
