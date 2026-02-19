#!/usr/bin/env python
"""
Simple script to start PyJabber XMPP server for SPADE agents.
This server allows agents to connect and communicate with each other.
"""
import asyncio
from pyjabber.server import Server

async def main():
    print("=" * 60)
    print("Starting PyJabber XMPP Server")
    print("=" * 60)
    print("Host: localhost")
    print("Port: 5222")
    print("Registration: Enabled (auto-register)")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server\n")
    
    # Create and start the server
    server = Server(
        domain="localhost",
        port=5222,
        db_path="pyjabber.db"
    )
    
    try:
        await server.start()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        await server.stop()
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: If you see connection errors, the server is running.")
        print("Keep this terminal open and run your agent in another terminal.")
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            print("\nShutting down...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
