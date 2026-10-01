class CameraModel:
    """
    Data model of the camera.
    This class holds only the state and the math (no pygame, no drawing).
    It represents where the camera looks and how the world is scaled.
    """

    def __init__(self, x, y, distance, resolution=(640, 480)) -> None:
        self.x = x
        self.y = y
        self.distance = distance  # Distance for width (in meters)
        self.resolution = resolution

    def get_local_point(self, global_x, global_y) -> tuple:
        """
        This function convert global coordinates to local coordinates
        :param global_x: X coordinate in global coordinates
        :param global_y: Y coordinate in global coordinates
        :return: Local coordinates (x, y)
        """
        local_x = (global_x - self.x) * self.resolution[0] / self.distance
        local_y = (global_y - self.y) * self.resolution[0] / self.distance

        return local_x, local_y

    def get_global_point(self, local_x, local_y) -> tuple:
        """
        This function convert local coordinates to global coordinates
        :param local_x: X coordinate in local coordinates
        :param local_y: Y coordinate in local coordinates
        :return: Global coordinates (x, y)
        """
        global_x = local_x / self.resolution[0] * self.distance + self.x
        global_y = local_y / self.resolution[0] * self.distance + self.y

        return global_x, global_y

    def get_local_radius(self, r) -> float:
        """
        This function convert global radius to local radius
        :param r: Radius in global coordinates
        :return: Radius in local coordinates
        """
        return r * self.resolution[0] / self.distance

    def get_global_radius(self, r) -> float:
        """
        This function convert local radius to global radius
        :param r: Radius in local coordinates
        :return: Radius in global coordinates
        """
        return r * self.distance / self.resolution[0]

    def move_left(self, speed, dt) -> None:
        """
        This function move camera to the left side
        :param speed: The speed of a camera
        :param dt: Delta time
        :return: None
        """
        self.x -= speed * self.distance * dt / 1000

    def move_right(self, speed, dt) -> None:
        """
        This function move camera to the right side
        :param speed: The speed of a camera
        :param dt: Delta time
        :return: None
        """
        self.x += speed * self.distance * dt / 1000

    def move_up(self, speed, dt) -> None:
        """
        This function move camera to the up
        :param speed: The speed of a camera
        :param dt: Delta time
        :return: None
        """
        self.y -= speed * self.distance * dt / 1000

    def move_down(self, speed, dt) -> None:
        """
        This function move camera to the down
        :param speed: The speed of a camera
        :param dt: Delta time
        :return: None
        """
        self.y += speed * self.distance * dt / 1000

    def scale_in(self, speed_scale, dt) -> None:
        """
        This function change scale in the map
        :param speed_scale: The speed of a scale
        :param dt: Delta time
        :return: None
        """
        self.distance += self.distance * speed_scale * dt / 1000

    def scale_out(self, speed_scale, dt) -> None:
        """
        This function change scales out the map
        :param speed_scale: The speed of a scale
        :param dt: Delta time
        :return: None
        """
        self.distance -= self.distance * speed_scale * dt / 1000
