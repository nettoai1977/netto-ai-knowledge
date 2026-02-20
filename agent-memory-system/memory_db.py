"""
Memory Database Module for Self-Organizing Agent Memory System
Implements SQLite database with FTS5 full-text search for structured memory storage
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os


class MemoryDB:
    """Structured memory database with FTS5 full-text search"""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize memory database

        Args:
            db_path: Path to SQLite database file. If None, creates in workspace
        """
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(__file__),
                "agent_memory.db"
            )

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        """Initialize memory database schema"""
        # Memory cells table - atomic knowledge units
        self.db.execute("""
        CREATE TABLE IF NOT EXISTS mem_cells (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scene TEXT NOT NULL,
            cell_type TEXT NOT NULL,
            salience REAL NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)

        # Scenes table - consolidated scene summaries
        self.db.execute("""
        CREATE TABLE IF NOT EXISTS mem_scenes (
            scene TEXT PRIMARY KEY,
            summary TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """)

        # Full-text search index for fast retrieval
        self.db.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS mem_cells_fts
        USING fts5(content, scene, cell_type)
        """)

        # Index on salience for fallback retrieval
        self.db.execute("""
        CREATE INDEX IF NOT EXISTS idx_salience
        ON mem_cells(salience DESC)
        """)

        self.db.commit()

    def insert_cell(self, cell: Dict) -> int:
        """
        Insert a memory cell

        Args:
            cell: Dictionary with keys: scene, cell_type, salience, content

        Returns:
            ID of inserted cell
        """
        cursor = self.db.execute(
            "INSERT INTO mem_cells (scene, cell_type, salience, content, created_at) VALUES (?,?,?,?,?)",
            (
                cell["scene"],
                cell["cell_type"],
                cell["salience"],
                json.dumps(cell["content"]),
                datetime.utcnow().isoformat()
            )
        )

        # Also insert into full-text search index
        self.db.execute(
            "INSERT INTO mem_cells_fts (content, scene, cell_type) VALUES (?,?,?)",
            (
                json.dumps(cell["content"]),
                cell["scene"],
                cell["cell_type"]
            )
        )

        self.db.commit()
        return cursor.lastrowid

    def get_scene(self, scene: str) -> Optional[Dict]:
        """
        Get scene by name

        Args:
            scene: Scene identifier

        Returns:
            Scene dict or None
        """
        row = self.db.execute(
            "SELECT * FROM mem_scenes WHERE scene=?",
            (scene,)
        ).fetchone()

        return dict(row) if row else None

    def upsert_scene(self, scene: str, summary: str) -> None:
        """
        Insert or update scene summary

        Args:
            scene: Scene identifier
            summary: Consolidated scene summary
        """
        self.db.execute("""
        INSERT INTO mem_scenes VALUES (?,?,?)
        ON CONFLICT(scene) DO UPDATE SET
            summary=excluded.summary,
            updated_at=excluded.updated_at
        """, (scene, summary, datetime.utcnow().isoformat()))
        self.db.commit()

    def retrieve_scene_summary(self, scene: str) -> str:
        """
        Retrieve consolidated scene summary

        Args:
            scene: Scene identifier

        Returns:
            Scene summary or empty string
        """
        row = self.get_scene(scene)
        return row["summary"] if row else ""

    def retrieve_context(self, query: str, limit: int = 6) -> List[Dict]:
        """
        Retrieve relevant memory cells using full-text search

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching memory cells
        """
        import re

        # Tokenize query for FTS
        tokens = re.findall(r"[a-zA-Z0-9]+", query)
        if not tokens:
            return []

        fts_query = " OR ".join(tokens)

        # Try full-text search first
        rows = self.db.execute("""
        SELECT mem_cells.scene, mem_cells.content, mem_cells.salience, mem_cells.cell_type
        FROM mem_cells_fts
        JOIN mem_cells ON mem_cells.id = mem_cells_fts.rowid
        WHERE mem_cells_fts MATCH ?
        LIMIT ?
        """, (fts_query, limit)).fetchall()

        # Fallback to salience-based retrieval
        if not rows:
            rows = self.db.execute("""
            SELECT scene, content, salience, cell_type
            FROM mem_cells
            ORDER BY salience DESC
            LIMIT ?
            """, (limit,)).fetchall()

        return [dict(row) for row in rows]

    def get_all_scenes(self) -> List[Dict]:
        """
        Get all scenes

        Returns:
            List of scene dictionaries
        """
        rows = self.db.execute("SELECT * FROM mem_scenes").fetchall()
        return [dict(row) for row in rows]

    def get_cells_by_scene(self, scene: str, limit: int = 100) -> List[Dict]:
        """
        Get all cells for a scene

        Args:
            scene: Scene identifier
            limit: Maximum number of cells

        Returns:
            List of memory cells for the scene
        """
        rows = self.db.execute("""
        SELECT * FROM mem_cells
        WHERE scene=?
        ORDER BY salience DESC
        LIMIT ?
        """, (scene, limit)).fetchall()

        return [dict(row) for row in rows]

    def search_by_type(self, cell_type: str, limit: int = 20) -> List[Dict]:
        """
        Search cells by type

        Args:
            cell_type: One of [fact, plan, preference, decision, task, risk]
            limit: Maximum number of results

        Returns:
            List of memory cells
        """
        rows = self.db.execute("""
        SELECT * FROM mem_cells
        WHERE cell_type=?
        ORDER BY salience DESC
        LIMIT ?
        """, (cell_type, limit)).fetchall()

        return [dict(row) for row in rows]

    def get_statistics(self) -> Dict:
        """
        Get database statistics

        Returns:
            Dict with stats: total_cells, total_scenes, cells_by_type
        """
        total_cells = self.db.execute("SELECT COUNT(*) FROM mem_cells").fetchone()[0]
        total_scenes = self.db.execute("SELECT COUNT(*) FROM mem_scenes").fetchone()[0]

        # Count cells by type
        cells_by_type = {}
        for cell_type in ["fact", "plan", "preference", "decision", "task", "risk"]:
            count = self.db.execute(
                "SELECT COUNT(*) FROM mem_cells WHERE cell_type=?",
                (cell_type,)
            ).fetchone()[0]
            cells_by_type[cell_type] = count

        return {
            "total_cells": total_cells,
            "total_scenes": total_scenes,
            "cells_by_type": cells_by_type
        }

    def close(self):
        """Close database connection"""
        self.db.close()


# Convenience function for quick database access
_memory_db_instance = None


def get_memory_db(db_path: Optional[str] = None) -> MemoryDB:
    """
    Get singleton instance of memory database

    Args:
        db_path: Database path

    Returns:
        MemoryDB instance
    """
    global _memory_db_instance

    if _memory_db_instance is None:
        _memory_db_instance = MemoryDB(db_path)

    return _memory_db_instance
