# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
- Membres du foyer (famille et occupants) au quotidien, avec des niveaux d'aisance technique variés.
- Visiteurs ou invités pouvant interagir avec l'écran tactile du salon/entrée.

## Product Purpose
- Offrir une interface centrale, intuitive et réactive pour piloter et surveiller l'habitat en temps réel.
- Permettre le contrôle immédiat du confort (éclairage, consigne de chauffage/thermostats, ambiance multimédia) et le suivi de l'énergie.
- Critère de réussite : une interaction fluide en un seul geste, un état global compréhensible en un clin d'œil sans surcharge d'informations.

## Positioning
- Hub domotique domestique unifié et sur mesure, adapté aux habitudes et pièces de la maison, éliminant la dispersion entre applications propriétaires.

## Operating Context
- Tablette tactile murale dédiée en affichage permanent (mode kiosk) dans les pièces de vie.
- Application mobile Home Assistant Companion (iOS / Android) pour le contrôle en mobilité et hors du domicile.
- Consultation et administration occasionnelle sur navigateur desktop.

## Capabilities and Constraints
- Environnement : Home Assistant (mode YAML), intégrant Zigbee2MQTT, ESPHome, DIYHue, Alexa, HomeKit, Proxmox, Tesla, Jellyfin.
- Écosystème Lovelace existant : `button-card`, `layout-card`, `kiosk-mode`, `card-mod`, `mushroom`, `apexcharts-card`, `mini-graph-card`.
- Architecture de cartes : flexibilité confirmée pour faire évoluer et adapter les templates ou modules de cartes (Mushroom, custom button cards, sections Lovelace) pour servir au mieux l'ergonomie.

## Brand Commitments
- Design sobre, élégant et chaleureux s'intégrant discrètement dans la pièce de vie.
- Confort visuel : fond adapté et transitions douces pour éviter l'éblouissement ou la fatigue visuelle, notamment en soirée et de nuit.

## Evidence on Hand
- Fichiers dashboards Lovelace : `/config/ui-lovelace.yaml`, `/config/salon_dashboard.yaml`, `/config/maison_energie_dashboard.yaml`.
- Bibliothèques de templates et styles : `/config/button_card_templates/`, `/config/themes/tablet.yaml`, thèmes minimalist.
- Entités et règles opérationnelles réelles : `/config/automations.yaml`, `/config/scripts.yaml`, `/config/template.yaml`, `/config/sensors.yaml`.

## Product Principles
- **Glanceability (Lisibilité immédiate)** : les états essentiels (lumières actives, température ambiante vs consigne, alertes) sont perceptibles à distance sans toucher l'écran.
- **Accès instantané (1-tap control)** : les actions les plus fréquentes (marche/arrêt éclairage, scénarios clés) s'exécutent en un seul tap direct avec feedback visuel clair.
- **Sobriété et discrétion domestique** : l'écran fait partie intégrante de la décoration du foyer, évitant les surcharges cognitives et les animations superflues.
- **Continuité tablette / mobile** : hiérarchie et repères cohérents entre l'écran mural kiosk et l'accès sur smartphone.

## Accessibility & Inclusion
- Zones tactiles larges (touch targets confortables) adaptées à un usage tactile mural debout ou en passant.
- Typographie et contrastes calibrés pour rester lisibles à 1–2 mètres de distance.

