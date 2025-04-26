class PythonGenerator:
    def generate(self, parsed):
        self.inputs = parsed["inputs"]
        self.outputs = parsed["outputs"]
        self.assignments = parsed["assignments"]

        lines = []

        # Declare inputs
        for inp in self.inputs:
            lines.append(f"{inp} = input()")

        # Declare outputs
        for out in self.outputs:
            lines.append(f"{out} = output()")

        for var, conditions in self.assignments.items():
            lines.append("")
            first_condition = True  # <-- Track first condition for each variable

            for idx, (cond, val) in enumerate(conditions):
                if cond == "else":
                    lines.append(f"else:")
                    lines.append(f"    {var} = {val}")
                elif cond == "":
                    lines.append(f"{var} = {val}")
                else:
                    prefix = "if" if first_condition else "elif"
                    lines.append(f"{prefix} {cond}:")
                    lines.append(f"    {var} = {val}")
                    first_condition = False  # <-- After first, switch to elif

        return "\n".join(lines)
    
    """
INPUT tenko
OUTPUT token

assign token = tenko * 2

IF token < 10 THEN
  assign token = 15
ELIF token > 10 THEN
  assign token = -15
ELSE
  assign token = 0"""
