from collections import defaultdict
from typing import List

class PseudocodeParser:
    def __init__(self):
        self.errors = []

    @property
    def errors(self) -> List:
        return self._errors

    @errors.setter
    def errors(self, errs: List):
        self._errors = errs

    def parse(self, pseudocode: str):
        self.errors = []
        lines = pseudocode.strip().splitlines()
        inputs = set()
        outputs = set()
        assignments = defaultdict(list)
        current_conditions = []

        def get_indent(line):
            return len(line) - len(line.lstrip())

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            if line.startswith("INPUT "):
                parts = line.split(" ", 1)
                if len(parts) != 2 or not parts[1].isidentifier():
                    self.errors.append(f"Invalid INPUT syntax at line {i+1}: '{line}'")
                else:
                    inputs.add(parts[1])

            elif line.startswith("OUTPUT "):
                parts = line.split(" ", 1)
                if len(parts) != 2 or not parts[1].isidentifier():
                    self.errors.append(f"Invalid OUTPUT syntax at line {i+1}: '{line}'")
                else:
                    outputs.add(parts[1])

            elif line.startswith("IF ") or line.startswith("ELIF "):
                if not line.endswith(" THEN"):
                    self.errors.append(f"Missing 'THEN' at line {i+1}: '{line}'")
                condition = line.split(" ", 1)[1].rsplit(" THEN", 1)[0]
                if not condition:
                    self.errors.append(f"Empty condition at line {i+1}: '{line}'")
                current_conditions = [condition]

            elif line.startswith("ELSE"):
                if line != "ELSE":
                    self.errors.append(f"Invalid ELSE syntax at line {i+1}: '{line}'")
                current_conditions = ["else"]

            elif line.startswith("assign "):
                assign_part = line[len("assign "):]
                if "=" not in assign_part:
                    self.errors.append(f"Invalid assignment syntax at line {i+1}: '{line}'")
                    i += 1
                    continue
                var_val = assign_part.split("=", 1)
                var = var_val[0].strip()
                val = var_val[1].strip()
                if val.startswith("=") or val.endswith("="):
                    self.errors.append(f"Too much '=' at line {i+1}: '{var}'")
                if not var.isidentifier():
                    self.errors.append(f"Invalid variable name at line {i+1}: '{var}'")
                if not val:
                    self.errors.append(f"Empty value in assignment at line {i+1}: '{line}'")
                condition = current_conditions[-1] if current_conditions else ""
                if condition == "else":
                    assignments[var].append(("else", val))
                else:
                    assignments[var].append((" and ".join(current_conditions), val))
            else:
                self.errors.append(f"Unknown statement at line {i+1}: '{line}'")

            # check if next line has less indentation (ending IF block)
            if i + 1 < len(lines) and get_indent(lines[i + 1]) < get_indent(lines[i]):
                current_conditions = []

            i += 1

        return {"inputs": inputs, "outputs": outputs, "assignments": dict(assignments)}
