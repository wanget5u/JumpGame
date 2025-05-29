class EndWall:
    def __init__(self,
                 x: int, y: int,
                 color: tuple[int, int, int]):

        assert isinstance(x, int) and isinstance(y, int), "x i y muszą być liczbami całkowitymi"
        assert isinstance(color, tuple) and len(color) == 3 and all(isinstance(c, int) and 0 <= c <= 255 for c in color), "color musi być krotką 3 liczb całkowitych z zakresu 0-255"