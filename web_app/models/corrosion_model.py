import numpy as np
import pandas as pd

from web_app.models import Model


class corrosion_model:
    def __init__(self):
        self.article_identifier = 'parent class'
        self.model_name = 'parent class'


    def eval_material_loss(self):
        pass


    def get_model_name(self):
        return self.model_name



class CorrosionProcessTypeError(Exception):
    """Custom exception for invalid corrosion process type."""
    pass


def get_corrosion_process_type(model: Model) -> str:
    """Determines the corrosion process type based on the tags in a model.

    Args:
        model (Model): The model instance to check.

    Returns:
        str: The corrosion process type, either 'immersion corrosion' or 'atmospheric corrosion'.

    Raises:
        CorrosionProcessTypeError: If both or none of the tags are present.
    """
    has_immersion_corrosion = 'immersion corrosion model' in model.tags
    has_atmospheric_corrosion = 'atmospheric corrosion model' in model.tags

    if has_immersion_corrosion and has_atmospheric_corrosion:
        raise CorrosionProcessTypeError("Model has both 'immersion corrosion' and 'atmospheric corrosion' tags.")
    elif has_immersion_corrosion:
        return 'immersion corrosion'
    elif has_atmospheric_corrosion:
        return 'atmospheric corrosion'
    else:
        raise CorrosionProcessTypeError("Model does not have any valid corrosion process tags.")