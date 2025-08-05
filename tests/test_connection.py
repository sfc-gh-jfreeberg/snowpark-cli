import unittest
import tempfile
import os
from pathlib import Path
from snowpark_cli.connection import ConnectionManager


class TestConnectionManager(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False)
        self.temp_file.write("""
default_connection_name = "test"

[test]
account = "test-account"
user = "test-user"
password = "test-password"
database = "test-db"
schema = "test-schema"
warehouse = "test-warehouse"
role = "test-role"

[other]
account = "other-account"
user = "other-user"
password = "other-password"
""")
        self.temp_file.close()
        
    def tearDown(self):
        """Clean up test fixtures."""
        os.unlink(self.temp_file.name)
    
    def test_load_connections(self):
        """Test loading connections from TOML file."""
        manager = ConnectionManager(self.temp_file.name)
        config = manager._load_connections()
        
        self.assertIn('test', config)
        self.assertIn('other', config)
        self.assertEqual(config['default_connection_name'], 'test')
    
    def test_get_default_connection_params(self):
        """Test getting default connection parameters."""
        manager = ConnectionManager(self.temp_file.name)
        params = manager.get_connection_params()
        
        self.assertEqual(params['account'], 'test-account')
        self.assertEqual(params['user'], 'test-user')
        self.assertEqual(params['password'], 'test-password')
        self.assertEqual(params['database'], 'test-db')
    
    def test_get_specific_connection_params(self):
        """Test getting specific connection parameters."""
        manager = ConnectionManager(self.temp_file.name)
        params = manager.get_connection_params('other')
        
        self.assertEqual(params['account'], 'other-account')
        self.assertEqual(params['user'], 'other-user')
        self.assertEqual(params['password'], 'other-password')
    
    def test_missing_connection(self):
        """Test error handling for missing connection."""
        manager = ConnectionManager(self.temp_file.name)
        
        with self.assertRaises(ValueError):
            manager.get_connection_params('nonexistent')
    
    def test_missing_file(self):
        """Test error handling for missing connections file."""
        manager = ConnectionManager('/nonexistent/path.toml')
        
        with self.assertRaises(FileNotFoundError):
            manager._load_connections()


if __name__ == '__main__':
    unittest.main()
