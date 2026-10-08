from scripts.UI.element import UIElement


# Class UIGroup - a container that groups UI elements (it is itself a UIElement, so
# the UI manager can hold it like any other element). Setting its visible state
# (hide() / show() / visible = ...) applies to every element in the group at once.
class UIGroup(UIElement):
    def __init__(self) -> None:
        self.elements = []
        self._visible = True

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value) -> None:
        self._visible = value
        for element in self.elements:
            element.visible = value

    def add(self, element) -> None:
        element.visible = self._visible
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
