import os
import json
import csv
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import numpy as np

from .creator import Creator
from .file import File


class Measurement:
    """Class representing the details of a measurement extracted from a JSON file."""

    KEY_TITLE = 'title'
    KEY_IDENTIFIER = 'identifier'
    KEY_DESCRIPTION = 'description'
    KEY_SPECIAL_NOTES = 'special notes'
    KEY_LINKS = 'links'
    KEY_RECORD_TO = 'record_to'
    KEY_EXTRAS = 'extras'
    KEY_PARAMETERS = 'Parameters'
    KEY_TAGS = 'tags'
    KEY_FILES = 'files'
    MEASUREMENT_DIR='../data/tables/'

    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path
        self.name: str = ''
        self.kadi_identifier: str = ''
        self.description: str = ''
        self.special_note: Optional[str] = None
        self.parameters: List[Dict[str, Any]] = []  # Parameters as a list of dictionaries
        self.files: List[File] = []
        self.tags: List[str] = []
        self.created_at: Optional[datetime] = None
        self.creator: Optional[Creator] = None
        self.last_modified: Optional[datetime] = None
        self.record_to: Dict[str, Any] = {}  # Record_to stored as a dictionary
        self.data: Dict[str, Any] = {}  # Store processed data from valid files

        self._load_and_extract_details()
        self._process_files()  # Process the files after extraction

    def _load_and_extract_details(self) -> None:
        """Loads the JSON file and extracts measurement details."""
        data = self._load_json_file()
        self._extract_details(data)

    def _load_json_file(self) -> Dict[str, Any]:
        """Loads a JSON file and returns its content as a dictionary."""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading JSON file at {self.json_file_path}: {str(e)}") from e

    def _extract_details(self, data: Dict[str, Any]) -> None:
        """Extracts measurement details from a JSON object and sets them as class attributes."""
        self.name = data.get(self.KEY_TITLE, '')
        self.kadi_identifier = data.get(self.KEY_IDENTIFIER, '')
        self.description = data.get(self.KEY_DESCRIPTION, '')
        self.special_note = data.get(self.KEY_SPECIAL_NOTES)
        self.created_at = datetime.fromisoformat(data.get('created_at'))
        self.creator = Creator(**data['creator'])
        self.last_modified = datetime.fromisoformat(data.get('last_modified'))
        self.tags = data.get(self.KEY_TAGS, [])

        # Extract files and convert them into File objects
        self.files = [File(**file_data) for file_data in data.get(self.KEY_FILES, [])]

        # Extract parameters from the extras section
        for extra in data.get(self.KEY_EXTRAS, []):
            if extra.get('key') == self.KEY_PARAMETERS:
                self.parameters = extra.get('value', [])

        # Extract record_to information from links
        if data.get(self.KEY_LINKS):
            link = data[self.KEY_LINKS][0].get(self.KEY_RECORD_TO)
            if link:
                self.record_to = {
                    "identifier": link.get('identifier', ''),
                    "title": link.get('title', ''),
                    "doi": next((item['value'] for item in link.get('extras', []) if item.get('key') == 'doi'), ''),
                    "journal_name": next(
                        (item['value'] for item in link.get('extras', []) if item.get('key') == 'journalName'), '')
                }

    def _process_files(self) -> None:
        """
        Processes valid files (those starting with 'Units') and loads the data into self.data.
        """
        for file in self.files:
            try:
                # Construct the full file path using the measurement directory and the file name
                file_path = os.path.join(self.MEASUREMENT_DIR, file.name)

                # Load and process the file
                file_data = self._load_file(file_path)
                if file_data:
                    self.data[file.name] = file_data
            except Exception as e:
                print(f"Error processing file {file.name}: {str(e)}")

    def _load_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Loads the file if it starts with 'Units' and processes the data."""
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)

                # Check if the second row starts with 'Units'
                if len(rows) < 2 or 'Units' not in rows[1][0]:
                    print(f"File {file_path} is not valid (no 'Units' in second row). Skipping.")
                    return None

                # Extract the units and data
                headers = rows[0]  # First row contains headers like 'time', 'weightloss_NaclX'
                units = rows[1]  # Second row contains units like 'h', 'mg', etc.
                data_rows = rows[2:]  # Data starts from the third row

                # Process time and weight loss data
                time = []
                weight_losses = {header: [] for header in headers[1:]}

                for row in data_rows:
                    time.append(float(row[0]))  # First column is time
                    for idx, header in enumerate(headers[1:], start=1):
                        weight_losses[header].append(float(row[idx]))

                return {
                    "headers": headers,
                    "units": units,
                    "time": time,
                    "weight_losses": weight_losses
                }

        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
            return None

    def display_details(self) -> None:
        """Prints the measurement details."""
        print(f"Name: {self.name}")
        print(f"Kadi Identifier: {self.kadi_identifier}")
        print(f"Description: {self.description}")
        print(f"Special Note: {self.special_note}")
        print(f"Created At: {self.created_at}")
        print(f"Creator: {self.creator}")
        print(f"Last Modified: {self.last_modified}")
        print(f"Tags: {', '.join(self.tags)}")
        print("Parameters:")
        for param in self.parameters:
            print(f"  - {param}")
        print("Files:")
        for file in self.files:
            print(f"  - {file}")
        print(f"Record To: {self.record_to}")
        print("Data:")
        for key, value in self.data.items():
            print(f"  - File: {key}")
            print(f"    Time: {value['time']}")
            for header, weight_loss in value['weight_losses'].items():
                print(f"    {header}: {weight_loss}")

    def get_measurement_data_for_plot(self) -> List[Dict[str, Any]]:
        """
        Returns the data from the valid files in a structure that is compatible with the generate_plot function.

        Each entry in the returned list will contain:
        - 'name': The name of the weight loss column (e.g., 'weightloss_Nacl0').
        - 'data': A NumPy array with two columns (time, weight loss).
        - 'x_axis_label': The x-axis label (assumed to be 'Time [hours]').
        - 'y_axis_label': The y-axis label (assumed to be 'Mass loss [mg]').
        """
        measurements = []

        # If no valid files were processed, return an empty list
        if not self.data:
            return measurements

        # Iterate over the processed data from valid files
        for file_name, file_data in self.data.items():
            time_values = np.array(file_data['time'])  # Convert time to a NumPy array

            # For each weight loss column (e.g., weightloss_Nacl0, weightloss_Nacl2, etc.)
            for header, weight_loss in file_data['weight_losses'].items():
                weight_loss_values = np.array(weight_loss)  # Convert weight loss values to a NumPy array

                # Combine time and weight loss into a 2D array
                data_matrix = np.column_stack((time_values, weight_loss_values))

                # Create a dictionary entry for this measurement
                measurements.append({
                    'name': header,
                    'data': data_matrix,
                    'x_axis_label': 'Time [hours]',  # Assuming the time is in hours based on the example file
                    'y_axis_label': 'Mass loss [mg]'  # Assuming the weight loss is in mg based on the example file
                })

        return measurements


def load_measurements_from_directory(directory_paths: Union[str, List[str]]) -> List[Measurement]:
    """Loads all measurements from JSON files in the specified directory or directories.

    Args:
        directory_paths (Union[str, List[str]]): A single directory path or a list of directory paths.

    Returns:
        List[Measurement]: A list of Measurement instances loaded from the JSON files in the specified directory or directories.

    Raises:
        ValueError: If a directory does not exist or no JSON files are found.
    """
    if isinstance(directory_paths, str):
        directory_paths = [directory_paths]  # Convert to a list for uniform processing

    measurements = []
    for directory_path in directory_paths:
        if not os.path.isdir(directory_path):
            raise ValueError(f"The specified directory does not exist: {directory_path}")

        json_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.json')]
        if not json_files:
            raise ValueError(f"No JSON files found in the specified directory: {directory_path}")

        for json_file in json_files:
            try:
                measurement = Measurement(json_file)
                measurements.append(measurement)
            except ValueError as e:
                print(f"Warning: {e}")

    return measurements