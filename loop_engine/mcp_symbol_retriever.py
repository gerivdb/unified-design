#!/usr/bin/env python3
"""
mcp_symbol_retriever.py - Client MCP Serena pour récupération symbolique
Économie ~16k tokens par session en remplaçant Read/Edit bruts par lookup MCP.
"""

from __future__ import annotations

import asyncio
import json
import logging
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class SymbolResult:
    """Résultat d'une requête de récupération de symbole."""
    name: str
    kind: str  # function | class | method | variable
    file_path: str
    line_start: int
    line_end: int
    signature: str
    docstring: Optional[str] = None
    references: list[str] = field(default_factory=list)
    source_snippet: Optional[str] = None


@dataclass
class MCPConfig:
    """Configuration du client MCP Serena."""
    server_command: list[str] = field(default_factory=lambda: ["serena", "mcp", "start"])
    transport: str = "stdio"
    max_symbols_per_call: int = 50
    request_timeout_sec: float = 10.0
    cache_ttl_sec: int = 300


class SerenaMCPClient:
    """
    Client MCP pour Serena - récupération symbolique au niveau fonction/classe.
    Remplace la lecture complète de fichiers (2000+ lignes) par extraction ciblée.
    """
    
    def __init__(self, config: Optional[MCPConfig] = None):
        self.config = config or MCPConfig()
        self._process: Optional[subprocess.Popen] = None
        self._request_id = 0
        self._symbol_cache: dict[str, list[SymbolResult]] = {}
    
    async def start(self) -> bool:
        """Démarre le serveur MCP Serena."""
        try:
            self._process = subprocess.Popen(
                self.config.server_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            # Handshake MCP
            await self._send_initialize()
            logger.info("Serena MCP client started")
            return True
        except FileNotFoundError:
            logger.error("Serena MCP server not found. Install: pip install serena-mcp")
            return False
        except Exception as e:
            logger.error(f"Failed to start Serena MCP: {e}")
            return False
    
    async def stop(self):
        """Arrête le serveur MCP."""
        if self._process:
            self._process.terminate()
            await asyncio.wait_for(self._process.wait(), timeout=5.0)
            self._process = None
    
    async def _send_initialize(self):
        """Envoie la requête d'initialisation MCP."""
        req = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "unified-design", "version": "1.0"}
            }
        }
        await self._send_request(req)
        # Lire la réponse
        await self._read_response()
    
    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id
    
    async def _send_request(self, request: dict):
        """Envoie une requête JSON-RPC."""
        if not self._process or not self._process.stdin:
            raise RuntimeError("MCP process not started")
        line = json.dumps(request) + "\n"
        self._process.stdin.write(line)
        await asyncio.get_event_loop().run_in_executor(None, self._process.stdin.flush)
    
    async def _read_response(self) -> dict:
        """Lit une réponse JSON-RPC."""
        if not self._process or not self._process.stdout:
            raise RuntimeError("MCP process not started")
        line = await asyncio.get_event_loop().run_in_executor(
            None, self._process.stdout.readline
        )
        return json.loads(line)
    
    async def find_symbol(
        self,
        query: str,
        project_path: Path,
        symbol_kind: Optional[str] = None,
        max_results: Optional[int] = None
    ) -> list[SymbolResult]:
        """
        Recherche un symbole par nom/pattern dans le projet.
        Retourne liste de SymbolResult avec signatures et références.
        """
        cache_key = f"{project_path}:{query}:{symbol_kind}"
        if cache_key in self._symbol_cache:
            logger.debug(f"Cache hit for {cache_key}")
            return self._symbol_cache[cache_key]
        
        req = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {
                "name": "find_symbol",
                "arguments": {
                    "query": query,
                    "path": str(project_path),
                    "kind": symbol_kind,
                    "max_results": max_results or self.config.max_symbols_per_call
                }
            }
        }
        
        await self._send_request(req)
        response = await asyncio.wait_for(
            self._read_response(),
            timeout=self.config.request_timeout_sec
        )
        
        results = self._parse_find_symbol_response(response)
        self._symbol_cache[cache_key] = results
        return results
    
    async def get_references(
        self,
        symbol: SymbolResult,
        project_path: Path
    ) -> list[str]:
        """Récupère les références (callers) d'un symbole."""
        req = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {
                "name": "find_references",
                "arguments": {
                    "symbol": symbol.name,
                    "file_path": symbol.file_path,
                    "line": symbol.line_start,
                    "path": str(project_path)
                }
            }
        }
        await self._send_request(req)
        response = await asyncio.wait_for(
            self._read_response(),
            timeout=self.config.request_timeout_sec
        )
        return self._parse_references_response(response)
    
    async def get_symbol_context(
        self,
        symbol: SymbolResult,
        project_path: Path,
        include_body: bool = True,
        context_lines: int = 20
    ) -> SymbolResult:
        """
        Enrichit un symbole avec son corps source et références.
        C'est la fonction principale pour remplacer Read fichier complet.
        """
        if include_body and not symbol.source_snippet:
            # Lire seulement les lignes nécessaires
            snippet = await self._read_file_range(
                project_path / symbol.file_path,
                symbol.line_start - context_lines,
                symbol.line_end + context_lines
            )
            symbol.source_snippet = snippet
        
        if not symbol.references:
            symbol.references = await self.get_references(symbol, project_path)
        
        return symbol
    
    async def _read_file_range(self, file_path: Path, start: int, end: int) -> str:
        """Lit une plage de lignes d'un fichier (fallback local)."""
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.splitlines()
            start = max(0, start - 1)
            end = min(len(lines), end)
            return "\n".join(lines[start:end])
        except Exception as e:
            logger.warning(f"Could not read file range: {e}")
            return ""
    
    def _parse_find_symbol_response(self, response: dict) -> list[SymbolResult]:
        """Parse la réponse find_symbol de Serena."""
        results = []
        try:
            data = response.get("result", {})
            for item in data.get("symbols", []):
                results.append(SymbolResult(
                    name=item.get("name", ""),
                    kind=item.get("kind", "unknown"),
                    file_path=item.get("file_path", ""),
                    line_start=item.get("line_start", 0),
                    line_end=item.get("line_end", 0),
                    signature=item.get("signature", ""),
                    docstring=item.get("docstring"),
                ))
        except Exception as e:
            logger.error(f"Parse error find_symbol: {e}")
        return results
    
    def _parse_references_response(self, response: dict) -> list[str]:
        """Parse la réponse find_references."""
        refs = []
        try:
            data = response.get("result", {})
            for item in data.get("references", []):
                refs.append(f"{item['file_path']}:{item['line']}")
        except Exception as e:
            logger.error(f"Parse error references: {e}")
        return refs
    
    def clear_cache(self):
        """Vide le cache symbolique."""
        self._symbol_cache.clear()


async def demo():
    """Demo rapide du client."""
    logging.basicConfig(level=logging.INFO)
    client = SerenaMCPClient()
    
    if await client.start():
        try:
            project = Path.cwd()
            symbols = await client.find_symbol("simulate", project, "function")
            for s in symbols:
                enriched = await client.get_symbol_context(s, project)
                print(f"Found: {enriched.name} in {enriched.file_path}:{enriched.line_start}")
                print(f"  Signature: {enriched.signature}")
                if enriched.source_snippet:
                    print(f"  Body: {enriched.source_snippet[:200]}...")
        finally:
            await client.stop()
    else:
        print("Serena MCP not available - install with: pip install serena-mcp")


if __name__ == "__main__":
    asyncio.run(demo())