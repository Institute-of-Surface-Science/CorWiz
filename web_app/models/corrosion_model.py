from .model import Model
from typing import List, Dict, Union, Tuple


class CorrosionModel:
    """
    A base class for corrosion models.

    This class serves as a template for specific corrosion models, providing basic attributes
    and methods that can be overridden by subclasses.

    Attributes:
        article_identifier (str): Identifier for the article or dataset used by the model.
        model_name (str): The name of the corrosion model.
    """

    def __init__(self, article_identifier: str = 'parent class', model_name: str = 'parent class'):
        """
        Initializes the base corrosion model with default or specified article identifier and model name.

        Args:
            article_identifier (str): Identifier for the article or dataset used by the model. Defaults to 'parent class'.
            model_name (str): The name of the corrosion model. Defaults to 'parent class'.
        """
        self.article_identifier = article_identifier
        self.model_name = model_name

    def eval_material_loss(self, *args, **kwargs):
        """
        Placeholder method for evaluating material loss.

        This method should be overridden by subclasses to provide specific implementations.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_model_name(self) -> str:
        """
        Returns the name of the corrosion model.

        Returns:
            str: The name of the model.
        """
        return self.model_name




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