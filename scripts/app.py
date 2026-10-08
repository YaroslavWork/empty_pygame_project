import pygame

import scripts.settings as s
from scripts.camera import CameraModel, CameraView
from scripts.field import FieldModel, FieldView
from scripts.UI.button import Button
from scripts.UI.input_field import InputField
from scripts.UI.text import TextView
from scripts.UI.ui import UI

class App:

    def __init__(self) -> None:
        # Initialize pygame and settings
        pygame.init()

        self.size = self.width, self.height = s.SIZE
        self.name = s.NAME
        self.colors = s.COLORS
        self.fps = s.FPS

        # Set pygame window
        pygame.display.set_caption(self.name)

        # Set pygame clock
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        # Set input variables
        self.dt = 0
        self.mouse_pos = (0, 0)
        self.keys = []

        # Set model variables
        self.camera_model = CameraModel(x=0, y=0, distance=10, resolution=self.size)
        self.field_model = FieldModel()

        # Set view variables
        self.camera_view = CameraView(self.camera_model)
        self.field_view = FieldView(self.field_model)

        # Set UI variables
        self.ui = UI()

        # ALL THIS SECTION BELOW IS JUST AN EXAMPLE OF HOW TO USE THE UI SYSTEM
        self.button = Button("Hide FPS", (20, 20), (120, 50))
        self.fps_text = TextView("FPS: 0", (0, 0, 0), 20,
                                 pos=(self.width - 70, self.height - 21), center=False)
        self.ui.add(self.button)
        self.ui.add(self.fps_text)

        # INPUT FIELD EXAMPLE: click the box, type a name and press Enter.
        # The label under the box mirrors the content, the caption shows it on Enter.
        self.name_field = InputField((20, 90), (220, 40), placeholder="Type your name")
        self.name_text = TextView("Hello!", (0, 0, 0), 24, pos=(20, 150), center=False)
        self.ui.add(self.name_field)
        self.ui.add(self.name_text)

    def update(self) -> None:
        """
        Main update function of the program.
        This function is called every frame
        """
        self.handle_input()  # -*-*- Input Block -*-*-
        self.update_physics()  # -*-*- Physics Block -*-*-
        self.render()  # -*-*- Rendering Block -*-*-
        self.update_display()  # -*-*- Update Block -*-*-

    def handle_input(self) -> None:
        """
        Input block.
        Reads the mouse, events and keyboard, collects the input.
        """
        self.mouse_pos = pygame.mouse.get_pos()  # Get mouse position

        for event in pygame.event.get():  # Get all events
            if event.type == pygame.QUIT:  # If you want to close the program...
                TextView.fonts = {}  # Clear fonts
                close()

            if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse button down...
                if event.button == 1:
                    self.ui.handle_input(event)
                elif event.button == 3:
                    pass

            if event.type == pygame.MOUSEBUTTONUP:  # If mouse button up...
                if event.button == 1:
                    self.ui.handle_input(event)

            if event.type == pygame.TEXTINPUT:  # If a character was typed...
                self.ui.handle_input(event)  # Give it to the UI (used by InputField)

            if event.type == pygame.KEYDOWN:  # If key button down...
                if event.key == pygame.K_SPACE:
                    pass
                else:
                    self.ui.handle_input(event)  # Give it to the UI (used by InputField)

        self.keys = pygame.key.get_pressed()  # Get all keys (pressed or not)

    def update_physics(self) -> None:
        """
        Physics block.
        Calculate model from *Model classes.
        """

        ### CAMERA MOVEMENT EXAMPLE: Move camera with arrow keys or WASD
        if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
            self.camera_model.move_left(1, self.dt)
        if self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
            self.camera_model.move_right(1, self.dt)
        if self.keys[pygame.K_UP] or self.keys[pygame.K_w]:
            self.camera_model.move_up(1, self.dt)
        if self.keys[pygame.K_DOWN] or self.keys[pygame.K_s]:
            self.camera_model.move_down(1, self.dt)
        if self.keys[pygame.K_e]:
            self.camera_model.scale_in(1, self.dt)
        if self.keys[pygame.K_q]:
            self.camera_model.scale_out(1, self.dt)

        self.fps_text.set_text("FPS: " + str(int(self.clock.get_fps()))) # FPS TEXT EXAMPLE: Update FPS text

        self.ui.update(self.mouse_pos)

        if self.button.clicked:  # BUTTON EXAMPLE: Hide fps text button
            if self.fps_text.visible:
                self.fps_text.hide()
                self.button.set_text("Show FPS")
            else:
                self.fps_text.show()
                self.button.set_text("Hide FPS")

        # INPUT FIELD EXAMPLE: show the typed content in the label under the box...
        typed_text = self.name_field.get_text()  # Read what the user typed inside
        if typed_text:
            self.name_text.set_text("Hello, " + typed_text + "!")
        else:
            self.name_text.set_text("Hello!")

        if self.name_field.submitted:  # INPUT FIELD EXAMPLE: Enter shows it in the caption
            pygame.display.set_caption(self.name + " - " + typed_text)

    def render(self) -> None:
        """
        Rendering block.
        Draws the current model state with help of *View classes.
        """
        self.screen.fill(self.colors['background'])  # Fill background

        self.field_view.draw(self.screen, self.camera_model)

        self.ui.draw(self.screen)  # Draw UI

        self.camera_view.draw_map_scale(self.screen, offset=(140, 15))  # MAP SCALE EXAMPLE: Draw map scale in top left corner

    def update_display(self) -> None:
        """
        Update block.
        Flips the display and updates the delta time.
        """
        self.ui.reset()

        pygame.display.update()

        self.dt = self.clock.tick(self.fps)


def close():
    pygame.quit()
    exit()
