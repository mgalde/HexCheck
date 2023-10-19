# HexCheck - Network Visualization Tool

`HexCheck` is a graphical tool built with `tkinter` in Python that provides a visual representation of server statuses using hexagonal tiles.

## Features

1. **Dynamic Server Configuration**: Load server configurations from a file, allowing for easy modification and expansion.
2. **Ping Check**: Determine if a server is alive using the `ping` command.
3. **Port Check**: Test if a specific port is open on the server.
4. **Visual Feedback**:
   - Hexagon turns **red** if the server is not reachable.
   - Hexagon turns **green** if the server is alive and the specified port is open.
   - Hexagon turns **blue** if the server is alive but the specified port is closed.
5. **Dynamic Hexagon Positioning**: Hexagons are positioned dynamically based on screen width. If there are too many hexagons for one row, they wrap to the next row.
6. **Interactive UI**:
   - Right-click context menu with options to toggle fullscreen mode or exit the application.
   - Periodic automatic updates to refresh server status.
7. **Modern Font & Design**: Uses modern fonts available on Windows for a sleek look.

## Code Breakdown

- **Utility Functions**:
  - `is_host_alive(ip)`: Checks if a host is alive using the `ping` command.
  - `is_port_open(ip, port, timeout=1)`: Checks if a specific port is open on a given IP.
  - `get_hexagon_status_color(ip, port)`: Determines the color of a hexagon based on server and port status.
  
- **Visualization Functions**:
  - `draw_hexagon(canvas, x, y, size, fill_color, name)`: Draws a single hexagon on the canvas.
  - `update_hexagon_color(x, y, size, fill_color, canvas_item)`: Updates the color of an existing hexagon.
  - `draw_all_hexagons(canvas, servers)`: Draws all hexagons based on the provided server list.
  - `adjust_canvas_size(canvas, servers)`: Adjusts the canvas size to fit all hexagons.

- **Configuration Management**:
  - `parse_config(filename)`: Parses a configuration file to obtain a list of servers.

- **UI Event Handlers**:
  - `update_canvas()`: Periodically updates the status of all servers and refreshes their colors.
  - `toggle_fullscreen(event=None)`: Toggles the application between fullscreen and windowed mode.
  - `create_context_menu(event)`: Displays a context menu on right-click.
