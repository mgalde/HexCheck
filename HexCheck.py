import tkinter as tk
import subprocess
import socket
import platform
import os
import time

def is_host_alive(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]
    try:
        if platform.system().lower() == "windows":
            # For windows, prevent the command line window from showing up
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, timeout=2, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, timeout=2)
        return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:  # Handle timeout explicitly
        return False  # Host is not responding within the timeout


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
canvas_items = []

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
    font_choice = ("DejaVu Sans", 12)
    text = canvas.create_text(x, y, fill="white", text=name, font=font_choice)

    #text = canvas.create_text(x, y, fill="white", text=name)  # Server name in the middle
    canvas_items.extend([hexagon, text])  # Add the hexagon and text items to the list

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

def update_hexagon_color(x, y, size, fill_color, canvas_item):
    """Updates the color of an existing hexagon."""
    coords = [
        x, y-size,
        x+(size*1.5), y-(size/2),
        x+(size*1.5), y+(size/2),
        x, y+size,
        x-(size*1.5), y+(size/2),
        x-(size*1.5), y-(size/2)
    ]
    canvas.itemconfig(canvas_item, fill=fill_color)

def update_canvas():
    x, y = 100, 100  # Starting coordinates

    for index, server in enumerate(servers):
        color = get_hexagon_status_color(server["ip"], server["port"])
        
        # Each hexagon is two items (polygon and text), so index*2 gives the hexagon item.
        hexagon_item = canvas_items[index*2]
        update_hexagon_color(x, y, size, color, hexagon_item)
        
        x += (size*3) + spacing  # Adjust for spacing

    root.after(7000, update_canvas)  # Repoll every 7 seconds

def adjust_canvas_size(canvas, servers):
    screen_width = root.winfo_screenwidth()  # Get screen width
    max_hexagons_in_row = screen_width // (3*size + spacing)  # Maximum hexagons in one row

    total_rows = len(servers) // max_hexagons_in_row
    if len(servers) % max_hexagons_in_row != 0:
        total_rows += 1

    canvas_height = total_rows * (2 * size + spacing) + 100  # 100 for some padding
    canvas_width = screen_width

    canvas.config(width=canvas_width, height=canvas_height)


def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes('-fullscreen', is_fullscreen)

def create_context_menu(event):
    global context
    context.post(event.x_root, event.y_root)

root = tk.Tk()
root.title("IAES Network Visualization")
root.configure(background='black')

is_fullscreen = False  # To keep track of the fullscreen state

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=tk.YES)
canvas.bind("<Button-3>", create_context_menu)  # Bind right-click

# Create a context menu
context = tk.Menu(root, tearoff=0)
context.add_command(label="Toggle Fullscreen", command=toggle_fullscreen)
context.add_command(label="Exit", command=root.quit)

# Parse config and get servers list
servers = parse_config("config.txt")
size = 50  # Hexagon size
spacing = 5  # Space between hexagons

def draw_all_hexagons(canvas, servers):
    """Draws all hexagons on the canvas based on the servers provided."""
    screen_width = root.winfo_screenwidth()  # Get screen width
    max_hexagons_in_row = screen_width // (3*size + spacing)  # Maximum hexagons in one row
    
    # Starting coordinates for each hexagon
    x, y = 100, 100  
    
    for server in servers:
        fill_color = "gray"  # Default color before the first check
        draw_hexagon(canvas, x, y, size, fill_color, server["name"])
        
        # Check if we've reached the max hexagons in this row
        if (servers.index(server) + 1) % max_hexagons_in_row == 0:
            y += 2 * size + spacing  # Move to the next row
            x = 100  # Reset x to starting position
        else:
            x += (size * 3) + spacing  # Adjust for spacing within the row

# Clear the canvas
canvas.delete("all")

# Adjust canvas size to fit all hexagons
adjust_canvas_size(canvas, servers)

# Draw hexagons for each server
draw_all_hexagons(canvas, servers)




# Call the update function
update_canvas()

root.mainloop()
