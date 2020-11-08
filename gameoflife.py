class GameOfLife:

    def __init__(self, tab_height, tab_width):
        # 2 Arrays: "self.tab" is main frame and "evo" is used for evolution comput.
        self.tab_height = tab_height
        self.tab_width = tab_width

        self.tab = [[0 for j in range(self.tab_width)] for i in range(self.tab_height)]
        self.evo = self.tab[:]

    def _start_pos(self, shape):
        for pos in shape:
            self.tab[pos[0]][pos[1]] = 1

    def _print_tab(self):
        print("000000000011111111112222222222333333333344444444445")
        print("012345678901234567890123456789012345678901234567890")
        for i, row in enumerate(self.tab):
            print(f"{''.join([str(cell) for cell in row])} {i}")

    def _neighbour(self, i, j):
        # Relative position around cell in arg.
        neighbourhood = [(i-1, j-1), (i-1, j), (i-1, j+1),(i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)]
        neighbors = [pos for pos in neighbourhood if (pos[0]>=0 and pos[0]<n) and (pos[1]>=0 and pos[1]<p)]
        # alive neighbours
        neighborsA = [pos for pos in neighbors if self.tab[pos[0]][pos[1]] == 1]
        # deade neighbours
        neighborsD = [pos for pos in neighbors if self.tab[pos[0]][pos[1]] == 0]

        return (neighborsA, neighborsD)

    def evolution(self, cells):
        alive_cell = []
        empty_cell = []
        for pos in cells:
            i = pos[0]
            j = pos[1]
            cell_neighbors = self._neighbour(i, j)

            alive_cell.extend(cell_neighbors[0])
            empty_cell.extend(cell_neighbors[1])

        skip_cell = []
        for cell in cells:
            if cell in skip_cell:
                continue

            skip_cell.append(cell)
            if not (1 < alive_cell.count(cell) < 4):
                self.tab[cell[0]][cell[1]] = 0
                for i in range(alive_cell.count(cell)):
                    alive_cell.remove(cell)

        for cell in empty_cell:
            if cell in skip_cell:
                continue

            skip_cell.append(cell)
            if empty_cell.count(cell) == 3:
                self.tab[cell[0]][cell[1]] = 1
                alive_cell.append(cell)

        cells = list((set(alive_cell)))
        return cells


SHAPES = {
    "clear": [],
    "blinker": [(10, 22), (10, 23), (10, 24)],
    "row10": [(10, 18), (10, 19), (10, 20), (10, 21), (10, 22), (10, 23), (10, 24), (10, 25), (10, 26), (10, 27)],
    "ship": [(18, 3), (18, 4), (18, 5), (19,5), (20,4)]
}

if __name__ == "__main__":
    from time import sleep, time
    # Array scale:
    n = 21
    p = 51

    gof = GameOfLife(n,p)

    # Animation settings.
    rate = 0.19  # Durée d'attente entre les frames.
    frame = 170  # Nombre de frames a calculer.
    # Set a start postion and init cells list.
    gof._start_pos(SHAPES["row10"])
    cells = SHAPES["row10"]

    # Run animation.
    print(f"\nFrame: 0 -------------------------------------")
    gof._print_tab()
    start = time()
    for i in range(frame):
        print(f"\nFrame: {i+1} -------------------------------------")
        cells = gof.evolution(cells)
        gof._print_tab()
        # sleep(rate)

    fin = time()
    print(f"{frame} frames simulées en {fin - start} secondes")