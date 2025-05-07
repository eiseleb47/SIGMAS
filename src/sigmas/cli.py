import click
from sigmas import create_app
import webbrowser
import threading
import time

def open_browser():
    """Opens the default web browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open("http://localhost:5000")

@click.command()
def main():
    """Launch SIGMAS web interface"""
    # Start browser in separate thread
    threading.Thread(target=open_browser).start()
    # Start Flask app
    create_app().run()

if __name__ == "__main__":
    main()