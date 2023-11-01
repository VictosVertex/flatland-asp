"""
    This is a basic example of how to run clingo from python
    
"""
from clingo.control import Control
from clingo import Model


def on_model(model: Model) -> None:
    """ Prints the current model to the terminal

        Args:
            model: Model that was found, which satisfies the provided instance/encoding
    """
    print(f"{model}")


# Creating the clingo control class which manages loading, grounding and solving
ctl = Control()

# Load some ASP instance from a file
ctl.load("clingo_python_example_instance_and_encoding.lp")

# Ground the program
ctl.ground()

# Start solving
# Intercept each model with the on_model method
# On finish return the result
result = ctl.solve(on_model=on_model)

# Print the result
# ("SAT" in case the program is satisfied, "UNSAT" in case it is not)
print(result)
