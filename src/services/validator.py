# python_validator.py

class PythonValidator:
    def validate(self, code: str):
        lines = code.strip().splitlines()
        errors = []
        declared_vars = set()
        input_vars = set()
        output_vars = set()

        python_builtins = {"input", "output", "int", "str", "bool", "not", "and", "or"}

        # First pass: register declared vars
        for line in lines:
            stripped = line.strip()
            if " = input()" in stripped:
                var = stripped.split(" = ")[0].strip()
                input_vars.add(var)
                declared_vars.add(var)
            elif " = output()" in stripped:
                var = stripped.split(" = ")[0].strip()
                output_vars.add(var)
                declared_vars.add(var)
            elif " = " in stripped:
                var = stripped.split(" = ")[0].strip()
                declared_vars.add(var)

        # Second pass: check for misuse and invalid conditions
        for idx, line in enumerate(lines):
            stripped = line.strip()

            # Validate IF/ELIF statements
            if stripped.startswith("if") or stripped.startswith("elif"):
                if stripped.endswith(":"):
                    condition = stripped[2 if stripped.startswith("if") else 4 : -1].strip()
                    if not condition:
                        errors.append(f"Error: Empty condition at line {idx + 1}.")

            if " = " in stripped:
                var, val = map(str.strip, stripped.split(" = ", 1))
                # Check input reassignment
                if var in input_vars and not stripped.endswith(" = input()"):
                    errors.append(f"Error: Input variable '{var}' is read-only and cannot be modified.")
                # Check all used variables in RHS
                tokens = val.replace("(", " ").replace(")", " ") \
                            .replace("+", " ").replace("-", " ").replace("*", " ") \
                            .replace("/", " ").replace("<", " ").replace(">", " ") \
                            .replace("==", " ").replace("!=", " ").replace("<=", " ") \
                            .replace(">=", " ").replace(",", " ").split()

                for token in tokens:
                    if token.isidentifier() and token not in declared_vars and token not in python_builtins:
                        errors.append(f"Error: Variable '{token}' used before declaration at line {idx + 1}.")

        return errors
