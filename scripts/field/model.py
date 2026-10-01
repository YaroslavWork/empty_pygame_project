class FieldModel:
    """
    Data model of the field.
    This class holds only the state of the game world (no pygame, no drawing).
    """

    def __init__(self) -> None:
        pass

    def to_dict(self) -> dict:
        """
        This function convert field state to a plain dict (for network/save).
        :return: Field state as a dict
        """
        return {}

    def from_dict(self, data) -> None:
        """
        This function restore field state from a plain dict.
        :param data: Field state as a dict
        :return: None
        """
        pass

