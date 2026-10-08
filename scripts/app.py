import pygame

import scripts.settings as s
from scripts.camera import CameraModel, CameraView
from scripts.field import FieldView
from scripts.net.client import Client, LocalClient
from scripts.UI.button import Button
from scripts.UI.input_field import InputField
from scripts.UI.text import TextView
from scripts.UI.ui import UI
from scripts.world import WorldModel


class App:

    def __init__(self, client: Client = None) -> None:
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
        self.intents = set()

        # Set model variables
        self.world = WorldModel(camera_model=CameraModel(x=s.CAMERA_START_X, y=s.CAMERA_START_Y,
                                                         distance=s.CAMERA_START_DISTANCE, resolution=self.size))
        self.camera_model = self.world.camera_model
        self.field_model = self.world.field_model

        # Set client (singleplayer uses an in-process world)
        self.client = client or LocalClient(self.world)

        # Set view variables
        self.camera_view = CameraView(self.camera_model)
        self.field_view = FieldView(self.field_model)

        # Set UI variables
        self.ui = UI()

        # ALL THIS SECTION BELOW IS JUST AN EXAMPLE OF HOW TO USE THE UI SYSTEM
        self.button = Button("Hide FPS", s.UI_BUTTON_POS, s.UI_BUTTON_SIZE, size_font=s.UI_FONT_SIZE)
        self.fps_text = TextView("FPS: 0", self.colors['text'], s.HUD_FONT_SIZE,
                                 pos=(self.width - s.HUD_FPS_MARGIN[0], self.height - s.HUD_FPS_MARGIN[1]),
                                 center=False)
        self.ui.add(self.button)
        self.ui.add(self.fps_text)

        # INPUT FIELD EXAMPLE: click the box, type a name and press Enter.
        # The label under the box mirrors the content, the caption shows it on Enter.
        self.name_field = InputField(s.UI_INPUT_POS, s.UI_INPUT_SIZE, placeholder=s.UI_INPUT_PLACEHOLDER,
                                     size_font=s.UI_FONT_SIZE)
        self.name_text = TextView("Hello!", self.colors['text'], s.UI_FONT_SIZE,
                                  pos=s.UI_NAME_TEXT_POS, center=False)
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
        self.intents = self.collect_intents()  # Collect intents from keys

    def collect_intents(self) -> set:
        """
        Input block.
        Converts the pressed keys into a set of input intents.
        """
        intents = set()

        if self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
            intents.add("left")
        if self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
            intents.add("right")
        if self.keys[pygame.K_UP] or self.keys[pygame.K_w]:
            intents.add("up")
        if self.keys[pygame.K_DOWN] or self.keys[pygame.K_s]:
            intents.add("down")
        if self.keys[pygame.K_e]:
            intents.add("zoom_in")
        if self.keys[pygame.K_q]:
            intents.add("zoom_out")

        return intents

    def update_physics(self) -> None:
        """
        Physics block.
        Sends the input intents to the client and applies the received snapshot.
        """
        snapshot = self.client.update(self.dt, self.intents)

        if snapshot is not None:
            self.world.apply_snapshot(snapshot)

        self.fps_text.set_text("FPS: " + str(int(self.clock.get_fps())))  # FPS TEXT EXAMPLE: Update FPS text

        self.ui.update(self.mouse_pos)

        if self.button.clicked:  # BUTTON EXAMPLE: Hide/show fps text button
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

        self.camera_view.draw_map_scale(self.screen, offset=s.HUD_SCALE_OFFSET)  # Draw map scale

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
