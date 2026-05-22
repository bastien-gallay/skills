# Changelog

## Unreleased

## v0.1.0 — 2026-05-22

### Added

- **Skill `/redaction` extrait dans un repo dédié.** Initialement vivant
  sous `~/.claude/skills/redaction/`, désormais source-of-truth versionnée
  à `~/Dev/personal/skills/redaction/`. Installation locale via symlink
  `~/.claude/skills/redaction → skills/redaction`.
- **Phase 0 étape 4 — Fichier de suivi (SUIVI).** Scaffold automatique de
  `.personal/ecriture/SUIVI-<basename>.md` à la première invocation sur
  un nouvel écrit ; lecture intégrale et respect des éléments verrouillés
  (thèse, architecture, bijoux, décisions actées) à la reprise.
- **Section « Fichier de suivi (`SUIVI-*.md`) ».** Cycle de vie (création
  / chaque tour / hygiène / fin de session / reprise), sections
  obligatoires vs optionnelles, règles (concision, pas de duplication,
  pas de scaffold visuel, pas d'auto-attribution). Template copy-paste
  fourni dans `skills/redaction/suivi-template.md`.
- **Cross-référencement Axx/Bxx.** Chaque piège du catalogue porte
  désormais en titre son code de référence vers `style-bastien.md` §0
  du repo consommateur — `A8`/`B3` pour Hedging, `B1` pour Registre
  LinkedIn, `B4` pour Pathos / Transitions mémoire, `B2` pour Conclusion
  qui nuance. Les pièges propres au skill (Thèse molle, Re-cloisonnement,
  Énumération qui esquive, Croissance quantitative) sont marqués
  `(candidat §0)` — à promouvoir via un mode rétrospectif quand 3+
  occurrences sont observées.
- **Colonne `Code` dans l'audit phrase par phrase.** Le format de retour
  intègre le code Axx/Bxx à côté du verdict (`✅` / `🔧` / `✂️`).
- **Workflow exécutif** mis à jour pour refléter le scaffold du SUIVI en
  Phase 0 et le tag Axx/Bxx en critique.
