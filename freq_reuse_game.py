import tkinter as tk
from tkinter import ttk
from math import cos, sin, sqrt, radians

# https://github.com/noobien/pytk-hexagon-grid
# http://vlabs.iitkgp.ernet.in/fcmc/exp6A/index.html
# https://www.redblobgames.com/grids/hexagons/

class FillHexagon:
    def __init__(self, parent, x, y, length, color, tags):
        self.parent = parent # canvas
        self.x = x           # top left x
        self.y = y           # top left y
        self.length = length # length of a side
        self.color = color   # fill color

        self.selected = False
        self.tags = tags
        
        self.draw()

    def draw(self):
        start_x = self.x
        start_y = self.y
        angle = 60
        coords = []
        for i in range(6):
            end_x = start_x + self.length * cos(radians(angle * i))
            end_y = start_y + self.length * sin(radians(angle * i))
            coords.append([start_x, start_y])
            start_x = end_x
            start_y = end_y
        self.parent.create_polygon(coords[0][0],
                                   coords[0][1], 
                                   coords[1][0], 
                                   coords[1][1],
                                   coords[2][0],
                                   coords[2][1],
                                   coords[3][0],
                                   coords[3][1],
                                   coords[4][0],
                                   coords[4][1], 
                                   coords[5][0],
                                   coords[5][1], 
                                   fill=self.color,
                                   outline="gray",
                                   tags=self.tags)

class FrequencyReuseGame(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Frequency Reuse Game")

        self.rowconfigure(0, minsize=800, weight=1)

        self.columnconfigure(0, minsize=150, weight=1)
        self.columnconfigure(3, minsize=800, weight=1)

        self.hex_frame = tk.Canvas(self, width=300, height=300, bg="#ffffff")
        self.hexagons = []
        self.selected_hexagons = set()

        menu = tk.Frame(self)
        self.first_cell = None

        self.i_entry = tk.Entry(master=menu, width=10)
        i_lbl = tk.Label(master=menu, text="i :", width=2)

        self.j_entry = tk.Entry(master=menu, width=10)
        j_lbl = tk.Label(master=menu, text="j :", width=2)

        i_lbl.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.i_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        j_lbl.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.j_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        self.n_lbl = tk.Label(master=menu, text="N :")
        self.n_lbl.grid(row=2, column=0, columnspan=2)

        self.start_btn = tk.Button(menu, text="Start", width=10, command=self.start)
        self.reset_btn = tk.Button(menu, state="disabled", text="Reset", width=10, command=self.reset)
        self.end_btn = tk.Button(menu, state="disabled", text="Finish", width=10, command=self.end)

        self.start_btn.grid(row=3, column=0, sticky="n", padx=5, pady=5, columnspan=2)
        self.reset_btn.grid(row=4, column=0, sticky="n", padx=5, pady=5, columnspan=2)
        self.end_btn.grid(row=5, column=0, sticky="n", padx=5, pady=5, columnspan=2)

        self.res_lbl = tk.Label(master=menu, text="")
        self.res_lbl.grid(row=6, column=0, columnspan=2)

        sep = ttk.Separator(orient=tk.VERTICAL)

        self.initGrid(25, 25, 40, debug=False)

        menu.grid(row=0, column=0, sticky="ns", pady=20)
        sep.grid(row=0, column=2, sticky="ns")
        self.hex_frame.grid(row=0, column=3, sticky="nsew")

    def initGrid(self, cols, rows, size, debug):
        """
        2d grid of hexagons
        """
        for c in range(cols):
            if c % 2 == 0:
                offset = size * sqrt(3) / 2
            else:
                offset = 0
            for r in range(rows):
                if debug :
                    coords = "{}, {}".format(c, 2*r if c%2==0 else 2*r-1)
                    self.hex_frame.create_text(c*(size*1.5) + (size/2), (r*(size*sqrt(3))) + offset + (size/2), text=coords)

                h = FillHexagon(self.hex_frame, c*(size*1.5), (r*(size*sqrt(3))) + offset, size, "#ffffff", "{}.{}".format(c, 2*r if c%2==0 else 2*r-1))
                self.hexagons.append(h)

    def click(self, evt):
        x, y = evt.x, evt.y

        clicked = self.hex_frame.find_closest(x, y)[0] # find closest

        if not self.first_cell:
            self.hex_frame.itemconfigure(self.hexagons[int(clicked)-1].tags, fill="pink")
            self.first_cell = self.hexagons[int(clicked)-1].tags

        elif self.first_cell != self.hexagons[int(clicked)-1].tags and not self.hexagons[int(clicked)-1].selected:
            self.hexagons[int(clicked)-1].selected = True
            self.hex_frame.itemconfigure(self.hexagons[int(clicked)-1].tags, fill="orange")
            self.selected_hexagons.add(self.hexagons[int(clicked)-1].tags)

    def reset(self):
        for i in self.hexagons:
            self.hex_frame.itemconfigure(i.tags, fill=i.color)
            i.selected = False
        self.first_cell = None
        self.reset_btn["state"] = "active"
        self.end_btn["state"] = "active"
        self.start_btn["state"] = "disabled"
        self.points = 0
        self.res_lbl["text"] = ""
        self.i_entry["state"] = "readonly"
        self.j_entry["state"] = "readonly"

    def calculate_n(self):
        i = int(self.i_entry.get()) if self.i_entry.get() != "" else 0
        j = int(self.j_entry.get()) if self.j_entry.get() != "" else 0
        n = i**2 + j**2 + i*j

        self.n_lbl["text"] = f"N : {n}"

    def update_points(self):
        self.res_lbl["text"] = f"Points : {self.points}/30"
        
    def start(self):
        self.calculate_n()
        self.reset()
        self.selected_hexagons = set()
        self.hex_frame.bind("<Button-1>", self.click)

    def end(self):
        self.reset_btn["state"] = "disabled"
        self.end_btn["state"] = "disabled"
        self.start_btn["state"] = "active"
        self.i_entry["state"] = "normal"
        self.j_entry["state"] = "normal"

        if self.first_cell:
            self.find_cells()
        self.update_points()
        self.hex_frame.unbind("<Button-1>")

    def find_cells(self):
        i = int(self.i_entry.get()) if self.i_entry.get() != "" else 0
        j = int(self.j_entry.get()) if self.j_entry.get() != "" else 0

        f_x, f_y = map(int, self.first_cell.split("."))
        self.hex_frame.itemconfigure(self.first_cell, fill="green")

        # the tags for each hexagon store their doubled coordinates in the grid. Thus we can easily find the neighbours
        # of a given cell, and traverse to the co channel cell by following the given offsets:
        #          x,y-2 
        # x-1,y-1         x+1,y-1
        #          x, y
        # x-1,y+1         x+1,y+1
        #          x,y+2
        cells = [f"{f_x-j}.{f_y-2*i-j}", f"{f_x-i-j}.{f_y-i+j}", f"{f_x-i}.{f_y+i+2*j}", f"{f_x+j}.{f_y+2*i+j}", f"{f_x+i+j}.{f_y+i-j}", f"{f_x+i}.{f_y-i-2*j}"]

        for cell in cells:
            self.hex_frame.itemconfigure(cell, fill="blue")
        for cell in self.selected_hexagons:
            if cell in cells:
                self.hex_frame.itemconfigure(cell, fill="green")
                self.points += 5
            else:
                self.hex_frame.itemconfigure(cell, fill="red")
                self.points -= 1


if __name__=="__main__":
    window = FrequencyReuseGame()
    window.mainloop()