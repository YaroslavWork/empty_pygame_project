class UI:
    """
    Manager of the UI layer.
    This class is the only place that updates UI elements, gives them the input
    events, draws them and clears their one-frame input state. A developer adds a
    new UI element with add().
    """

    def __init__(self) -> None:
        self.elements = []

    def add(self, element) -> None:
        self.elements.append(element)

    def update(self, mouse_pos) -> None:
        for element in self.elements:
            element.update(mouse_pos)

    def handle_input(self, event) -> None:
        for element in self.elements:
            element.handle_input(event)

    def draw(self, screen) -> None:
        for element in self.elements:
            element.draw(screen)

    def reset(self) -> None:
        for element in self.elements:
            element.reset()
