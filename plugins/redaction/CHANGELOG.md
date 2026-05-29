# Changelog

## Unreleased

## v0.2.0 — 2026-05-29

### Added

- **Fallback « mode inline » sans filesystem persistant.** Nouvelle
  section de `SKILL.md` : sur un host sans écriture fichier (claude.ai
  web, Desktop hors repo), le SUIVI est tenu inline dans la conversation,
  exporté en fin de session dans un bloc copiable et réimporté à la
  reprise. L'export/réimport remplace la persistance fichier ; le reste
  du contrat (thèse verrouillée, une dérive par tour, pas de rédaction
  des paragraphes-cœur) est inchangé.
- **README — install multi-host.** Documentation des trois voies
  d'installation : plugin Claude Code (marketplace), bundle `.skill`
  (Claude Desktop double-clic / uploader claude.ai web), et symlink dev
  local. Note explicite sur la dégradation du SUIVI hors Claude Code.

### Changed

- **README — install plugin/dev corrigée.** Remplacement des
  placeholders `<repo-url>` / `<owner>` par le remote public
  `bastien-gallay/redaction` désormais publié.

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
