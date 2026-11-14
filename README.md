# formules

Formules mathématiques sur des voies de mesure, communes à GLviewer et à loggerFPGA :
ce moteur vivait en deux copies, une par application. Il est ici une seule fois, sans Qt,
avec numpy pour seule dépendance.

```python
import numpy as np
import formules
from formules import units

tree = formules.parse("([T sortie] - [T entrée]) / [P]")
formules.references(tree)             # (set(), {"T sortie", "T entrée", "P"})
formules.evaluate(tree, {"[T sortie]": np.array([40.0, 42.0]),
                         "[T entrée]": 20.0, "[P]": 200.0})     # array([0.1 , 0.11])
report = units.analyse(tree, {"[T sortie]": "°C", "[T entrée]": "°C", "[P]": "W"})
units.describe(report.unit)           # "K/W (résistance thermique)"
```

| Module | Rôle |
|---|---|
| `formules` | `parse`, `references`, `evaluate`, `FormulaError` |
| `formules.units` | Homogénéité d'une formule et unité de son résultat |
| `formules.lut` | Tables de correspondance : `steps(x; x1; y1...)`, `interp(x; x1; y1...)` |
| `formules.fluids` | Propriétés de l'eau et de l'air : `rho_water(T)`, `cp_air(T)`... |
| `formules.lexer`, `parser`, `nodes`, `interpreter`, `values`, `tokens` | Étapes du calcul, pour une application qui ajoute ses propres fonctions |

Une formule invalide (syntaxe, voie inconnue, calcul impossible) lève `FormulaError`, qui
est une `ValueError` au message affichable tel quel.

## Installer

Depuis une étiquette de version (une application ne change pas quand le moteur évolue) :

```
pip install git+https://github.com/florianmontaut/formules@v0.1.0
```

Pour travailler sur le moteur en même temps que sur une application, depuis ce dossier :

```
pip install -e .
```

## Tests

```
pip install -e .[dev]
python -m pytest
```

137 tests : lexer, parser, interpréteur, formules complètes, unités, caloporteurs, tables.

## Versions

Le numéro est dans `src/formules/__init__.py`. Une étiquette git par version (`v0.1.0`).
Tant que le paquet est en 0.x, un changement incompatible monte la version mineure.
