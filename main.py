import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox
from tkinter import filedialog
from fit import Fit
from PIL import ImageGrab
import webbrowser

# Some constants
APP_NAME = 'ISO Fits & Tolerances'
ICON_PATH = 'icon.ico'
MY_FONT = ('Comic Sans MS', 10)
MY_FONT_BOLD = ('Comic Sans MS', 11, 'bold')
BLUE = '#264653'
GREEN = '#2a9d8f'
YELLOW = '#e9c46a'
ORANGE = '#f4a261'
RED = '#e76f51'
CANVAS_WIDTH = 200
CANVAS_HEIGHT = 400
GITHUB_LINK = 'https://github.com/georgievm/py-tkinter-iso-fits'


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self['bg'] = BLUE
        self.title(APP_NAME)
        self.iconbitmap(ICON_PATH)
        self.resizable(False, False)

        # Common widget params
        btn_kwargs = {'font': MY_FONT, 'bg': GREEN, 'fg': 'white', 'relief': None, 'width': 20}
        lbl_kwargs = {'font': MY_FONT, 'bg': BLUE, 'fg': 'white'}

        left_fr = tk.Frame(self, height=30, bg=BLUE)
        left_fr.pack(side='left', padx=17, anchor='n')

        title_font = Font(left_fr, family='Comic Sans MS', size=18, weight='bold', underline=True, slant='italic')
        lbl_title = tk.Label(left_fr, text='ISO Fits', fg=YELLOW, bg=BLUE, font=title_font)
        lbl_title.pack(side='top', pady=18)

        input_fr = tk.Frame(left_fr, bg=BLUE)
        input_fr.pack(side='top')

        # Size
        lbl_size = tk.Label(input_fr, text='Size (mm):', **lbl_kwargs)
        lbl_size.grid(row=1, column=0, sticky='w')
        global size_var
        size_var = tk.IntVar(value=50)
        size_box = tk.Spinbox(input_fr, from_=3, to=400, textvariable=size_var, width=6, font=MY_FONT)
        size_box.grid(row=1, column=1)

        # Hole Tolerance
        global hole_toler_var
        hole_toler_var = tk.StringVar(value='E6')
        lbl_hole = tk.Label(input_fr, text='Hole Tolerance:', **lbl_kwargs)
        lbl_hole.grid(row=2, column=0, pady=12, sticky='w')
        hole_combo = ttk.Combobox(input_fr, width=5, textvariable=hole_toler_var, font=MY_FONT)
        hole_combo.config(values=Fit.get_hole_toler_lst())
        hole_combo.grid(row=2, column=1)

        # Shaft Tolerance
        global shaft_toler_var
        shaft_toler_var = tk.StringVar(value='e6')
        lbl_shaft = tk.Label(input_fr, text='Shaft Tolerance:  ', **lbl_kwargs)
        lbl_shaft.grid(row=3, column=0)
        shaft_combo = ttk.Combobox(input_fr, width=5, textvariable=shaft_toler_var, font=MY_FONT)
        shaft_combo.config(values=Fit.get_shaft_toler_lst())
        shaft_combo.grid(row=3, column=1)

        # Buttons
        calc_btn = tk.Button(input_fr, text='Calculate', command=self.calculate, **btn_kwargs)
        calc_btn.grid(row=4, column=0, columnspan=2, pady=30)

        view_on_gh_btn = tk.Button(left_fr, text='View on GitHub',
                                   command=lambda: webbrowser.open(GITHUB_LINK))
        view_on_gh_btn.config(**btn_kwargs)
        view_on_gh_btn.pack(side='bottom')

        help_btn = tk.Button(left_fr, text='Help', command=self.view_help, **btn_kwargs)
        help_btn.pack(side='bottom', pady=25)

        self.save_img_btn = tk.Button(left_fr, text='Save Graph', command=self.save_img, state='disabled')
        self.save_img_btn.config(**btn_kwargs)
        self.save_img_btn.pack(side='bottom')

        # Center Area
        center_frame = tk.Frame(self, bg=GREEN)
        center_frame.pack(side='left', pady=20)

        databox_fr = tk.Frame(center_frame, bg=BLUE)
        databox_fr.pack(fill='both', expand=True, padx=7)
        self.databox = tk.Text(databox_fr, width=30, height=19, bg=BLUE, fg=YELLOW, font=MY_FONT_BOLD, bd=0)
        self.databox.insert(1.0, 'Click "Calculate" to see more.')
        self.databox.pack(fill='both', expand=True, padx=20)

        # Canvas
        self.canvas = tk.Canvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=BLUE, bd=0, highlightthickness=0)
        self.canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, text='Graph here', font=MY_FONT_BOLD, fill=YELLOW)
        self.canvas.pack(side='left', padx=15, pady=15)

        # Key binding
        self.bind('<Return>', lambda e: self.calculate())
        self.bind('<Control-s>', lambda e: self.save_img())
        self.bind('<F1>', lambda e: self.view_help())

    def calculate(self):
        # Input data validation
        try:
            size = size_var.get()
        except Exception:
            messagebox.showerror(APP_NAME, 'INVALID Size value!')
            return

        size = size_var.get()
        hole_toler = hole_toler_var.get()
        shaft_toler = shaft_toler_var.get()

        try:
            fit = Fit(size, hole_toler, shaft_toler)
        except Exception as e:
            messagebox.showerror(APP_NAME, e)
            return

        self.fit = fit

        self.save_img_btn['state'] = 'normal'
        self.databox.delete(1.0, 'end')

        # Add fit data to the textbox
        self.databox.insert('end', f'DETAILS FOR {fit.fit_designation}')
        self.databox.insert('end', '\n\n' + '---HOLE---' + '\n')
        self.databox.insert('end', f'Upper Deviation (ES) = {fit.ES} μm\n')
        self.databox.insert('end', f'Lower Deviation (EI) = {fit.EI} μm\n')
        self.databox.insert('end', f'Max. Size = {fit.max_hole_size} mm\n')
        self.databox.insert('end', f'Min. Size = {fit.min_hole_size} mm')

        self.databox.insert('end', '\n\n' + '---SHAFT---' + '\n')
        self.databox.insert('end', f'Upper Deviation (es) = {fit.es} μm\n')
        self.databox.insert('end', f'Lower Deviation (ei) = {fit.ei} μm\n')
        self.databox.insert('end', f'Max. Size = {fit.max_shaft_size} mm\n')
        self.databox.insert('end', f'Min. Size = {fit.min_shaft_size} mm')

        self.databox.insert('end', '\n\n' + '---FIT---' + '\n')
        self.databox.insert('end', f'Type: {fit.fit_type}\n')

        if fit.c_max is not None:
            self.databox.insert('end', f'Max. Clearance = {fit.c_max} μm\n')
        if fit.c_min is not None:
            self.databox.insert('end', f'Min. Clearance = {fit.c_min} μm\n')
        if fit.c_avg is not None:
            self.databox.insert('end', f'Avg. Clearance = {fit.c_avg} μm')

        if fit.i_max is not None:
            self.databox.insert('end', f'Max. Interference = {fit.i_max} μm\n')
        if fit.i_min is not None:
            self.databox.insert('end', f'Min. Interference = {fit.i_min} μm\n')
        if fit.i_avg is not None:
            self.databox.insert('end', f'Avg. Interference = {fit.i_avg} μm')

        if fit.transition is not None:
            self.databox.insert('end', f'Transition = {fit.transition} μm')

        # Draw graph
        self.canvas.delete("all")
        self.draw_graph()

    def draw_graph(self):
        fit = self.fit
        hole_color, shaft_color = ORANGE, RED
        num_font = 'Consolas 11'
        gr_font = 'Consolas 11 bold'
        w, h = CANVAS_WIDTH, CANVAS_HEIGHT
        FONT_GRAPH = Font(self.canvas, family='Comic Sans MS', size=11, weight='bold', underline=True)

        # Canvas - Title
        self.canvas.create_text(w / 2, h / 16, text='GRAPH', fill='white', font=FONT_GRAPH)
        self.canvas.create_text(w / 2, h / 16 + 22, text=f'({self.fit.fit_designation})', fill=YELLOW, font=MY_FONT_BOLD)

        if fit.fit_type == 'Clearance':
            extra = 0 if fit.EI == fit.es else 10
            # rectangles
            self.canvas.create_rectangle(w / 4, h / 4, w / 2, h / 2 - extra, fill=hole_color)
            self.canvas.create_rectangle(w / 2, h / 2 + extra, w / 4 * 3, h / 4 * 3, fill=shaft_color)
            # tolerance grades
            self.canvas.create_text(w / 4 + w / 8, h / 2 - h / 8 - extra / 2, text=fit.hole_toler, font=gr_font)
            self.canvas.create_text(w / 2 + w / 8, h / 2 + h / 8 + extra / 2, text=fit.shaft_toler, font=gr_font)
            # deviations
            self.canvas.create_text(w / 8, h / 4, text=fit.ES, font=num_font, fill='white')
            self.canvas.create_text(w / 8, h / 2 - extra, text=fit.EI, font=num_font, fill='white')
            self.canvas.create_text(w - w / 8, h / 2 + extra, text=fit.es, font=num_font, fill='white')
            self.canvas.create_text(w - w / 8, h / 4 * 3, text=fit.ei, font=num_font, fill='white')
        elif fit.fit_type == 'Interference':
            extra = 0 if fit.ei == fit.ES else 10
            # rectangles
            self.canvas.create_rectangle(w / 4, h / 2 + extra, w / 2, h / 4 * 3, fill=hole_color)
            self.canvas.create_rectangle(w / 2, h / 4, w / 4 * 3, h / 2 - extra, fill=shaft_color)
            # tolerance grades
            self.canvas.create_text(w / 4 + w / 8, h / 2 + h / 8 + extra / 2, text=fit.hole_toler, font=gr_font)
            self.canvas.create_text(w / 2 + w / 8, h / 2 - h / 8 - extra / 2, text=fit.shaft_toler, font=gr_font)
            # deviations
            self.canvas.create_text(w / 8, h / 2 + extra, text=fit.ES, font=num_font, fill='white')
            self.canvas.create_text(w / 8, h / 4 * 3, text=fit.EI, font=num_font, fill='white')
            self.canvas.create_text(w - w / 8, h / 4, text=fit.es, font=num_font, fill='white')
            self.canvas.create_text(w - w / 8, h / 2 - extra, text=fit.ei, font=num_font, fill='white')
        else:  # Transition
            if fit.ES > fit.es and fit.EI < fit.ei:
                # ||
                # ||||
                # ||
                # rectangles
                self.canvas.create_rectangle(w / 4, h / 4, w / 2, h / 4 * 3, fill=hole_color)
                self.canvas.create_rectangle(w / 2, h / 2 - h / 8, w / 4 * 3, h / 2 + h / 8, fill=shaft_color)
                # tolerance grades
                self.canvas.create_text(w / 4 + w / 8, h / 2, text=fit.hole_toler, font=gr_font)
                self.canvas.create_text(w / 2 + w / 8, h / 2, text=fit.shaft_toler, font=gr_font)
                # deviations
                self.canvas.create_text(w / 8, h / 4, text=fit.ES, font=num_font, fill='white')
                self.canvas.create_text(w / 8, h / 4 * 3, text=fit.EI, font=num_font, fill='white')
                self.canvas.create_text(w - w / 8, h / 2 - h / 8, text=fit.es, font=num_font, fill='white')
                self.canvas.create_text(w - w / 8, h / 2 + h / 8, text=fit.ei, font=num_font, fill='white')
            elif fit.ES < fit.es and fit.EI > fit.ei:
                #   ||
                # ||||
                #   ||
                # rectangles
                self.canvas.create_rectangle(w / 4, h / 2 - h / 8, w / 2, h / 2 + h / 8, fill=hole_color)
                self.canvas.create_rectangle(w / 2, h / 4, w / 4 * 3, h / 4 * 3, fill=shaft_color)
                # tolerance grades
                self.canvas.create_text(w / 4 + w / 8, h / 2, text=fit.hole_toler, font=gr_font)
                self.canvas.create_text(w / 2 + w / 8, h / 2, text=fit.shaft_toler, font=gr_font)
                # deviations
                self.canvas.create_text(w - w / 8, h / 4, text=fit.es, font=num_font, fill='white')
                self.canvas.create_text(w - w / 8, h / 4 * 3, text=fit.ei, font=num_font, fill='white')
                self.canvas.create_text(w / 8, h / 2 - h / 8, text=fit.ES, font=num_font, fill='white')
                self.canvas.create_text(w / 8, h / 2 + h / 8, text=fit.EI, font=num_font, fill='white')
            elif fit.ES < fit.es:
                extra = h / 8 if fit.EI == fit.ei else 0
                # rectangles
                self.canvas.create_rectangle(w / 4, h / 2 - h / 8, w / 2, h / 4 * 3, fill=hole_color)
                self.canvas.create_rectangle(w / 2, h / 4, w / 4 * 3, h / 2 + h / 8 + extra, fill=shaft_color)
                # tolerance grades
                self.canvas.create_text(w / 4 + w / 8, h / 2 + h / 16, text=fit.hole_toler, font=gr_font)
                self.canvas.create_text(w / 2 + w / 8, h / 2 - h / 16 + extra / 2, text=fit.shaft_toler, font=gr_font)
                # deviations
                self.canvas.create_text(w - w / 8, h / 4, text=fit.es, font=num_font, fill='white')
                self.canvas.create_text(w - w / 8, h / 2 + h / 8 + extra, text=fit.ei, font=num_font, fill='white')
                self.canvas.create_text(w / 8, h / 2 - h / 8, text=fit.ES, font=num_font, fill='white')
                self.canvas.create_text(w / 8, h / 4 * 3, text=fit.EI, font=num_font, fill='white')
            elif fit.ES > fit.es:
                extra = h / 8 if fit.EI == fit.ei else 0
                # rectangles
                self.canvas.create_rectangle(w / 4, h / 4, w / 2, h / 2 + h / 8 + extra, fill=hole_color)
                self.canvas.create_rectangle(w / 2, h / 2 - h / 8, w / 4 * 3, h / 4 * 3, fill=shaft_color)
                # tolerance grades
                self.canvas.create_text(w / 4 + w / 8, h / 2 - h / 16 + extra / 2, text=fit.hole_toler, font=gr_font)
                self.canvas.create_text(w / 2 + w / 8, h / 2 + h / 16, text=fit.shaft_toler, font=gr_font)
                # deviations
                self.canvas.create_text(w - w / 8, h / 2 - h / 8, text=fit.es, font=num_font, fill='white')
                self.canvas.create_text(w - w / 8, h / 4 * 3, text=fit.ei, font=num_font, fill='white')
                self.canvas.create_text(w / 8, h / 4, text=fit.ES, font=num_font, fill='white')
                self.canvas.create_text(w / 8, h / 2 + h / 8 + extra, text=fit.EI, font=num_font, fill='white')
            elif fit.ES == fit.es:
                if fit.EI < fit.ei:
                    extra = h / 16
                elif fit.EI > fit.ei:
                    extra = -h / 16
                else:  # EI = ei
                    extra = 0

                # rectangles
                self.canvas.create_rectangle(w / 4, h / 4, w / 2, h / 2 + extra, fill=hole_color)
                self.canvas.create_rectangle(w / 2, h / 4, w / 4 * 3, h / 2 - extra, fill=shaft_color)
                # tolerance grades
                self.canvas.create_text(w / 4 + w / 8, h / 4 + h / 10, text=fit.hole_toler, font=gr_font)
                self.canvas.create_text(w / 2 + w / 8, h / 4 + h / 10, text=fit.shaft_toler, font=gr_font)
                # deviations
                self.canvas.create_text(w - w / 8, h / 4, text=fit.es, font=num_font, fill='white')
                self.canvas.create_text(w - w / 8, h / 2 - extra, text=fit.ei, font=num_font, fill='white')
                self.canvas.create_text(w / 8, h / 4, text=fit.ES, font=num_font, fill='white')
                self.canvas.create_text(w / 8, h / 2 + extra, text=fit.EI, font=num_font, fill='white')
            else:
                self.canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, text='Sorry ;(', font=MY_FONT_BOLD, fill=YELLOW)

        # Canvas - Fit Type
        self.canvas.create_text(w / 2, h - h / 6, text=f'Type: {fit.fit_type} Fit', fill='white', font=FONT_GRAPH)

        # Canvas - Legend
        legend_font = Font(self.canvas, family='Comic Sans MS', size=9)
        x = 10
        self.canvas.create_rectangle(w / 4, h - 30, w / 4 + x, h - 30 - x, fill=hole_color)
        self.canvas.create_text(w / 2 + w / 16, h - 30 - x / 2, text='Hole Tolerance', fill=YELLOW, font=legend_font)

        self.canvas.create_rectangle(w / 4, h - 15, w / 4 + x, h - 15 - x, fill=shaft_color)
        self.canvas.create_text(w / 2 + w / 16, h - 15 - x / 2, text='Shaft Tolerance', fill=YELLOW, font=legend_font)

    def save_img(self):
        widget = self.canvas
        # get canvas coordinates
        x = self.winfo_rootx() + widget.winfo_x()
        y = self.winfo_rooty() + widget.winfo_y()
        x1 = x + widget.winfo_width()
        y1 = y + widget.winfo_height()

        img_path = filedialog.asksaveasfilename(
            initialfile=f'Fit_{self.fit.size}mm_{self.fit.hole_toler}_{self.fit.shaft_toler}',
            defaultextension='.png',
            filetypes=[('PNG', '*.png')]
        )
        if img_path:
            ImageGrab.grab().crop((x, y, x1, y1)).save(img_path)

    def view_help(self):
        webbrowser.open('https://clubtechnical.com/limits-fits-tolerances')


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
