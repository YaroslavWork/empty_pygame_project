import pygame

import scripts.settings as s
from scripts.camera import CameraModel, CameraView
from scripts.field import FieldView
from scripts.net.client import Client, LocalClient
from scripts.player import PlayerView
from scripts.UI.text import TextView
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

        # Singleplayer owns one local player; multiplayer receives players via snapshots
        if isinstance(self.client, LocalClient):
            self.world.add_player("0")

        # Set view variables
        self.camera_view = CameraView(self.camera_model)
        self.field_view = FieldView(self.field_model)
        self.player_views = {}

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
                    pass
                elif event.button == 3:
                    pass

            if event.type == pygame.KEYDOWN:  # If key button down...
                if event.key == pygame.K_SPACE:
                    pass

        self.keys = pygame.key.get_pressed()  # Get all keys (pressed or not)
        self.intents = self.collect_intents()  # Collect intents from keys

    def collect_intents(self) -> set:
        """
        Input block.
        Converts the pressed keys into a set of input intents.
        WASD moves the player, Q/E zoom the camera.
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
            self.camera_model.resolution = tuple(self.size)  # Keep the local window resolution

    def render(self) -> None:
        """
        Rendering block.
        Draws the current model state with help of *View classes.
        """
        self.screen.fill(self.colors['background'])  # Fill background

        self.field_view.draw(self.screen, self.camera_model)
        self.draw_players()

        self.camera_view.draw_map_scale(self.screen, offset=s.HUD_SCALE_OFFSET)  # Draw map scale
        fps_text = "FPS: " + str(int(self.clock.get_fps()))
        TextView(fps_text, self.colors['text'], s.HUD_FONT_SIZE).print(
            self.screen,
            (self.width - s.HUD_FPS_MARGIN[0], self.height - s.HUD_FPS_MARGIN[1]),
            False)  # FPS counter

    def draw_players(self) -> None:
        """
        Rendering block.
        Synchronizes player views with the world players and draws each of them.
        """
        for player_id in list(self.player_views):
            if player_id not in self.world.players:
                del self.player_views[player_id]

        for player_id, player_model in self.world.players.items():
            if player_id not in self.player_views:
                self.player_views[player_id] = PlayerView(player_model)

            self.player_views[player_id].draw(self.screen, self.camera_model)

    def update_display(self) -> None:
        """
        Update block.
        Flips the display and updates the delta time.
        """
        pygame.display.update()

        self.dt = self.clock.tick(self.fps)


def close():
    pygame.quit()
    exit()
