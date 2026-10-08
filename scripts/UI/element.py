class UIElement:
    """
    Base interface of a UI element.
    The UI manager drives every element through these methods, so a new
    UI element only has to inherit from this class and implement them.
    Every element also carries a shared visible flag (hide() / show()): a hidden
    element draws nothing and must not react to input.
    """

    visible = True

    def hide(self) -> None:
        self.visible = False

    def show(self) -> None:
        self.visible = True

    def update(self, mouse_pos) -> None:
        pass

    def handle_input(self, event) -> None:
        pass

    def draw(self, screen) -> None:
        pass

    def reset(self) -> None:
        pass
