import os
import json
from typing import List, Dict, Any, Optional


class ModelDetails:
    """Class representing the details of a single model extracted from a JSON file."""

    # Constants for JSON keys
    KEY_TITLE = 'title'
    KEY_IDENTIFIER = 'identifier'
    KEY_DESCRIPTION = 'description'
    KEY_SPECIAL_NOTES = 'special notes'
    KEY_LINKS = 'links'
    KEY_RECORD_TO = 'record_to'
    KEY_EXTRAS = 'extras'
    KEY_PARAMETERS = 'Parameters'
    KEY_FORMULA = 'Formula'

    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path
        self.name: Optional[str] = None
        self.kadi_identifier: Optional[str] = None
        self.description: Optional[str] = None
        self.special_note: Optional[str] = None
        self.parameters: Optional[str] = None
        self.formula: Optional[str] = None
        self.article_identifier: Optional[str] = None

        self._load_and_extract_details()

    def _load_json_file(self) -> Dict[str, Any]:
        """Loads a JSON file and returns its content as a dictionary."""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading JSON file at {self.json_file_path}: {str(e)}") from e

    def _extract_details(self, data: Dict[str, Any]) -> None:
        """Extracts model details from a JSON object and sets them as class attributes."""
        self.name = data.get(self.KEY_TITLE, '')
        self.kadi_identifier = data.get(self.KEY_IDENTIFIER, '')
        self.description = data.get(self.KEY_DESCRIPTION, '')
        self.special_note = data.get(self.KEY_SPECIAL_NOTES, '')
        self.article_identifier = data.get(self.KEY_LINKS, [{}])[0].get(self.KEY_RECORD_TO, {}).get(self.KEY_IDENTIFIER, '')

        extras = data.get(self.KEY_EXTRAS, [])
        self.parameters = next((item['value'] for item in extras if item.get('key') == self.KEY_PARAMETERS), '')
        self.formula = next((item['value'] for item in extras if item.get('key') == self.KEY_FORMULA), '')

    def _load_and_extract_details(self) -> None:
        """Loads a JSON file and extracts model details."""
        data = self._load_json_file()
        self._extract_details(data)

    def display_details(self) -> None:
        """Prints the model details."""
        print(f"Name: {self.name}")
        print(f"Kadi Identifier: {self.kadi_identifier}")
        print(f"Description: {self.description}")
        print(f"Special Note: {self.special_note}")
        print(f"Parameters: {self.parameters}")
        print(f"Formula: {self.formula}")
        print(f"Article Identifier: {self.article_identifier}")


def load_models_from_directory(directory_path: str) -> List[ModelDetails]:
    """Loads all models from JSON files in the specified directory."""
    if not os.path.isdir(directory_path):
        raise ValueError(f"The specified directory does not exist: {directory_path}")

    json_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.json')]
    if not json_files:
        raise ValueError(f"No JSON files found in the specified directory: {directory_path}")

    models = []
    for json_file in json_files:
        try:
            model = ModelDetails(json_file)
            models.append(model)
        except ValueError as e:
            print(f"Warning: {e}")

    return models
