# Santorini

### Authors: Tom Wallenstein Emily Slaughter

## Design patterns used:
1. Abstract factory method

ex. PlayerFactory class creates a new instance of a subclass of Player based on the desired type.

2. Memento

ex. History class (Caretaker) keeps track of Turn objects (Mementos).

3. Template

ex. Player class is a template for Human/AI subclasses to finish defining substeps of a commonly defined process.

4. Strategy pattern

ex. The set of heuristics functions follow the strategy pattern. All three function have a common interface and implement different solutions for the same problem, e.g. evaluate the current position of the worker on the board. 
