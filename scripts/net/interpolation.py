from scripts import settings as s


def lerp(a, b, alpha) -> float:
    """
    This function linearly interpolate between two numbers.
    :param a: Value at alpha 0
    :param b: Value at alpha 1
    :param alpha: Blend factor between 0 and 1
    :return: The interpolated value
    """
    return a + (b - a) * alpha


def blend(previous, current, alpha):
    """
    This function merge two snapshots into one rendered frame.
    Dicts are merged recursively, numbers are interpolated, everything else
    (strings, bools, lists like the camera resolution) is taken from current
    so discrete data is never corrupted by the blend.
    :param previous: The older snapshot (or a value from it)
    :param current: The newer snapshot (or a value from it)
    :param alpha: Blend factor between 0 (previous) and 1 (current)
    :return: The blended value
    """
    if isinstance(previous, dict) and isinstance(current, dict):
        return {key: blend(previous.get(key), current[key], alpha) for key in current}

    if isinstance(current, bool) or not isinstance(current, (int, float)):
        return current

    if not isinstance(previous, (int, float)) or isinstance(previous, bool):
        return current

    return lerp(previous, current, alpha)


class SnapshotBuffer:
    """
    Holds the last two snapshots and samples a frame between them.
    A new snapshot restarts the clock, so the sampled frame glides from the
    previous snapshot to the current one over interval_ms.
    This class holds only the math (no pygame, no drawing).
    """

    def __init__(self, interval_ms=s.NET_INTERP_MS) -> None:
        self.interval_ms = interval_ms
        self.previous = None
        self.current = None
        self.elapsed = 0.0

    def push(self, snapshot) -> None:
        """
        This function register a newly received snapshot and restart the clock.
        :param snapshot: The latest world state as a dict
        :return: None
        """
        if self.current is not None:
            self.previous = self.current
        self.current = snapshot
        self.elapsed = 0.0

    def advance(self, dt) -> None:
        """
        This function advance the clock by dt.
        :param dt: Delta time
        :return: None
        """
        self.elapsed += dt

    @property
    def alpha(self) -> float:
        if self.interval_ms <= 0:
            return 1.0

        return min(1.0, self.elapsed / self.interval_ms)

    def sample(self):
        """
        This function return the snapshot to render for the current clock.
        :return: The blended world state as a dict (or None before the first snapshot)
        """
        if self.current is None:
            return None

        if self.previous is None:
            return self.current

        return blend(self.previous, self.current, self.alpha)
