import json
import os
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def save_to_json(data: dict, file_output_path: str) -> None:
    """
    Save data to a JSON file.

    Args:
        data (dict): The data to save.
        file_output_path (str): The path to save the JSON file.

    Raises:
        ValueError: If the data is not serializable to JSON.
        IOError: If there is an issue writing the file.
    """
    try:
        # Vérifier si les données sont bien sérialisables avant d'écrire le fichier
        json.dumps(data, ensure_ascii=False, indent=4)

        # S'assurer que le dossier de destination existe
        os.makedirs(os.path.dirname(file_output_path), exist_ok=True)

        # Sauvegarde du fichier JSON
        with open(file_output_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        logging.info(f"✔ JSON file successfully saved at: {file_output_path}")

    except TypeError as e:
        logging.error(f"❌ Data is not serializable to JSON: {e}")
        raise ValueError(f"Data provided is not serializable to JSON: {e}")

    except IOError as e:
        logging.error(f"❌ Failed to write JSON file at {file_output_path}: {e}")
        raise IOError(f"Failed to write JSON file at {file_output_path}: {e}")
