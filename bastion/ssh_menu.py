#!/usr/bin/env python3
"""
SSH Connection Menu with Catppuccin Mocha Theme
A beautiful, intuitive SSH bastion menu system with multi-user support
"""

import curses
import json
import subprocess
import sys
from pathlib import Path


class SSHMenu:
    def __init__(self, config_path='config.json'):
        """Initialize SSH Menu with configuration"""
        self.config_path = config_path
        self.config = None
        
    def load_config(self):
        """Load and parse JSON configuration"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            return True
        except FileNotFoundError:
            print(f"Error: Configuration file '{self.config_path}' not found")
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in configuration file: {e}")
            return False
    
    def validate_config(self):
        """Validate configuration integrity"""
        errors = []
        
        # Check top-level structure
        if not isinstance(self.config, dict):
            errors.append("Config must be a JSON object")
            return errors
        
        if 'networks' not in self.config:
            errors.append("Missing 'networks' key in config")
            return errors
        
        if not isinstance(self.config['networks'], list):
            errors.append("'networks' must be an array")
            return errors
        
        # Validate each network
        required_network_fields = ['name', 'servers']
        
        for idx, network in enumerate(self.config['networks']):
            net_prefix = f"Network [{idx}]"
            
            # Check required network fields
            for field in required_network_fields:
                if field not in network:
                    errors.append(f"{net_prefix}: Missing required field '{field}'")
            
            # Validate servers
            if 'servers' in network:
                if not isinstance(network['servers'], list):
                    errors.append(f"{net_prefix}: 'servers' must be an array")
                    continue
                
                for srv_idx, server in enumerate(network['servers']):
                    srv_prefix = f"{net_prefix} Server [{srv_idx}]"
                    
                    # Check that server has IP
                    if 'ip' not in server:
                        errors.append(f"{srv_prefix}: Missing required field 'ip'")
                    
                    # Validate server format (old vs new)
                    has_username = 'username' in server
                    has_users = 'users' in server
                    
                    if not has_username and not has_users:
                        errors.append(f"{srv_prefix}: Must have either 'username' or 'users' field")
                    
                    if has_username and has_users:
                        errors.append(f"{srv_prefix}: Cannot have both 'username' and 'users' fields")
                    
                    # Validate users array if present
                    if has_users:
                        if not isinstance(server['users'], list):
                            errors.append(f"{srv_prefix}: 'users' must be an array")
                        elif len(server['users']) == 0:
                            errors.append(f"{srv_prefix}: 'users' array cannot be empty")
                        else:
                            for user_idx, user in enumerate(server['users']):
                                user_prefix = f"{srv_prefix} User [{user_idx}]"
                                if 'username' not in user:
                                    errors.append(f"{user_prefix}: Missing required field 'username'")
                                
                                # Validate key_path if present
                                if 'key_path' in user and user['key_path']:
                                    key_path = Path(user['key_path']).expanduser()
                                    if not key_path.exists():
                                        errors.append(f"{user_prefix}: SSH key not found at '{user['key_path']}'")
                    
                    # Validate port if present
                    if 'port' in server and server['port'] is not None:
                        port = server['port']
                        if not isinstance(port, int) or not (1 <= port <= 65535):
                            errors.append(f"{srv_prefix}: Invalid port '{port}' (must be 1-65535)")
                    
                    # Validate key_path for old format
                    if has_username and 'key_path' in server and server['key_path']:
                        key_path = Path(server['key_path']).expanduser()
                        if not key_path.exists():
                            errors.append(f"{srv_prefix}: SSH key not found at '{server['key_path']}'")
        
        return errors
    
    def normalize_server_format(self, server):
        """
        Normalize server format to always use 'users' array internally.
        This ensures backward compatibility with old format.
        
        Returns: (server_info, users_list)
        """
        # Extract common server properties
        server_info = {
            'ip': server['ip'],
            'description': server.get('description', 'N/A'),
            'port': self.get_port(server)
        }
        
        # Check if old format (direct username) or new format (users array)
        if 'users' in server:
            # New format: already has users array
            users = server['users']
        else:
            # Old format: convert to users array
            users = [{
                'username': server['username'],
                'key_path': server.get('key_path'),
                'description': server.get('description', 'Default user')
            }]
        
        return server_info, users
    
    def get_auth_method_display(self, user):
        """Determine authentication method and display info for a user"""
        key_path = user.get('key_path')
        
        if key_path:
            # Expand ~ to home directory
            expanded_path = str(Path(key_path).expanduser())
            return "KEY", expanded_path
        else:
            return "PASSWORD", None
    
    def get_port(self, server):
        """Get SSH port with default fallback"""
        port = server.get('port', 22)
        
        # Validate port is valid
        if not isinstance(port, int) or not (1 <= port <= 65535):
            return 22  # Fallback to default
        
        return port
    
    def init_catppuccin_colors(self):
        """Initialize Catppuccin Mocha color scheme"""
        
        # Check if terminal supports color customization
        if not curses.can_change_color():
            return self.init_fallback_colors()
        
        try:
            # Catppuccin Mocha palette (RGB values scaled to 0-1000 for curses)
            colors = {
                'base':      (117, 117, 180),   # #1e1e2e - background
                'text':      (804, 839, 957),   # #cdd6f4 - main text
                'subtext':   (729, 761, 878),   # #bac2de - secondary text
                'overlay':   (423, 439, 522),   # #6c7086 - dimmed text
                'surface':   (192, 196, 267),   # #313244 - subtle bg
                'mauve':     (796, 651, 969),   # #cba6f7 - purple accent
                'blue':      (537, 706, 980),   # #89b4fa - primary accent
                'lavender':  (706, 745, 996),   # #b4befe - secondary accent
                'green':     (651, 890, 631),   # #a6e3a1 - success
                'yellow':    (976, 886, 686),   # #f9e2af - warning
                'red':       (953, 545, 659),   # #f38ba8 - error
                'peach':     (980, 702, 529),   # #fab387 - highlight
                'teal':      (580, 886, 835),   # #94e2d5 - info
            }
            
            # Define custom colors (curses color IDs 16-28)
            curses.init_color(16, *colors['base'])
            curses.init_color(17, *colors['text'])
            curses.init_color(18, *colors['subtext'])
            curses.init_color(19, *colors['overlay'])
            curses.init_color(20, *colors['surface'])
            curses.init_color(21, *colors['mauve'])
            curses.init_color(22, *colors['blue'])
            curses.init_color(23, *colors['lavender'])
            curses.init_color(24, *colors['green'])
            curses.init_color(25, *colors['yellow'])
            curses.init_color(26, *colors['red'])
            curses.init_color(27, *colors['peach'])
            curses.init_color(28, *colors['teal'])
            
            # Define color pairs (foreground, background)
            curses.init_pair(1, 17, 16)   # Normal text: text on base
            curses.init_pair(2, 16, 22)   # Selected: base on blue
            curses.init_pair(3, 21, 16)   # Header: mauve on base
            curses.init_pair(4, 27, 16)   # Highlight: peach on base
            curses.init_pair(5, 24, 16)   # Success: green on base
            curses.init_pair(6, 26, 16)   # Error: red on base
            curses.init_pair(7, 18, 16)   # Subtext: subtext on base
            curses.init_pair(8, 23, 16)   # Info: lavender on base
            curses.init_pair(9, 28, 16)   # Accent: teal on base
            curses.init_pair(10, 22, 16)  # Links: blue on base
            curses.init_pair(11, 25, 16)  # Warning: yellow on base
            
        except Exception:
            return self.init_fallback_colors()
    
    def init_fallback_colors(self):
        """Fallback color scheme for terminals that don't support custom colors"""
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)    # Normal
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)     # Selected
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Header
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # Highlight
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)    # Success
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)      # Error
        curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)     # Subtext
        curses.init_pair(8, curses.COLOR_BLUE, curses.COLOR_BLACK)     # Info
        curses.init_pair(9, curses.COLOR_CYAN, curses.COLOR_BLACK)     # Accent
        curses.init_pair(10, curses.COLOR_BLUE, curses.COLOR_BLACK)    # Links
        curses.init_pair(11, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Warning
    
    def setup_colors(self):
        """Initialize color scheme"""
        curses.start_color()
        curses.use_default_colors()
        
        # Try to initialize Catppuccin colors
        try:
            self.init_catppuccin_colors()
        except Exception:
            self.init_fallback_colors()
    
    def draw_header(self, stdscr, title):
        """Draw styled header with Catppuccin Mocha theme"""
        height, width = stdscr.getmaxyx()
        
        # Clear and set background
        stdscr.bkgd(' ', curses.color_pair(1))
        stdscr.clear()
        
        # Draw top border (mauve/purple accent)
        border_line = "═" * (width - 4)
        try:
            stdscr.addstr(0, 2, border_line, curses.color_pair(3) | curses.A_BOLD)
        except curses.error:
            pass
        
        # Draw title (centered, with icon)
        if "NETWORK" in title.upper():
            icon = "🌐 "
        elif "SERVER" in title.upper():
            icon = "  "
        elif "USER" in title.upper():
            icon = "👤 "
        else:
            icon = " "
        
        title_text = f"{icon}{title}"
        x_pos = max(2, (width - len(title_text)) // 2)
        try:
            stdscr.addstr(1, x_pos, title_text, curses.color_pair(3) | curses.A_BOLD)
        except curses.error:
            pass
        
        # Draw bottom border
        try:
            stdscr.addstr(2, 2, border_line, curses.color_pair(3) | curses.A_BOLD)
        except curses.error:
            pass
    
    def draw_footer(self, stdscr, text):
        """Draw footer with instructions"""
        height, width = stdscr.getmaxyx()
        footer_y = height - 2
        x_pos = max(2, (width - len(text)) // 2)
        
        try:
            stdscr.addstr(footer_y, x_pos, text, curses.color_pair(8))
        except curses.error:
            pass
    
    def run_network_selection(self, stdscr):
        """Network selection menu with Catppuccin styling"""
        current_row = 0
        networks = self.config['networks']
        
        while True:
            stdscr.clear()
            self.draw_header(stdscr, "SELECT NETWORK ZONE")
            height, width = stdscr.getmaxyx()
            
            # Display networks
            start_y = 4
            for idx, network in enumerate(networks):
                y_pos = start_y + idx
                
                if y_pos >= height - 3:
                    break
                
                # Format network info
                name = network['name'].ljust(15)
                cidr = network.get('cidr', 'N/A').ljust(18)
                server_count = len(network.get('servers', []))
                info = f"{server_count} server{'s' if server_count != 1 else ''}"
                
                line = f"  {name} ({cidr}) - {info}"
                
                # Apply color based on selection
                try:
                    if idx == current_row:
                        # Selected item: base text on blue background
                        stdscr.addstr(y_pos, 2, "→", curses.color_pair(4) | curses.A_BOLD)
                        stdscr.addstr(y_pos, 4, line, curses.color_pair(2) | curses.A_BOLD)
                    else:
                        # Normal item: text on base
                        stdscr.addstr(y_pos, 2, " ")
                        stdscr.addstr(y_pos, 4, line, curses.color_pair(1))
                except curses.error:
                    pass
            
            # Draw footer with instructions
            self.draw_footer(stdscr, "↑/↓: Navigate | ENTER: Select | Q: Quit")
            
            stdscr.refresh()
            
            # Handle input
            key = stdscr.getch()
            
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(networks) - 1:
                current_row += 1
            elif key == ord('\n'):
                result = self.run_server_selection(stdscr, networks[current_row])
                if result is None:
                    continue  # Return to network selection
            elif key in [ord('q'), ord('Q'), 27]:  # Q or ESC
                return None
    
    def run_server_selection(self, stdscr, network):
        """Server selection menu with Catppuccin styling"""
        current_row = 0
        servers = network.get('servers', [])
        
        if not servers:
            # Show "no servers" message
            stdscr.clear()
            self.draw_header(stdscr, f"{network['name']} Network")
            height, width = stdscr.getmaxyx()
            
            msg = "No servers configured in this network"
            x_pos = (width - len(msg)) // 2
            try:
                stdscr.addstr(height // 2, x_pos, msg, curses.color_pair(6))
            except curses.error:
                pass
            
            self.draw_footer(stdscr, "Press any key to return...")
            stdscr.refresh()
            stdscr.getch()
            return None
        
        while True:
            stdscr.clear()
            title = f"SELECT SERVER - {network['name']} Network"
            self.draw_header(stdscr, title)
            height, width = stdscr.getmaxyx()
            
            start_y = 4
            for idx, server in enumerate(servers):
                y_pos = start_y + (idx * 3)  # 3 lines per server
                
                if y_pos >= height - 4:
                    break
                
                # Normalize server format
                server_info, users = self.normalize_server_format(server)
                
                # Get server info
                ip = server_info['ip']
                desc = server_info['description']
                port = server_info['port']
                port_display = f":{port}" if port != 22 else ""
                
                # Determine user count display
                user_count = len(users)
                if user_count == 1:
                    user_display = f"User: {users[0]['username']}"
                else:
                    user_display = f"{user_count} users available"
                
                # Line 1: IP and description
                try:
                    if idx == current_row:
                        stdscr.addstr(y_pos, 2, "→", curses.color_pair(4) | curses.A_BOLD)
                        stdscr.addstr(y_pos, 4, f"{ip}{port_display}", curses.color_pair(2) | curses.A_BOLD)
                        stdscr.addstr(y_pos, 4 + len(ip) + len(port_display) + 2, f"- {desc}", curses.color_pair(2))
                    else:
                        stdscr.addstr(y_pos, 2, " ")
                        stdscr.addstr(y_pos, 4, f"{ip}{port_display}", curses.color_pair(10))  # Blue for IP
                        stdscr.addstr(y_pos, 4 + len(ip) + len(port_display) + 2, f"- {desc}", curses.color_pair(7))  # Subtext
                    
                    # Line 2: User count
                    user_color = curses.color_pair(9) if user_count > 1 else curses.color_pair(7)
                    user_icon = "👥" if user_count > 1 else "👤"
                    user_text = f"    {user_icon} {user_display}"
                    
                    if idx == current_row:
                        stdscr.addstr(y_pos + 1, 4, user_text, user_color | curses.A_BOLD)
                    else:
                        stdscr.addstr(y_pos + 1, 4, user_text, user_color)
                    
                except curses.error:
                    pass
            
            # Footer
            self.draw_footer(stdscr, "↑/↓: Navigate | ENTER: Select | Q: Back")
            
            stdscr.refresh()
            
            # Handle input
            key = stdscr.getch()
            
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(servers) - 1:
                current_row += 1
            elif key == ord('\n'):
                # Normalize server format
                server_info, users = self.normalize_server_format(servers[current_row])
                
                # If only one user, connect directly
                if len(users) == 1:
                    self.connect_ssh(server_info, users[0])
                else:
                    # Show user selection menu
                    self.run_user_selection(stdscr, server_info, users)
            elif key in [ord('q'), ord('Q'), 27]:
                return None
    
    def run_user_selection(self, stdscr, server_info, users):
        """User selection menu (NEW!)"""
        current_row = 0
        
        while True:
            stdscr.clear()
            title = f"SELECT USER - {server_info['ip']}"
            self.draw_header(stdscr, title)
            height, width = stdscr.getmaxyx()
            
            # Display server context at top
            context_y = 4
            try:
                stdscr.addstr(context_y, 4, f"Server: ", curses.color_pair(7))
                stdscr.addstr(context_y, 12, f"{server_info['ip']} - {server_info['description']}", curses.color_pair(1))
            except curses.error:
                pass
            
            # Display users
            start_y = 6
            for idx, user in enumerate(users):
                y_pos = start_y + (idx * 3)  # 3 lines per user
                
                if y_pos >= height - 4:
                    break
                
                # Get user info
                username = user['username']
                user_desc = user.get('description', 'No description')
                auth_method, key_info = self.get_auth_method_display(user)
                
                # Line 1: Username
                try:
                    if idx == current_row:
                        stdscr.addstr(y_pos, 2, "→", curses.color_pair(4) | curses.A_BOLD)
                        stdscr.addstr(y_pos, 4, f"👤 {username}", curses.color_pair(2) | curses.A_BOLD)
                    else:
                        stdscr.addstr(y_pos, 2, " ")
                        stdscr.addstr(y_pos, 4, f"👤 {username}", curses.color_pair(10))
                    
                    # Line 2: Description
                    desc_color = curses.color_pair(2) if idx == current_row else curses.color_pair(7)
                    stdscr.addstr(y_pos + 1, 7, user_desc, desc_color)
                    
                    # Line 3: Auth method
                    auth_color = curses.color_pair(5) if auth_method == "KEY" else curses.color_pair(11)
                    auth_icon = " " if auth_method == "KEY" else " "
                    auth_text = f"{auth_icon} {auth_method}"
                    if key_info:
                        # Truncate long key paths
                        key_display = key_info if len(key_info) < 50 else f"...{key_info[-47:]}"
                        auth_text += f" ({key_display})"
                    
                    if idx == current_row:
                        stdscr.addstr(y_pos + 2, 7, auth_text, auth_color | curses.A_BOLD)
                    else:
                        stdscr.addstr(y_pos + 2, 7, auth_text, auth_color)
                    
                except curses.error:
                    pass
            
            # Footer
            self.draw_footer(stdscr, "↑/↓: Navigate | ENTER: Connect | Q: Back")
            
            stdscr.refresh()
            
            # Handle input
            key = stdscr.getch()
            
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(users) - 1:
                current_row += 1
            elif key == ord('\n'):
                # Connect with selected user
                self.connect_ssh(server_info, users[current_row])
            elif key in [ord('q'), ord('Q'), 27]:
                return None
    
    def connect_ssh(self, server_info, user):
        """Connect to server with specific user (Catppuccin-styled info display)"""
        # Restore terminal to normal mode
        curses.endwin()
        
        # Get connection details
        ip = server_info['ip']
        port = server_info['port']
        description = server_info['description']
        username = user['username']
        user_desc = user.get('description', 'N/A')
        auth_method, key_info = self.get_auth_method_display(user)
        
        # Catppuccin Mocha ANSI color codes
        RESET = "\033[0m"
        MAUVE = "\033[38;2;203;166;247m"      # Catppuccin Mauve
        BLUE = "\033[38;2;137;180;250m"       # Catppuccin Blue
        GREEN = "\033[38;2;166;227;161m"      # Catppuccin Green
        YELLOW = "\033[38;2;249;226;175m"     # Catppuccin Yellow
        PEACH = "\033[38;2;250;179;135m"      # Catppuccin Peach
        TEXT = "\033[38;2;205;214;244m"       # Catppuccin Text
        SUBTEXT = "\033[38;2;186;194;222m"    # Catppuccin Subtext
        RED = "\033[38;2;243;139;168m"        # Catppuccin Red
        
        # Display connection info
        print(f"\n{MAUVE}{'═' * 60}{RESET}")
        print(f"{BLUE}Connecting to:{RESET} {PEACH}{ip}{RESET}")
        print(f"{BLUE}Description:{RESET}   {TEXT}{description}{RESET}")
        print(f"{BLUE}👤 Username:{RESET}      {TEXT}{username}{RESET} {SUBTEXT}({user_desc}){RESET}")
        
        if auth_method == "KEY":
            print(f"{BLUE}Auth Method:{RESET}   {GREEN}{auth_method}{RESET}")
            print(f"{BLUE}Key Path:{RESET}      {SUBTEXT}{key_info}{RESET}")
        else:
            print(f"{BLUE}Auth Method:{RESET}   {YELLOW}{auth_method}{RESET}")
        
        port_label = f"{port} {'(default)' if port == 22 else '(custom)'}"
        print(f"{BLUE}🔌 Port:{RESET}          {TEXT}{port_label}{RESET}")
        print(f"{MAUVE}{'═' * 60}{RESET}\n")
        
        # Build SSH command
        ssh_command = ["ssh", "-p", str(port)]
        
        if auth_method == "KEY":
            ssh_command.extend(["-i", key_info])
        
        ssh_command.append(f"{username}@{ip}")
        
        # Execute SSH
        try:
            subprocess.run(ssh_command)
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Connection interrupted{RESET}")
        except Exception as e:
            print(f"\n{RED}Connection failed: {e}{RESET}")
        
        # Wait before returning to menu
        input(f"\n{SUBTEXT}Press ENTER to return to menu...{RESET}")
    
    def run(self):
        """Main application entry point"""
        # Load configuration
        if not self.load_config():
            return 1
        
        # Validate configuration
        errors = self.validate_config()
        if errors:
            print("Configuration validation failed:\n")
            for error in errors:
                print(f"  • {error}")
            return 1
        
        # Run curses interface
        try:
            curses.wrapper(self._run_curses)
        except KeyboardInterrupt:
            print("\nGoodbye!")
        
        return 0
    
    def _run_curses(self, stdscr):
        """Curses main loop wrapper"""
        # Setup
        self.setup_colors()
        curses.curs_set(0)  # Hide cursor
        stdscr.keypad(True)  # Enable special keys
        
        # Run network selection menu
        self.run_network_selection(stdscr)


def main():
    """Application entry point"""
    menu = SSHMenu()
    sys.exit(menu.run())


if __name__ == '__main__':
    main()

