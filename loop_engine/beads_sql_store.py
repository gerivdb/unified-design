#!/usr/bin/env python3
"""
beads_sql_store.py - Mémoire SQL versionnée (SQLite+WAL) pour graphe d'insights
Remplace TODO.md par stockage structuré + compression 70% + survie reset/rotation.
"""

from __future__ import annotations

import hashlib
import json
import logging
import sqlite3
import time
import uuid
import zlib
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class InsightNode:
    """Nœud d'insight dans le graphe Beads."""
    id: str
    type: str  # observation | decision | pattern | hypothesis | result
    content: str  # JSON compressé (hex)
    content_hash: str
    compression_ratio: float
    parent_ids: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    session_id: str = ""
    account_id: str = ""
    version: int = 1


@dataclass
class InsightEdge:
    """Arête entre insights (relation sémantique)."""
    id: str
    source_id: str
    target_id: str
    relation: str  # derives_from | contradicts | supports | refines | supersedes
    weight: float = 1.0
    created_at: float = field(default_factory=time.time)


class BeadsSQLStore:
    """
    Stockage SQL versionné pour insights (remplace Markdown TODO).
    - SQLite + WAL pour concurrence
    - Compression zlib ~70% sur content
    - Graphe relationnel complet
    - Survie: context_reset + account_rotation
    - Index full-text + B-tree
    """
    
    SCHEMA_VERSION = 1
    COMPRESSION_TARGET = 0.70
    
    def __init__(self, db_path: Path, account_id: str = "default"):
        self.db_path = db_path
        self.account_id = account_id
        self.session_id = str(uuid.uuid4())[:8]
        self._init_db()
    
    def _init_db(self):
        """Initialise la base avec schema Beads."""
        with self._conn() as conn:
            # Table nœuds insights
            conn.execute("""
                CREATE TABLE IF NOT EXISTS insights (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    content TEXT NOT NULL,           -- JSON compressé (hex zlib)
                    content_hash TEXT NOT NULL,      -- SHA256 du content original (16 chars)
                    compression_ratio REAL NOT NULL,
                    parent_ids TEXT NOT NULL,        -- JSON array
                    tags TEXT NOT NULL,              -- JSON array
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    session_id TEXT NOT NULL,
                    account_id TEXT NOT NULL,
                    version INTEGER NOT NULL DEFAULT 1
                )
            """)
            
            # Table arêtes (graphe)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS insight_edges (
                    id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    relation TEXT NOT NULL,
                    weight REAL NOT NULL DEFAULT 1.0,
                    created_at REAL NOT NULL,
                    FOREIGN KEY (source_id) REFERENCES insights(id),
                    FOREIGN KEY (target_id) REFERENCES insights(id)
                )
            """)
            
            # Index pour performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_insights_account ON insights(account_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_insights_session ON insights(session_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_insights_type ON insights(type)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_insights_created ON insights(created_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_insights_hash ON insights(content_hash)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_source ON insight_edges(source_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_target ON insight_edges(target_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_relation ON insight_edges(relation)")
            
            # Table meta pour schema version
            conn.execute("""
                CREATE TABLE IF NOT EXISTS meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)
            conn.execute(
                "INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)",
                ("schema_version", str(self.SCHEMA_VERSION))
            )
            conn.execute(
                "INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)",
                ("account_id", self.account_id)
            )
            
            # Activer WAL mode pour concurrence
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA cache_size=-32768")  # 32MB cache
            conn.execute("PRAGMA temp_store=memory")
            
            conn.commit()
    
    @contextmanager
    def _conn(self):
        """Context manager pour connexion DB."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def _compress(self, data: dict) -> tuple[str, str, float]:
        """Compresse un dict JSON avec zlib."""
        json_str = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        original_bytes = json_str.encode("utf-8")
        compressed = zlib.compress(original_bytes, level=6)
        ratio = len(compressed) / len(original_bytes) if original_bytes else 1.0
        content_hash = hashlib.sha256(original_bytes).hexdigest()[:16]
        return compressed.hex(), content_hash, ratio
    
    def _decompress(self, compressed_hex: str) -> dict:
        """Décompresse vers dict."""
        compressed = bytes.fromhex(compressed_hex)
        return json.loads(zlib.decompress(compressed).decode("utf-8"))
    
    def add_insight(
        self,
        insight_type: str,
        content: dict,
        parent_ids: list[str] = None,
        tags: list[str] = None
    ) -> InsightNode:
        """Ajoute un insight au graphe."""
        parent_ids = parent_ids or []
        tags = tags or []
        
        compressed, content_hash, ratio = self._compress(content)
        
        node = InsightNode(
            id=str(uuid.uuid4())[:12],
            type=insight_type,
            content=compressed,
            content_hash=content_hash,
            compression_ratio=ratio,
            parent_ids=parent_ids,
            tags=tags,
            session_id=self.session_id,
            account_id=self.account_id
        )
        
        with self._conn() as conn:
            conn.execute("""
                INSERT INTO insights (id, type, content, content_hash, compression_ratio,
                                     parent_ids, tags, created_at, updated_at,
                                     session_id, account_id, version)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                node.id, node.type, node.content, node.content_hash, node.compression_ratio,
                json.dumps(node.parent_ids), json.dumps(node.tags),
                node.created_at, node.updated_at,
                node.session_id, node.account_id, node.version
            ))
            
            # Arêtes vers parents
            for pid in parent_ids:
                edge = InsightEdge(
                    id=str(uuid.uuid4())[:12],
                    source_id=pid,
                    target_id=node.id,
                    relation="derives_from"
                )
                conn.execute("""
                    INSERT INTO insight_edges (id, source_id, target_id, relation, weight, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (edge.id, edge.source_id, edge.target_id, edge.relation, edge.weight, edge.created_at))
            
            conn.commit()
        
        logger.info(f"Added insight {node.id} ({insight_type}) compression: {ratio:.1%}")
        return node
    
    def get_insight(self, insight_id: str) -> Optional[InsightNode]:
        """Récupère un insight par ID."""
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM insights WHERE id = ?", (insight_id,)).fetchone()
            if not row:
                return None
            return self._row_to_node(row)
    
    def query_insights(
        self,
        insight_type: str = None,
        tags: list[str] = None,
        session_id: str = None,
        account_id: str = None,
        since: float = None,
        limit: int = 100
    ) -> list[InsightNode]:
        """Recherche insights avec filtres."""
        conditions = []
        params = []
        
        if insight_type:
            conditions.append("type = ?")
            params.append(insight_type)
        if tags:
            for tag in tags:
                conditions.append("tags LIKE ?")
                params.append(f"%{tag}%")
        if session_id:
            conditions.append("session_id = ?")
            params.append(session_id)
        if account_id:
            conditions.append("account_id = ?")
            params.append(account_id)
        else:
            conditions.append("account_id = ?")
            params.append(self.account_id)
        if since:
            conditions.append("created_at >= ?")
            params.append(since)
        
        where = "WHERE " + " AND ".join(conditions) if conditions else ""
        sql = f"SELECT * FROM insights {where} ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        
        with self._conn() as conn:
            rows = conn.execute(sql, params).fetchall()
            return [self._row_to_node(r) for r in rows]
    
    def get_related(
        self,
        insight_id: str,
        relation: str = None,
        direction: str = "both"  # outgoing | incoming | both
    ) -> list[tuple[InsightNode, InsightEdge]]:
        """Récupère insights liés (graphe)."""
        conditions = []
        params = []
        
        if direction in ("outgoing", "both"):
            conditions.append("source_id = ?")
            params.append(insight_id)
        if direction in ("incoming", "both"):
            conditions.append("target_id = ?")
            params.append(insight_id)
        if relation:
            conditions.append("relation = ?")
            params.append(relation)
        
        where = "WHERE " + " OR ".join(conditions)
        sql = f"SELECT * FROM insight_edges {where}"
        
        results = []
        with self._conn() as conn:
            edges = conn.execute(sql, params).fetchall()
            for edge_row in edges:
                edge = InsightEdge(
                    id=edge_row["id"],
                    source_id=edge_row["source_id"],
                    target_id=edge_row["target_id"],
                    relation=edge_row["relation"],
                    weight=edge_row["weight"],
                    created_at=edge_row["created_at"]
                )
                # Récupérer l'autre nœud
                other_id = edge.target_id if edge.source_id == insight_id else edge.source_id
                node = self.get_insight(other_id)
                if node:
                    results.append((node, edge))
        return results
    
    def add_relation(
        self,
        source_id: str,
        target_id: str,
        relation: str,
        weight: float = 1.0
    ) -> InsightEdge:
        """Ajoute une relation entre insights."""
        edge = InsightEdge(
            id=str(uuid.uuid4())[:12],
            source_id=source_id,
            target_id=target_id,
            relation=relation,
            weight=weight
        )
        with self._conn() as conn:
            conn.execute("""
                INSERT INTO insight_edges (id, source_id, target_id, relation, weight, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (edge.id, edge.source_id, edge.target_id, edge.relation, edge.weight, edge.created_at))
            conn.commit()
        return edge
    
    def get_stats(self) -> dict:
        """Statistiques du store."""
        with self._conn() as conn:
            total = conn.execute("SELECT COUNT(*) FROM insights").fetchone()[0]
            by_type = dict(conn.execute("SELECT type, COUNT(*) FROM insights GROUP BY type").fetchall())
            total_edges = conn.execute("SELECT COUNT(*) FROM insight_edges").fetchone()[0]
            
            avg_ratio = conn.execute("SELECT AVG(compression_ratio) FROM insights").fetchone()[0] or 0
            
            db_size = self.db_path.stat().st_size if self.db_path.exists() else 0
            
            return {
                "total_insights": total,
                "by_type": by_type,
                "total_edges": total_edges,
                "avg_compression_ratio": round(avg_ratio, 3),
                "db_size_bytes": db_size,
                "db_size_mb": round(db_size / 1024 / 1024, 2),
                "account_id": self.account_id,
                "current_session": self.session_id
            }
    
    def survive_reset(self, new_session_id: str = None, new_account_id: str = None) -> str:
        """
        Simule la survie après reset contexte / rotation compte.
        Les insights persistent car liés à account_id, pas session.
        """
        old_session = self.session_id
        self.session_id = new_session_id or str(uuid.uuid4())[:8]
        if new_account_id:
            self.account_id = new_account_id
            with self._conn() as conn:
                conn.execute("UPDATE meta SET value = ? WHERE key = 'account_id'", (self.account_id,))
                conn.commit()
        logger.info(f"Survived reset: session {old_session} -> {self.session_id}, account: {self.account_id}")
        return self.session_id
    
    def export_graph(self, account_id: str = None) -> dict:
        """Exporte le graphe complet pour backup/analyse."""
        aid = account_id or self.account_id
        with self._conn() as conn:
            nodes = conn.execute("SELECT * FROM insights WHERE account_id = ?", (aid,)).fetchall()
            edges = conn.execute("""
                SELECT e.* FROM insight_edges e
                JOIN insights i ON e.source_id = i.id
                WHERE i.account_id = ?
            """, (aid,)).fetchall()
            
            return {
                "account_id": aid,
                "exported_at": datetime.now().isoformat(),
                "nodes": [dict(n) for n in nodes],
                "edges": [dict(e) for e in edges]
            }
    
    def _row_to_node(self, row: sqlite3.Row) -> InsightNode:
        return InsightNode(
            id=row["id"],
            type=row["type"],
            content=row["content"],
            content_hash=row["content_hash"],
            compression_ratio=row["compression_ratio"],
            parent_ids=json.loads(row["parent_ids"]),
            tags=json.loads(row["tags"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            session_id=row["session_id"],
            account_id=row["account_id"],
            version=row["version"]
        )


def demo():
    """Demo du store Beads."""
    import tempfile
    logging.basicConfig(level=logging.INFO)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "beads.db"
        store = BeadsSQLStore(db_path, account_id="demo-account")
        
        # Ajouter insights
        obs1 = store.add_insight("observation", {
            "context": "Reading Graph of Loops paper",
            "finding": "Serena MCP saves 16k tokens by symbol retrieval",
            "confidence": 0.9
        }, tags=["context-recovery", "serena"])
        
        dec1 = store.add_insight("decision", {
            "action": "Implement ATOM-049 symbol-retrieval-mcp",
            "rationale": "Direct application of L3 Serena pattern",
            "priority": "high"
        }, parent_ids=[obs1.id], tags=["implementation", "priority-high"])
        
        pat1 = store.add_insight("pattern", {
            "name": "Agent Worktree Isolation",
            "source": "Graph of Loops G2",
            "application": "ATOM-050 agent-worktree-isolation",
            "benefits": ["no file conflicts", "dry-run merge", "parallel agents"]
        }, parent_ids=[dec1.id], tags=["isolation", "git-worktree"])
        
        res1 = store.add_insight("result", {
            "atom": "ATOM-049",
            "status": "implemented",
            "validation": "simulate.py passed",
            "token_savings": 16000
        }, parent_ids=[pat1.id], tags=["validation", "complete"])
        
        # Relations supplémentaires
        store.add_relation(obs1.id, pat1.id, "supports", 0.8)
        store.add_relation(pat1.id, res1.id, "derives_from", 1.0)
        
        # Queries
        print("\n=== All Observations ===")
        for node in store.query_insights(insight_type="observation"):
            print(f"  {node.id}: {store._decompress(node.content)['finding'][:60]}...")
        
        print("\n=== Graph from observation ===")
        for node, edge in store.get_related(obs1.id):
            print(f"  {edge.relation} -> {node.id} ({node.type})")
        
        # Stats
        print("\n=== Stats ===")
        stats = store.get_stats()
        for k, v in stats.items():
            print(f"  {k}: {v}")
        
        # Survival test
        print("\n=== Survival Test (context reset) ===")
        store.survive_reset(new_session_id="new-session-001")
        print(f"New session: {store.session_id}")
        
        recovered = store.query_insights(account_id="demo-account")
        print(f"Insights after reset: {len(recovered)}")


if __name__ == "__main__":
    demo()