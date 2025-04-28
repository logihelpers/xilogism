# boolean_converter.py

import re

class BooleanConverter:
    def __init__(self):
        self.nodes = {}
        self.counter = {
            "constant": 0,
            "multiplier": 0,
            "comparator": 0,
            "adder": 0,
            "logic": 0,
            "wire": 0
        }

    def _new_name(self, prefix):
        self.counter[prefix] += 1
        return f"{prefix}_{self.counter[prefix]}"

    def simplify_condition(self, condition: str):
        # Basic simplification: identify simple comparators and logic ops
        if any(op in condition for op in ["<", ">", "==", "!="]):
            return condition.strip()
        else:
            return condition.replace(" ", "").strip()

    def add_constant(self, value):
        name = f"constant_{value}" if isinstance(value, int) else self._new_name("constant")
        if name not in self.nodes:
            self.nodes[name] = {
                "type": "CONSTANT",
                "value": value,
                "hierarchy": 0
            }
        return name

    def process_expr(self, expr, from_var):
        expr = expr.strip()
        # Multiplication handling
        if "*" in expr:
            terms = [t.strip() for t in expr.split("*")]
            mul_name = self._new_name("multiplier")
            inputs = []
            for term in terms:
                if term.isdigit():
                    const = self.add_constant(int(term))
                    inputs.append(const)
                else:
                    inputs.append(term)
            self.nodes[mul_name] = {
                "type": "BLOCK",
                "block_type": "MULTIPLIER",
                "inputs": inputs,
                "output": mul_name,
                "hierarchy": 1
            }
            return mul_name
        elif expr.isdigit():
            return self.add_constant(int(expr))
        else:
            return expr

    def convert(self, python_code: str):
        self.nodes = {}
        self.counter = {
            "constant": 0,
            "multiplier": 0,
            "comparator": 0,
            "adder": 0,
            "logic": 0,
            "wire": 0
        }

        lines = python_code.strip().splitlines()
        current_condition = None
        last_var = None

        for line in lines:
            stripped = line.strip()

            if not stripped:
                continue

            if " = input()" in stripped:
                var = stripped.split("=")[0].strip()
                self.nodes[var] = {
                    "type": "INPUT_NODE",
                    "hierarchy": 0
                }

            elif " = output()" in stripped:
                var = stripped.split("=")[0].strip()
                self.nodes[var] = {
                    "type": "OUTPUT_NODE",
                    "hierarchy": -1
                }

            elif stripped.startswith("if ") or stripped.startswith("elif "):
                condition = stripped.split(' ', 1)[1].rstrip(":")
                current_condition = self.simplify_condition(condition)

            elif stripped.startswith("else:"):
                current_condition = "default"

            elif "=" in stripped:
                var, expr = map(str.strip, stripped.split("=", 1))
                expr_result = self.process_expr(expr, var)

                if current_condition == "default" or current_condition is None:
                    self.nodes[self._new_name("wire")] = {
                        "type": "WIRE",
                        "from": expr_result,
                        "to": var,
                        "hierarchy": 2
                    }
                else:
                    comp_name = self._new_name("comparator")
                    self.nodes[comp_name] = {
                        "type": "BLOCK",
                        "block_type": "COMPARATOR",
                        "condition": current_condition,
                        "true_path": expr_result,
                        "false_path": None,  # Else branch would fill this
                        "output": var,
                        "hierarchy": 2
                    }

        return self.nodes

