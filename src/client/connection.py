"""Connection manager for online play."""

import logging
from typing import Optional, Dict, Callable
import time


class ConnectionManager:
    """Manages connection to online game server."""
    
    def __init__(self, server_url: Optional[str] = None):
        """
        Initialize connection manager.
        
        Args:
            server_url: URL of the game server (WebSocket or HTTP)
        """
        self.server_url = server_url or "ws://localhost:8080"
        self.connected = False
        self.session_id: Optional[str] = None
        self.logger = logging.getLogger(__name__)
        self.callbacks: Dict[str, Callable] = {}
    
    def connect(self, auth_token: Optional[str] = None) -> bool:
        """
        Connect to the game server.
        
        Args:
            auth_token: Authentication token for server
            
        Returns:
            True if connection successful
        """
        try:
            self.logger.info(f"Connecting to {self.server_url}...")
            
            # Simulate connection (in real implementation, use websockets or requests)
            # import websockets
            # self.websocket = await websockets.connect(self.server_url)
            
            self.connected = True
            self.session_id = f"session_{int(time.time())}"
            self.logger.info(f"Connected successfully. Session ID: {self.session_id}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            self.connected = False
            return False
    
    def disconnect(self) -> None:
        """Disconnect from the game server."""
        if self.connected:
            self.logger.info("Disconnecting from server...")
            self.connected = False
            self.session_id = None
            # await self.websocket.close()
    
    def send_message(self, message_type: str, data: Dict) -> bool:
        """
        Send a message to the server.
        
        Args:
            message_type: Type of message (e.g., 'bet', 'spin')
            data: Message payload
            
        Returns:
            True if message sent successfully
        """
        if not self.connected:
            self.logger.error("Not connected to server")
            return False
        
        try:
            message = {
                "type": message_type,
                "session_id": self.session_id,
                "data": data,
                "timestamp": time.time()
            }
            
            self.logger.debug(f"Sending message: {message_type}")
            # await self.websocket.send(json.dumps(message))
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return False
    
    def receive_message(self) -> Optional[Dict]:
        """
        Receive a message from the server.
        
        Returns:
            Message dictionary or None
        """
        if not self.connected:
            return None
        
        try:
            # response = await self.websocket.recv()
            # return json.loads(response)
            
            # Placeholder for simulation
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to receive message: {e}")
            return None
    
    def register_callback(self, event_type: str, callback: Callable) -> None:
        """
        Register a callback for specific event types.
        
        Args:
            event_type: Type of event to listen for
            callback: Function to call when event occurs
        """
        self.callbacks[event_type] = callback
        self.logger.debug(f"Registered callback for {event_type}")
    
    def is_connected(self) -> bool:
        """
        Check if connected to server.
        
        Returns:
            True if connected
        """
        return self.connected
    
    def get_session_info(self) -> Dict:
        """
        Get current session information.
        
        Returns:
            Dictionary with session details
        """
        return {
            "server_url": self.server_url,
            "connected": self.connected,
            "session_id": self.session_id
        }
