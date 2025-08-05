import os
import sys
import runpy
import tempfile
from pathlib import Path
from typing import Optional
from .connection import ConnectionManager


class PythonRunner:
    """Handles running Python files with injected Snowpark Session."""
    
    def __init__(self, connection_manager: ConnectionManager):
        """
        Initialize the Python runner.
        
        Args:
            connection_manager: ConnectionManager instance for creating sessions.
        """
        self.connection_manager = connection_manager
    
    def run_file(self, file_path: str, connection_name: Optional[str] = None) -> None:
        """
        Run a Python file with an injected Snowpark Session.
        
        Args:
            file_path: Path to the Python file to execute.
            connection_name: Name of the connection to use. If None, uses the default connection.
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Python file not found: {file_path}")
        
        if not file_path.suffix == '.py':
            raise ValueError(f"File must have .py extension: {file_path}")
        
        # Create the Snowpark session
        try:
            session = self.connection_manager.create_session(connection_name)
        except Exception as e:
            raise RuntimeError(f"Failed to create Snowpark session: {e}")
        
        # Read the original file content
        with open(file_path, 'r') as f:
            original_content = f.read()
        
        # Create the modified content with session injection
        modified_content = self._inject_session(original_content)
        
        # Create a temporary file with the modified content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(modified_content)
            temp_file_path = temp_file.name
        
        try:
            # Add the directory containing the original file to Python path
            # so relative imports work correctly
            original_dir = str(file_path.parent.absolute())
            if original_dir not in sys.path:
                sys.path.insert(0, original_dir)
            
            # Create a globals dictionary with the session
            globals_dict = {
                '__name__': '__main__',
                '__file__': str(file_path.absolute()),
                'session': session,
            }
            
            # Execute the modified file
            with open(temp_file_path, 'r') as f:
                code = compile(f.read(), str(file_path), 'exec')
                exec(code, globals_dict)
                
        except Exception as e:
            raise RuntimeError(f"Error executing Python file: {e}")
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except OSError:
                pass
            
            # Close the session
            try:
                session.close()
            except Exception:
                pass  # Session might already be closed
    
    def _inject_session(self, content: str) -> str:
        """
        Inject session availability into the Python file content.
        
        Args:
            content: Original file content.
            
        Returns:
            Modified content with session injection comments.
        """
        injection_comment = """# Snowpark CLI: A 'session' variable is available in this script
# This session is configured using the connection specified in ~/.snowflake/connections.toml

"""
        
        return injection_comment + content
