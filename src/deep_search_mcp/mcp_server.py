"""FastMCP server for the Langgraph Deep Search implementation."""

import os
import asyncio
from typing import Any, Dict, List
from contextlib import asynccontextmanager

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource, ReadResourceRequest
from langchain_core.messages import HumanMessage

# Import the Langgraph implementation
from .graph import create_graph
from .state import OverallState
from .configuration import Configuration


class LanggraphDeepSearchMCP:
    """MCP Server wrapper for the Langgraph Deep Search implementation."""
    
    def __init__(self):
        self.graph = None
        self.config = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the Langgraph Deep Search agent."""
        try:
            # Verify API key
            if not os.getenv("GEMINI_API_KEY"):
                raise ValueError("GEMINI_API_KEY environment variable is required")
            
            # Create the research graph
            self.graph = create_graph()
            self.config = Configuration()
            print("✅ Langgraph Deep Search Agent initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize agent: {e}")
            self.graph = None
    
    async def deep_research(self, query: str, **kwargs) -> Dict[str, Any]:
        """Perform deep research using the Langgraph implementation."""
        if not self.graph:
            return {
                "error": "Agent not initialized. Please check your GEMINI_API_KEY.",
                "query": query,
                "answer": "",
                "sources": []
            }
        
        try:
            # Prepare the initial state
            initial_state: OverallState = {
                "messages": [HumanMessage(content=query)],
                "search_query": [],
                "web_research_result": [],
                "sources_gathered": [],
                "initial_search_query_count": kwargs.get("max_queries", 3),
                "max_research_loops": kwargs.get("max_iterations", 2),
                "research_loop_count": 0,
                "reasoning_model": kwargs.get("reasoning_model", "gemini-2.5-flash")
            }
            
            # Run the research graph
            final_state = await self.graph.ainvoke(
                initial_state,
                config={"configurable": {}}
            )
            
            # Extract the final answer
            answer = ""
            if final_state.get("messages"):
                last_message = final_state["messages"][-1]
                if hasattr(last_message, 'content'):
                    answer = last_message.content
                else:
                    answer = str(last_message)
            
            # Format sources
            sources = []
            for source in final_state.get("sources_gathered", []):
                if isinstance(source, dict):
                    sources.append({
                        "title": source.get("label", "Unknown"),
                        "url": source.get("value", ""),
                        "snippet": source.get("label", "")
                    })
            
            # Format a concise response
            result_summary = f"""
## Research Query: {query}

## Answer:
{answer}

## Sources ({len(sources)}):
{chr(10).join([f"- [{source.get('title', 'Unknown')}]({source.get('url', '')})" for source in sources[:10]])}

## Research Summary:
- Research loops completed: {final_state.get('research_loop_count', 0)}
- Search queries used: {len(final_state.get('search_query', []))}
- Sources gathered: {len(sources)}
"""
            
            return {
                "query": query,
                "answer": result_summary,
                "sources_count": len(sources),
                "research_loops": final_state.get("research_loop_count", 0),
                "status": "success"
            }
            
        except Exception as e:
            return {
                "error": f"Research failed: {str(e)}",
                "query": query,
                "answer": "",
                "sources": [],
                "status": "error"
            }
    
    async def quick_search(self, query: str, **kwargs) -> Dict[str, Any]:
        """Perform a quick search (single iteration)."""
        return await self.deep_research(
            query, 
            max_iterations=1, 
            max_queries=1,
            **kwargs
        )
    
    def get_status(self) -> Dict[str, Any]:
        """Get the status of the research agent."""
        return {
            "agent_initialized": self.graph is not None,
            "gemini_api_available": bool(os.getenv("GEMINI_API_KEY")),
            "configuration": {
                "query_generator_model": self.config.query_generator_model if self.config else None,
                "reflection_model": self.config.reflection_model if self.config else None,
                "answer_model": self.config.answer_model if self.config else None,
                "max_research_loops": self.config.max_research_loops if self.config else None,
            } if self.config else None
        }


# Create the MCP server
app = Server("langgraph-deep-search")
research_agent = LanggraphDeepSearchMCP()


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="deep_search",
            description="深く調査・検索・リサーチする。包括的で詳細な調査を行い、複数の検索イテレーションと反映を通じて徹底的にリサーチします。深い調査、詳しく調べる、深く検索、包括的に調査、詳細に調べる、徹底的に調査、しっかり調べる、網羅的に調査、深掘り調査、本格的に調べる、などの要求に最適です。",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "調査・検索したい質問やトピック"
                    },
                    "max_iterations": {
                        "type": "integer",
                        "description": "最大調査イテレーション数（デフォルト: 2、深い調査の場合は3-5推奨）",
                        "default": 2,
                        "minimum": 1,
                        "maximum": 5
                    },
                    "max_queries": {
                        "type": "integer", 
                        "description": "初期検索クエリの最大数（デフォルト: 3、包括的調査の場合は5-7推奨）",
                        "default": 3,
                        "minimum": 1,
                        "maximum": 10
                    },
                    "reasoning_model": {
                        "type": "string",
                        "description": "推論に使用するモデル（デフォルト: gemini-2.5-flash）",
                        "default": "gemini-2.5-flash"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="quick_search",
            description="クイック検索・簡単な調査・概要調査をする。単一イテレーションで迅速な結果を提供します。簡単に調べる、クイック検索、手早く調査、概要を調べる、サッと検索、軽く調べる、基本情報を調査、簡易検索、速攻調査、などの要求に最適です。",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "検索したい質問やキーワード"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_search_status",
            description="検索エージェントの現在の状態と設定を確認する。「状態を確認して」「設定を見せて」「エージェントの状況は？」などの要求に対応します。",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool calls."""
    if name == "deep_search":
        result = await research_agent.deep_research(**arguments)
        if "error" in result:
            return [TextContent(type="text", text=f"Error: {result['error']}")]
        return [TextContent(type="text", text=result["answer"])]
    
    elif name == "quick_search":
        result = await research_agent.quick_search(**arguments)
        if "error" in result:
            return [TextContent(type="text", text=f"Error: {result['error']}")]
        return [TextContent(type="text", text=result["answer"])]
    
    elif name == "get_search_status":
        result = research_agent.get_status()
        import json
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


@app.list_resources()
async def list_resources() -> List[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="langgraph://config",
            name="Langgraph Research Configuration",
            description="Current configuration and status of the Langgraph research agent",
            mimeType="application/json"
        )
    ]


@app.read_resource()
async def get_resource(request: ReadResourceRequest) -> str:
    """Get resource content."""
    if request.uri == "langgraph://config":
        status = research_agent.get_status()
        import json
        return json.dumps(status, indent=2)
    else:
        raise ValueError(f"Unknown resource: {request.uri}")


async def main():
    """Main entry point for the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream, 
            write_stream, 
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())