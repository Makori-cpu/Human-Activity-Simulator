
class MouseController:

    def __init__(self, canvas):
        self.canvas = canvas
        self.pointer = None

    def move_pointer(self, target_x, target_y):

        if self.pointer is None:
            self.pointer = self.canvas.create_oval(
                10, 10, 24, 24,
                fill="#00d4aa",
                outline=""
            )

        self.canvas.coords(
            self.pointer,
            target_x - 7,
            target_y - 7,
            target_x + 7,
            target_y + 7
        )

    def click_position(self, x, y):

        self.move_pointer(x, y)

        self.canvas.create_oval(
            x - 12, y - 12,
            x + 12, y + 12,
            outline="#f0b429",
            width=2
        )
