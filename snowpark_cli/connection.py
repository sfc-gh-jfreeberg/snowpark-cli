import os
import sys
import toml
from pathlib import Path
from typing import Dict, Any, Optional
from snowflake.snowpark import Session


class ConnectionManager:
    """Manages Snowflake connections from the connections.toml file."""
    
    def __init__(self, connections_file: Optional[str] = None):
        """
        Initialize the connection manager.
        
        Args:
            connections_file: Path to the connections.toml file. 
                            If None, uses ~/.snowflake/connections.toml
        """
        if connections_file is None:
            self.connections_file = Path.home() / ".snowflake" / "connections.toml"
        else:
            self.connections_file = Path(connections_file)
    
    def _load_connections(self) -> Dict[str, Any]:
        """Load connections from the TOML file."""
        if not self.connections_file.exists():
            raise FileNotFoundError(
                f"Connections file not found: {self.connections_file}\n"
                "Please create a connections.toml file with your Snowflake connection details."
            )
        
        try:
            with open(self.connections_file, 'r') as f:
                config = toml.load(f)
            return config
        except Exception as e:
            raise RuntimeError(f"Failed to parse connections file: {e}")
    
    def get_connection_params(self, connection_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get connection parameters for the specified connection.
        
        Args:
            connection_name: Name of the connection to use. If None, uses the default connection.
            
        Returns:
            Dictionary of connection parameters for Snowpark Session.
        """
        config = self._load_connections()
        
        # If no connection name specified, try to find the default
        if connection_name is None:
            if "default_connection_name" in config:
                connection_name = config["default_connection_name"]
            elif len(config) == 1:
                # If only one connection, use it as default
                connection_name = next(iter(config.keys()))
            else:
                # Look for a connection named "default"
                if "default" in config:
                    connection_name = "default"
                else:
                    available = [k for k in config.keys() if k != "default_connection_name"]
                    raise ValueError(
                        f"No connection specified and no default found. "
                        f"Available connections: {', '.join(available)}"
                    )
        
        if connection_name not in config:
            available = [k for k in config.keys() if k != "default_connection_name"]
            raise ValueError(
                f"Connection '{connection_name}' not found in connections file. "
                f"Available connections: {', '.join(available)}"
            )
        
        connection_config = config[connection_name]
        
        # Map common connection parameter names to Snowpark Session parameters
        session_params = {}
        
        # Required parameters
        required_params = {
            'account': 'account',
            'user': 'user',
            'password': 'password',
        }
        
        # Optional parameters
        optional_params = {
            'database': 'database',
            'schema': 'schema',
            'warehouse': 'warehouse',
            'role': 'role',
        }
        
        # Map required parameters
        for config_key, session_key in required_params.items():
            if config_key in connection_config:
                session_params[session_key] = connection_config[config_key]
            else:
                raise ValueError(f"Required parameter '{config_key}' missing from connection '{connection_name}'")
        
        # Map optional parameters
        for config_key, session_key in optional_params.items():
            if config_key in connection_config:
                session_params[session_key] = connection_config[config_key]
        
        return session_params
    
    def create_session(self, connection_name: Optional[str] = None) -> Session:
        """
        Create a Snowpark Session using the specified connection.
        
        Args:
            connection_name: Name of the connection to use. If None, uses the default connection.
            
        Returns:
            Configured Snowpark Session object.
        """
        params = self.get_connection_params(connection_name)
        return Session.builder.configs(params).create()
