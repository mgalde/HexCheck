import tkinter as tk
import subprocess
import socket
import platform
import os
import time

def debounce(wait):
    def decorator(fun):
        last_time = 0

        def debounced(*args, **kwargs):
            nonlocal last_time
            current_time = time.time()
            if current_time - last_time >= wait:
                result = fun(*args, **kwargs)
                last_time = current_time
                return result

        return debounced

    return decorator

def is_host_alive(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]
    try:
        if platform.system().lower() == "windows":
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, timeout=2, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, timeout=2)
        return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        return False

def is_port_open(ip, port, timeout=1):
    try:
        socket.create_connection((ip, port), timeout)
        return True
    except Exception:
        return False

def get_hexagon_status_color(ip, port):
    if not is_host_alive(ip):
        return "red"
    elif is_host_alive(ip) and is_port_open(ip, port):
        return "green"
    else:
        return "blue"

def draw_hexagon(canvas, x, y, size, fill_color, name):
    height = size * (3**0.5)
    coords = [
        x, y-size,
        x+(size*1.5), y-(size/2),
        x+(size*1.5), y+(size/2),
        x, y+size,
        x-(size*1.5), y+(size/2),
        x-(size*1.5), y-(size/2)
    ]
    hexagon = canvas.create_polygon(coords, fill=fill_color)
    font_size = int(size / 3)
    font_choice = ("DejaVu Sans", font_size)
    text = canvas.create_text(x, y, fill="white", text=name, font=font_choice)

    return hexagon, text

def parse_config(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_file_path = os.path.join(dir_path, filename)
    if not os.path.exists(filename):
        default_config = [
            "1",
            "Google DNS",
            "8.8.8.8",
            "53",
            "DNS",
            "2",
            "Cloudflare DNS",
            "1.1.1.1",
            "80",
            "Portal"
        ]
        with open(config_file_path, 'w') as file:
            file.write('\n'.join(default_config))

    with open(config_file_path, 'r') as file:
        lines = file.readlines()

        servers = []
        for i in range(0, len(lines), 5):
            server = {
                "id": lines[i].strip(),
                "name": lines[i+1].strip(),
                "ip": lines[i+2].strip(),
                "port": int(lines[i+3].strip()),
                "service": lines[i+4].strip()
            }
            servers.append(server)
    return servers

def update_hexagon_color(canvas, hexagon, fill_color):
    canvas.itemconfig(hexagon, fill=fill_color)

def update_canvas(canvas, hexagons, servers):
    for hexagon, server in zip(hexagons, servers):
        color = get_hexagon_status_color(server["ip"], server["port"])
        update_hexagon_color(canvas, hexagon[0], color)

    canvas.after(7000, update_canvas, canvas, hexagons, servers)

def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes('-fullscreen', is_fullscreen)

def create_context_menu(event):
    global context
    context.post(event.x_root, event.y_root)

@debounce(0.5)
def on_resize(event):
    global hexagons
    canvas.delete("all")
    hexagons = draw_all_hexagons(canvas, servers)
    update_canvas(canvas, hexagons, servers)

root = tk.Tk()
root.title("The Packet Network Visualization")
root.configure(background='black')

is_fullscreen = False

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=tk.YES)
canvas.bind("<Button-3>", create_context_menu)
canvas.bind("<Configure>", on_resize)

context = tk.Menu(root, tearoff=0)
context.add_command(label="Toggle Fullscreen", command=toggle_fullscreen)
context.add_command(label="Exit", command=root.quit)

servers = parse_config("config.txt")

def draw_all_hexagons(canvas, servers):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    num_servers = len(servers)
    size = min(canvas_width // (num_servers // 2 + 1), canvas_height // (num_servers // 3 + 1)) // 4
    spacing = size // 2

    max_hexagons_in_row = canvas_width // (3*size + spacing)
    total_rows = (num_servers - 1) // max_hexagons_in_row + 1

    hexagons = []
    for i, server in enumerate(servers):
        row = i // max_hexagons_in_row
        col = i % max_hexagons_in_row

        x = (3*size + spacing) * col + (3*size + spacing) // 2
        y = (2*size + spacing) * row + (2*size + spacing) // 2

        fill_color = "gray"
        hexagon, text = draw_hexagon(canvas, x, y, size, fill_color, server["name"])
        hexagons.append((hexagon, text))

    return hexagons

hexagons = []

root.mainloop()
