import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttkb
import math
import logging


logging.basicConfig(level=logging.INFO)

# sajat tooltip
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = ttkb.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tip(self, event):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

# dimensiok kiszamitasa
def square_dimensions(area):
    side = math.sqrt(area)
    return side

def rectangle_dimensions(area):
    width = math.sqrt(area / 2)
    length = 2 * width
    return length, width

def circle_dimensions(area):
    radius = math.sqrt(area / math.pi)
    return radius

def equilateral_triangle_dimensions(area):
    side = math.sqrt((4 * area) / math.sqrt(3))
    return side

def diagonal_of_square(side):
    return math.sqrt(2) * side

def diagonal_of_rectangle(length, width):
    return math.sqrt(length**2 + width**2)

def validate_input(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def adjust_scale_factor(max_dimension):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    max_canvas_dimension = min(canvas_width, canvas_height) / 2  
    return max_canvas_dimension / max_dimension

def convert_units(value, from_unit, to_unit):
    conversion_factors = {
        'm': {'m': 1, 'mm': 1000, 'cm': 100, 'in': 39.3701},
        'mm': {'m': 0.001, 'mm': 1, 'cm': 0.1, 'in': 0.0393701},
        'cm': {'m': 0.01, 'mm': 10, 'cm': 1, 'in': 0.393701},
        'in': {'m': 0.0254, 'mm': 25.4, 'cm': 2.54, 'in': 1}
    }
    return value * conversion_factors[from_unit][to_unit]

def on_convert():
    if not area_entry.get():
        return
    if not validate_input(area_entry.get()):
        messagebox.showerror("Érvénytelen szám", "Kérem, adjon meg egy érvényes számot a területhez.")
        return
    try:
        area = float(area_entry.get())
        unit = unit_var.get()
        
        # meterben
        square_side_m = square_dimensions(area)
        rectangle_length_m, rectangle_width_m = rectangle_dimensions(area)
        circle_radius_m = circle_dimensions(area)
        triangle_side_m = equilateral_triangle_dimensions(area)
        
        # atlo meterben
        square_diagonal_m = diagonal_of_square(square_side_m)
        rectangle_diagonal_m = diagonal_of_rectangle(rectangle_length_m, rectangle_width_m)
        
        # kivalasztott meretek
        square_side = convert_units(square_side_m, 'm', unit)
        rectangle_length = convert_units(rectangle_length_m, 'm', unit)
        rectangle_width = convert_units(rectangle_width_m, 'm', unit)
        circle_radius = convert_units(circle_radius_m, 'm', unit)
        triangle_side = convert_units(triangle_side_m, 'm', unit)
        
        
        square_diagonal = convert_units(square_diagonal_m, 'm', unit)
        rectangle_diagonal = convert_units(rectangle_diagonal_m, 'm', unit)
        
        
        max_dimension = max(square_side, rectangle_length, rectangle_width, circle_radius * 2, triangle_side)
        global scale_factor
        scale_factor = adjust_scale_factor(max_dimension)
        
        
        canvas.delete("all")
        
        
        draw_square(square_side, square_diagonal)
        draw_rectangle(rectangle_length, rectangle_width, rectangle_diagonal)
        draw_circle(circle_radius)
        draw_triangle(triangle_side)
        
        
        results = (
            f"Négyzet: oldalhossz = {square_side:.2f} {unit}, Átló = {square_diagonal:.2f} {unit}\n"
            f"Téglalap (az egyik oldal kétszerese a másiknak): Hossz = {rectangle_length:.2f} {unit}, Szélesség = {rectangle_width:.2f} {unit}, Átló = {rectangle_diagonal:.2f} {unit}\n"
            f"Kör: sugár = {circle_radius:.2f} {unit}, Átmérő = {circle_radius * 2:.2f} {unit}\n"
            f"Egyenlő oldalú háromszög: oldalhossz = {triangle_side:.2f} {unit}"
        )
        
        results_label.config(text=results)
    except ValueError:
        messagebox.showerror("Érvénytelen szám", "Kérem, adjon meg egy érvényes számot a területhez.")

def on_calculate_area():
    if not length_entry.get() or not width_entry.get():
        return
    if not validate_input(length_entry.get()) or not validate_input(width_entry.get()):
        messagebox.showerror("Érvénytelen szám", "Kérem, adjon meg érvényes számokat a méretekhez.")
        return
    try:
        length = float(length_entry.get())
        width = float(width_entry.get())
        from_unit = unit_var.get()
        
        
        length_m = convert_units(length, from_unit, 'm')
        width_m = convert_units(width, from_unit, 'm')
        area = length_m * width_m
        
        area_entry.delete(0, tk.END)
        area_entry.insert(0, str(area))
        on_convert()
    except ValueError:
        messagebox.showerror("Érvénytelen bemenet", "Kérem, adjon meg érvényes számokat a méretekhez.")

def draw_square(side, diagonal):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    center_x, center_y = canvas_width // 4, canvas_height // 4
    scaled_side = side * scale_factor
    padding = 20
    canvas.create_rectangle(center_x - scaled_side/2, center_y - scaled_side/2, center_x + scaled_side/2, center_y + scaled_side/2, outline="blue", fill="lightblue")
    canvas.create_line(center_x - scaled_side/2, center_y - scaled_side/2, center_x + scaled_side/2, center_y + scaled_side/2, fill="white")
    canvas.create_text(center_x, center_y - scaled_side/2 - padding, text="Négyzet", fill="white", font=("Arial", 16))
    canvas.create_text(center_x, center_y + scaled_side/2.5 + padding, text=f"{side:.2f} {unit_var.get()}", fill="white", font=("Arial", 16))
    canvas.create_text(center_x, center_y + scaled_side/2 + 2 * padding, text=f"Átló: {diagonal:.2f} {unit_var.get()}", fill="white", font=("Arial", 16))

def draw_rectangle(length, width, diagonal):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    center_x, center_y = canvas_width * 3 // 4, canvas_height // 4
    scaled_length = length * scale_factor
    scaled_width = width * scale_factor
    padding = 20
    canvas.create_rectangle(center_x - scaled_length/2, center_y - scaled_width/2, center_x + scaled_length/2, center_y + scaled_width/2, outline="green", fill="lightgreen")
    canvas.create_line(center_x - scaled_length/2, center_y - scaled_width/2, center_x + scaled_length/2, center_y + scaled_width/2, fill="white")
    canvas.create_text(center_x, center_y - scaled_width/2 - padding, text="Téglalap", fill="white", font=("Arial", 16))
    canvas.create_text(center_x, center_y + scaled_width/3 + padding, text=f"{length:.2f} {unit_var.get()}", fill="white", font=("Arial", 16))
    canvas.create_text(center_x - scaled_length/2 - padding, center_y, text=f"{width:.2f} {unit_var.get()}", fill="white", font=("Arial", 16), anchor=tk.E)
    canvas.create_text(center_x, center_y + scaled_width/2 + 2 * padding, text=f"Átló: {diagonal:.2f} {unit_var.get()}", fill="white", font=("Arial", 16))

def draw_circle(radius):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    center_x, center_y = canvas_width // 4, canvas_height * 3 // 4
    scaled_radius = radius * scale_factor
    padding = 20
    canvas.create_oval(center_x - scaled_radius, center_y - scaled_radius, center_x + scaled_radius, center_y + scaled_radius, outline="red", fill="lightcoral")
    canvas.create_text(center_x, center_y, text="Kör", fill="white", font=("Arial", 16))
    canvas.create_text(center_x, center_y + scaled_radius + padding, text=f"Sugár-r = {radius:.2f} {unit_var.get()}", fill="white", font=("Arial", 16))
    canvas.create_text(center_x, center_y + scaled_radius + 4 * padding, text=f"Átmérő-d: {2 * radius:.2f} {unit_var.get()}", fill="white", font=("Arial", 16))

def draw_triangle(side):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    center_x, center_y = canvas_width * 3 // 4, canvas_height * 3 // 4
    scaled_side = side * scale_factor
    height = (math.sqrt(3) / 2) * scaled_side
    padding = 20
    canvas.create_polygon(center_x, center_y - height/2, center_x - scaled_side/2, center_y + height/2, center_x + scaled_side/2, center_y + height/2, outline="purple", fill="plum")
    canvas.create_text(center_x, center_y - height/2 - padding, text="Háromszög", fill="white", font=("Arial", 16))
    canvas.create_text(center_x, center_y + height/2 + padding, text=f"{side:.2f} {unit_var.get()}", fill="white", font=("Arial", 16))

def on_clear_canvas():
    canvas.delete("all")
    results_label.config(text="")
    area_entry.delete(0, tk.END)
    length_entry.delete(0, tk.END)
    width_entry.delete(0, tk.END)

def save_canvas():
    canvas.postscript(file="shapes.eps")
    messagebox.showinfo("Mentés", "Vászon elmentve shapes.eps néven")


root = ttkb.Window(themename="superhero")
root.title("Area Converter")
root.geometry('1280x720')


style = ttkb.Style()
style.configure('TLabel', padding=5, foreground="white")
style.configure('TButton', padding=5, foreground="white")


input_frame = ttkb.Frame(root, padding="10 10 10 10")
input_frame.grid(row=0, column=0, sticky="ew")


unit_var = tk.StringVar(value='mm')
units_frame = ttkb.Frame(input_frame)
units_frame.grid(column=0, row=0, columnspan=3, pady=(0, 10))

ttkb.Label(units_frame, text="Egység kiválasztása:").grid(column=0, row=0, sticky=tk.W)
ttkb.Radiobutton(units_frame, text="mm", variable=unit_var, value='mm').grid(column=1, row=0, sticky=tk.W)
ttkb.Radiobutton(units_frame, text="cm", variable=unit_var, value='cm').grid(column=2, row=0, sticky=tk.W)
ttkb.Radiobutton(units_frame, text="col", variable=unit_var, value='in').grid(column=3, row=0, sticky=tk.W)


ttkb.Label(input_frame, text="Adja meg a területet négyzetméterben:").grid(column=0, row=1, sticky=tk.W)
area_entry = ttkb.Entry(input_frame, width=15)
area_entry.grid(column=1, row=1, sticky=(tk.W, tk.E))


convert_button = ttkb.Button(input_frame, text="Átváltás", command=on_convert)
convert_button.grid(column=2, row=1)
ToolTip(convert_button, "Terület átváltása alakzatokra")


ttkb.Label(input_frame, text="Vagy adja meg a méreteket a terület kiszámításához:").grid(column=0, row=2, columnspan=3, sticky=tk.W, pady=(10, 0))
ttkb.Label(input_frame, text="Hossz:").grid(column=0, row=3, sticky=tk.W)
length_entry = ttkb.Entry(input_frame, width=15)
length_entry.grid(column=1, row=3, sticky=(tk.W, tk.E))
ttkb.Label(input_frame, text="Szélesség:").grid(column=0, row=4, sticky=tk.W)
width_entry = ttkb.Entry(input_frame, width=15)
width_entry.grid(column=1, row=4, sticky=(tk.W, tk.E))


calculate_button = ttkb.Button(input_frame, text="Terület kiszámítása", command=on_calculate_area)
calculate_button.grid(column=2, row=3, rowspan=2)
ToolTip(calculate_button, "Terület kiszámítása méretek alapján")


results_label = ttkb.Label(root, text="", justify=tk.LEFT, foreground="white")
results_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")


canvas_frame = ttkb.Frame(root)
canvas_frame.grid(row=2, column=0, sticky="nsew")

canvas = tk.Canvas(canvas_frame, bg="white")
canvas.pack(fill='both', expand=True)


canvas_frame.config(borderwidth=2, relief="sunken")


scale_factor = 0.05


root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)
input_frame.columnconfigure(1, weight=1)


canvas.bind("<Configure>", lambda event: on_convert())


button_frame = ttkb.Frame(root, padding="10 10 10 10")
button_frame.grid(row=3, column=0, sticky="ew")

clear_button = ttkb.Button(button_frame, text="Vászon törlése", command=on_clear_canvas)
clear_button.grid(column=0, row=0)
ToolTip(clear_button, "Vászon törlése")

save_button = ttkb.Button(button_frame, text="Vászon mentése", command=save_canvas)
save_button.grid(column=1, row=0)
ToolTip(save_button, "Mentse a vásznat EPS fájlként")

root.mainloop()
