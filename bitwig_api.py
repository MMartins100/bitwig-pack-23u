import json
import socket
import time
from loguru import logger

class BitwigAPI:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False

    def connect(self):
        """Establish a connection to the Bitwig Studio API."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            logger.info(f"Connected to Bitwig API at {self.host}:{self.port}")
        except socket.error as e:
            logger.error(f"Failed to connect to Bitwig API: {e}")
            self.connected = False

    def disconnect(self):
        """Close the connection to the Bitwig Studio API."""
        if self.socket:
            self.socket.close()
            self.connected = False
            logger.info("Disconnected from Bitwig API.")

    def send_command(self, command):
        """Send a command to the Bitwig API and return the response."""
        if not self.connected:
            logger.warning("Not connected to Bitwig API. Please connect first.")
            return None
        
        try:
            self.socket.sendall((command + '\n').encode('utf-8'))
            response = self.socket.recv(4096).decode('utf-8')
            return json.loads(response)
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON response from Bitwig API.")
            return None
        except socket.error as e:
            logger.error(f"Socket error while sending command: {e}")
            return None

    def get_clip_list(self):
        """Retrieve the list of clips from the current Bitwig project."""
        command = '{"type": "getClipList"}'
        response = self.send_command(command)
        
        if response and 'clips' in response:
            return response['clips']
        else:
            logger.error("Failed to retrieve clip list.")
            return []

    def export_clip(self, clip_id, filename):
        """Export a specific clip to an audio file."""
        command = json.dumps({"type": "exportClip", "clipId": clip_id, "filename": filename})
        response = self.send_command(command)

        if response and response.get('success'):
            logger.info(f"Successfully exported clip {clip_id} to {filename}.")
        else:
            logger.error(f"Failed to export clip {clip_id}. Response: {response}")

    def wait_for_export(self, timeout=60):
        """Wait for the export process to complete."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Here you could add logic to check the status of the export if supported
            time.sleep(1)
        logger.warning("Export wait timed out.")

# TODO: Implement additional methods for more API functionalities
# TODO: Handle more specific error cases based on Bitwig API documentation
# TODO: Add proper logging instead of print statements for production use

# Potential limitations:
# - This code assumes a specific API response format.
# - Error handling is basic and could be enhanced.
# - The connection is not persistent; consider implementing a reconnect strategy.
