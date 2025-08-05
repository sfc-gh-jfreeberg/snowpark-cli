import click
import sys
from pathlib import Path
from .connection import ConnectionManager
from .runner import PythonRunner


@click.group()
@click.version_option()
def cli():
    """Snowpark CLI - Run Python files with injected Snowpark Session objects."""
    pass


@cli.command()
@click.argument('file', type=click.Path(exists=True, path_type=Path))
@click.option('--connection', '-c', 
              help='Name of the connection in connections.toml to use')
@click.option('--connections-file', 
              type=click.Path(exists=True, path_type=Path),
              help='Path to connections.toml file (default: ~/.snowflake/connections.toml)')
def run(file: Path, connection: str = None, connections_file: Path = None):
    """
    Run a Python file with an injected Snowpark Session object.
    
    The Session object will be available as 'session' variable in your Python script.
    Connection details are read from ~/.snowflake/connections.toml by default.
    
    FILE: Path to the Python file to execute
    """
    try:
        # Initialize connection manager
        connection_manager = ConnectionManager(connections_file)
        
        # Initialize runner
        runner = PythonRunner(connection_manager)
        
        # Run the file
        click.echo(f"Running {file} with Snowpark session...")
        if connection:
            click.echo(f"Using connection: {connection}")
        
        runner.run_file(str(file), connection)
        click.echo("✓ Execution completed successfully")
        
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except RuntimeError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\nExecution interrupted by user", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()
