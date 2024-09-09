import os
import json
from typing import List, Dict, Union, Tuple, Optional, Any
from .measurement import Measurement


class CorrosionMeasurement(Measurement):
    """
    A base class for corrosion measurements, inheriting from the Measurement class.

    This class serves as a template for specific corrosion measurements, providing basic attributes
    and methods that can be overridden by subclasses.

    Attributes:
        measurement_name (str): The name of the corrosion measurement.
    """

    def __init__(self, json_file_path: str, measurement_name: str = 'parent class'):
        """
        Initializes the corrosion measurement with a JSON file and a specified measurement name.

        Args:
            json_file_path (str): Path to the JSON file containing measurement details.
            measurement_name (str): The name of the corrosion measurement. Defaults to 'parent class'.
        """
        super().__init__(json_file_path)  # Initialize the Measurement base class
        self.measurement_name = measurement_name
        self.measurement_coordinates = None # Initialize the coordinates associated with the measurement to be None

    def get_material_loss(self, *args, **kwargs):
        """
        Placeholder method for returning material loss.

        This method should be overridden by subclasses to provide specific implementations.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")


def load_corrosion_measurements_from_directory(directory_paths: Union[str, List[str]], measurement_classes: Dict[str, Any]) -> List[CorrosionMeasurement]:
    """Loads all corrosion measurements from JSON files in the specified directory or directories.

    Args:
        directory_paths (Union[str, List[str]]): A single directory path or a list of directory paths.
        measurement_classes (Dict[str, Any]): A dictionary mapping measurement identifiers to their corresponding classes.

    Returns:
        List[CorrosionMeasurement]: A list of CorrosionMeasurement instances loaded from the JSON files in the specified directory or directories.

    Raises:
        ValueError: If a directory does not exist or no JSON files are found.
    """
    if isinstance(directory_paths, str):
        directory_paths = [directory_paths]  # Convert to a list for uniform processing

    corrosion_measurements = []
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

                # Determine the measurement identifier
                measurement_identifier = data.get('identifier', '')
                
                # Match the identifier with the corresponding class
                if measurement_identifier in measurement_classes:
                    corrosion_measurement = measurement_classes[measurement_identifier](json_file)
                    corrosion_measurements.append(corrosion_measurement)
                else:
                    print(f"Warning: No matching corrosion measurement class for identifier '{measurement_identifier}' in file {json_file}")

            except (ValueError, json.JSONDecodeError) as e:
                print(f"Warning: Error processing JSON file at {json_file}: {str(e)}")

    return corrosion_measurements