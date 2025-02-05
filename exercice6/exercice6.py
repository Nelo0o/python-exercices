# Exercice numéro 6 ! 👊
# 1. Créer des tests pour votre class créée à la question 2 de l'exercice 5
# 2. Même chose qu'à la question 1, mais avec pytest.

import pathlib
import sys

# Ajouter le chemin racine au sys.path pour pouvoir importer les modules
root_path = pathlib.Path(__file__).parent.resolve()
sys.path.append(str(root_path))

if __name__ == "__main__":
    # Test avec un simple assert
    print("\n=== Test avec assert ===")
    from tests.test_carte_assert import test_carte
    test_carte()

    # Tests avec pytest
    print("\n=== Tests avec pytest ===")
    print("Pour lancer les tests pytest, il faut faire :")
    print("python -m pytest tests/test_carte_pytest.py -v")
