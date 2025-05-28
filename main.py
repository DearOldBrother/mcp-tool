#!/usr/bin/env python3
"""
简单的 MCP 工具示例
这个工具提供基本的文本处理功能
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional

from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server


class SimpleMCPTool:
    """简单的 MCP 工具类"""
    
    def __init__(self):
        self.server = Server("python-text-tool")
        self.setup_handlers()
    
    def setup_handlers(self):
        """设置工具处理器"""
        
        # 列出可用的工具
        @self.server.list_tools()
        async def list_tools() -> List[types.Tool]:
            return [
                types.Tool(
                    name="text_reverse",
                    description="反转输入的文本",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "要反转的文本"
                            }
                        },
                        "required": ["text"]
                    }
                ),
                types.Tool(
                    name="text_count",
                    description="统计文本的字符数和单词数",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "要统计的文本"
                            }
                        },
                        "required": ["text"]
                    }
                ),
                types.Tool(
                    name="text_upper",
                    description="将文本转换为大写",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "要转换的文本"
                            }
                        },
                        "required": ["text"]
                    }
                )
            ]
        
        # 调用工具
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            if name == "text_reverse":
                text = arguments.get("text", "")
                reversed_text = text[::-1]
                return [
                    types.TextContent(
                        type="text",
                        text=f"原文本: {text}\n反转后: {reversed_text}"
                    )
                ]
            
            elif name == "text_count":
                text = arguments.get("text", "")
                char_count = len(text)
                word_count = len(text.split())
                return [
                    types.TextContent(
                        type="text",
                        text=f"文本: {text}\n字符数: {char_count}\n单词数: {word_count}"
                    )
                ]
            
            elif name == "text_upper":
                text = arguments.get("text", "")
                upper_text = text.upper()
                return [
                    types.TextContent(
                        type="text",
                        text=f"原文本: {text}\n大写: {upper_text}"
                    )
                ]
            
            else:
                raise ValueError(f"未知工具: {name}")
    
    async def run(self):
        """运行 MCP 服务器"""
        async with stdio_server() as streams:
            await self.server.run(
                streams[0], streams[1],
                self.server.create_initialization_options()
            )


# 主函数
async def main():
    tool = SimpleMCPTool()
    await tool.run()


if __name__ == "__main__":
    asyncio.run(main())
