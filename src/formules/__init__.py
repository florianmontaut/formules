# formules/__init__.py
"""
formules : formules mathématiques sur des voies de mesure (lexer -> parser -> interpréteur
numpy), avec contrôle de l'homogénéité des unités, tables de correspondance et propriétés
de caloporteurs. Moteur commun à GLviewer et à loggerFPGA, sans Qt.

    parse(text)          -> arbre de la formule (FormulaError si syntaxe invalide)
    references(tree)     -> voies utilisées : identifiants (CH3, time...) et [noms]
    evaluate(tree, vars) -> float ou np.ndarray ; vars : {"CH3": ..., "[T AMB]": ...}
    units.analyse(tree, {"[T AMB]": "°C"}) -> unité du résultat (homogénéité)
    lut                  -> tables steps(x; x1; y1...) et interp(x; x1; y1...)
    fluids               -> caloporteurs : rho_water(T), cp_air(T)...
"""
__version__ = "0.1.0"

from .errors import FormulaError
from .interpreter import CONSTANTS, Interpreter
from .lexer import Lexer
from .nodes import ChannelNode, FuncNode, VariableNode
from .parser import MathParser


def parse(text: str):
    tree = MathParser(Lexer(text).generate_tokens()).parse()
    if tree is None:
        raise FormulaError("Empty formula")
    return tree


def references(tree) -> tuple[set, set]:
    """(identifiants hors constantes, noms entre crochets) utilisés par la formule."""
    names, channels = set(), set()

    def walk(node):
        if isinstance(node, VariableNode):
            if node.name not in CONSTANTS:
                names.add(node.name)
        elif isinstance(node, ChannelNode):
            channels.add(node.name)
        elif isinstance(node, FuncNode):
            for arg in node.args:
                walk(arg)
        else:
            for value in vars(node).values():
                if hasattr(value, "__dataclass_fields__"):
                    walk(value)
    walk(tree)
    return names, channels


def evaluate(tree, variables: dict):
    """Valeur de la formule, dans un contexte neuf (pas de variables d'un calcul précédent)."""
    interpreter = Interpreter()
    interpreter.vars.update(variables)
    return interpreter.visit(tree).value
