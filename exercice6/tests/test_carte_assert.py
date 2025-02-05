import pathlib
import sys

root_path = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(root_path))

from modules import Carte

def test_carte():
    carte = Carte("As", "Cœur")
    assert str(carte) == "As de Cœur"
    print("Test simple réussi !")

if __name__ == "__main__":
    test_carte()
