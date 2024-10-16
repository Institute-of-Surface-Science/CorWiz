import os
import json
from typing import List, Dict, Union, Tuple, Optional, Any
from .model import Model


class CorrosionModel(Model):
    """
    A base class for corrosion models, inheriting from the Model class.

    This class serves as a template for specific corrosion models, providing basic attributes
    and methods that can be overridden by subclasses.

    Attributes:
        model_name (str): The name of the corrosion model.
    """

    def __init__(self, json_file_path: str, model_name: str = 'parent class'):
        """
        Initializes the corrosion model with a JSON file and a specified model name.

        Args:
            json_file_path (str): Path to the JSON file containing model details.
            model_name (str): The name of the corrosion model. Defaults to 'parent class'.
        """
        super().__init__(json_file_path)  # Initialize the Model base class
        self.model_name = model_name
        self.model_coordinates = None # Initialize the coordinates associated with the model to be None

    def evaluate_material_loss(self, *args, **kwargs):
        """
        Placeholder method for evaluating material loss.

        This method should be overridden by subclasses to provide specific implementations.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def massloss_is_thickness(self):
        return True

class CorrosionProcessTypeError(Exception):
    """Custom exception for invalid corrosion process type."""
    pass


def get_corrosion_process_type(models: Union[Model, List[Model]]) -> Union[Tuple[Model, str], List[Tuple[Model, str]]]:
    """
    Determines the corrosion process type for a single model or a list of models based on their tags.

    This function inspects the tags associated with each model to identify the corrosion process type.
    A valid tag must contain exactly three words, with the second-to-last word being "corrosion" and
    the last word being "model". The corrosion process type is then extracted from the first word in the tag.

    Args:
        models (Union[Model, List[Model]]): A single model instance or a list of model instances to check.

    Returns:
        Union[Tuple[Model, str], List[Tuple[Model, str]]]:
            - If a single model is passed, returns a tuple (model, process_type).
            - If a list of models is passed, returns a list of tuples where each tuple is (model, process_type).

    Raises:
        CorrosionProcessTypeError: If no valid tag is found in a model, i.e., no tag contains exactly
                                   three words with the last two words being "corrosion model".
        TypeError: If the input is neither a Model instance nor a list of Model instances.
    """

    def determine_type(model: Model) -> str:
        """Helper function to determine the corrosion process type for a single model."""
        for tag in model.tags:
            words = tag.split()
            # The tag must have exactly three words, with the last two being "corrosion" and "model"
            if len(words) == 3 and words[-2] == "corrosion" and words[-1] == "model":
                process_type = words[0] + " corrosion"  # Extract and format the process type
                return process_type

        raise CorrosionProcessTypeError("Model does not have any valid corrosion process tags.")

    if isinstance(models, Model):
        # Handle the case where a single model is passed
        process_type = determine_type(models)
        return models, process_type

    elif isinstance(models, list):
        # Handle the case where a list of models is passed
        model_process_pairs = []
        for model in models:
            try:
                process_type = determine_type(model)
                model_process_pairs.append((model, process_type))
            except CorrosionProcessTypeError as e:
                print(f"Error processing model {model.name}: {e}")

        return model_process_pairs

    else:
        raise TypeError("Input must be a Model instance or a list of Model instances.")


def load_corrosion_models_from_directory(directory_paths: Union[str, List[str]], model_classes: Dict[str, Any]) -> List[CorrosionModel]:
    """Loads all corrosion models from JSON files in the specified directory or directories.

    Args:
        directory_paths (Union[str, List[str]]): A single directory path or a list of directory paths.
        model_classes (Dict[str, Any]): A dictionary mapping model identifiers to their corresponding classes.

    Returns:
        List[CorrosionModel]: A list of CorrosionModel instances loaded from the JSON files in the specified directory or directories.

    Raises:
        ValueError: If a directory does not exist or no JSON files are found.
    """
    if isinstance(directory_paths, str):
        directory_paths = [directory_paths]  # Convert to a list for uniform processing

    corrosion_models = []
    for directory_path in directory_paths:
        if not os.path.isdir(directory_path):
            raise ValueError(f"The specified directory does not exist: {directory_path}")

        json_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.json')]
        if not json_files:
            raise ValueError(f"No JSON files found in the specified directory: {directory_path}")

        for json_file in json_files:
            try:
                # Load the JSON data
                with open(json_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                # Determine the model identifier
                model_identifier = data.get('identifier', '')

                # Match the identifier with the corresponding class
                if model_identifier in model_classes:
                    corrosion_model = model_classes[model_identifier](json_file)
                    corrosion_models.append(corrosion_model)
                else:
                    print(f"Warning: No matching corrosion model class for identifier '{model_identifier}' in file {json_file}")

            except (ValueError, json.JSONDecodeError) as e:
                print(f"Warning: Error processing JSON file at {json_file}: {str(e)}")

    return corrosion_models