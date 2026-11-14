# formules — contexte pour Claude

Moteur de formules partagé par les applications de l'utilisateur (GLviewer, loggerFPGA) :
lexer, parser, interpréteur numpy, homogénéité des unités, tables de correspondance,
caloporteurs. Dépôt : https://github.com/florianmontaut/formules (branche `main`).

## Travailler avec l'utilisateur

- Répondre en **français**. Avis francs, formulés avec douceur.
- Ne committer / pousser que sur demande explicite.
- Proposer et discuter l'approche avant un développement important.

## Environnement

- Python 3.11, numpy 1.26, pytest. Aucune dépendance vers Qt, ni vers une application.
- Tests : `python -m pytest` (moins d'une seconde).

## Règles

- Les applications dépendent de l'interface publique (`parse`, `references`, `evaluate`,
  `FormulaError`, `units`, `lut`, `fluids`, et les classes `Interpreter`, `FuncNode`...
  que loggerFPGA étend) : ne pas renommer ni changer une signature sans monter la version
  et le signaler. Ajouter plutôt que modifier.
- `FormulaError` hérite de `ValueError` seulement. Dans GLviewer, elle héritait aussi de
  `AnalysisError` : une application qui veut ce comportement l'attrape explicitement.
- Les fonctions propres à une application (dérivée, intégrale, moyenne glissante de
  loggerFPGA) restent dans l'application, tant qu'une deuxième n'en a pas besoin.
- Toute évolution arrive avec ses tests.

## Origine

Code repris de GLviewer (`model/formula`, commit 5740833), lui-même issu du projet LEXER.
loggerFPGA en avait une copie (`logger_app/model/formula`).

## Non fait

- GLviewer utilise encore sa copie (`model/formula`) ; loggerFPGA utilise ce paquet.
