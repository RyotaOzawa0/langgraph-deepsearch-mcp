#!/usr/bin/env python3
"""
Langgraph Deep Search MCP Server

This server provides the Langgraph Deep Search implementation
as an MCP (Model Context Protocol) server for integration with Claude Desktop
and other MCP clients.

Usage:
    python gemini_server.py

Environment Variables:
    GEMINI_API_KEY: Required - Your Gemini API key from Google AI Studio
"""

import sys
import os
import asyncio

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from deep_search_mcp.mcp_server import main


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable is required")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        sys.exit(1)
    
    print("🚀 Starting Langgraph Deep Search MCP Server...")
    print("💡 Using Langgraph implementation with native Google Search")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)