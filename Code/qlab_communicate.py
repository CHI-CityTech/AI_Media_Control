from pythonosc import udp_client

ip = "127.0.0.1"
port = 53000

client = udp_client.SimpleUDPClient(ip, port)

cue_id = "1"
client.send_message(f"/cue/{cue_id}/start", None)
print(f"Sent start command to cue {cue_id}")
