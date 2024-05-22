import http.server
import socketserver
import os
from colorama import Fore, Style, init
try:
    from pyngrok import ngrok, conf
except ImportError:
    print("Please install pyngrok library: pip install pyngrok")
    exit(1)

init(autoreset=True)

BANNER = f"""
{Fore.CYAN}
  ____             _        __  __           _      
 |  _ \\ __ _ _ __ (_) ___  |  \\/  | ___   __| | ___ 
 | |_) / _` | '_ \\| |/ __| | |\\/| |/ _ \\ / _` |/ _ \\
 |  __/ (_| | | | | | (__  | |  | | (_) | (_| |  __/
 |_|   \\__,_|_| |_|_|\\___| |_|  |_|\\___/ \\__,_|\\___|
{Fore.YELLOW}___________________________________________________
{Fore.MAGENTA}
 [+] {Fore.GREEN}GitHub: {Fore.RESET + Style.BRIGHT}https://github.com/InfectedClown 
{Fore.YELLOW}___________________________________________________
{Style.RESET_ALL}
"""

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="web", **kwargs)
        self.log_request("")
        print(f"{Fore.GREEN}[+] Visitor Info:")
        print(f"{Fore.CYAN}    IP Address: {self.client_address[0]}")
        print(f"{Fore.CYAN}    User-Agent: {self.headers['User-Agent']}{Style.RESET_ALL}")
    def end_headers(self):
        self.send_header('ngrok-skip-browser-warning', '1')
        super().end_headers()
    def log_message(self, format, *args):
        pass

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)

    try:
        port = int(input(Fore.GREEN + "Enter the port you want to use (default 8000): " + Style.RESET_ALL).strip() or 8000)
    except ValueError:
        print(f"{Fore.RED}[!] Invalid port. Using default port 8000.{Style.RESET_ALL}")
        port = 8000

    use_ngrok = input(Fore.GREEN + "Do you want to use ngrok? (yes/no): " + Style.RESET_ALL).strip().lower()
    tunnel = None

    if use_ngrok == 'yes':
        token = input(Fore.GREEN + "Enter Token: " + Style.RESET_ALL).strip()
        if token:
            try:
                conf.get_default().auth_token = token
                tunnel = ngrok.connect(port)
                print(f"{Fore.CYAN}[*] Ingress established at {tunnel.public_url}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Error establishing ngrok tunnel: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Token is required to use ngrok.{Style.RESET_ALL}")

    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        print(f"\n{Fore.CYAN}[*] HOST: http://localhost:{port}{Style.RESET_ALL}")
        if tunnel:
            print(f"{Fore.CYAN}[*] ngrok URL: {tunnel.public_url}{Style.RESET_ALL}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}\n[!] Server stopped.{Style.RESET_ALL}")
            if tunnel:
                ngrok.disconnect(tunnel.public_url)
                ngrok.kill()

if __name__ == '__main__':
    main()
