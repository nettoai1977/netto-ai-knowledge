"""
Memory Manager Module for Self-Organizing Agent Memory System
Handles extraction of memory cells from interactions and scene consolidation

VERSION: 1.1 - Fixed scene consolidation to properly store summaries
"""

import json
import re
import threading
from typing import List, Dict, Optional, Callable
from memory_db import MemoryDB


class MemoryManager:
    """Manages memory extraction, storage, and consolidation"""

    def __init__(self, db: MemoryDB, llm_provider: Optional[Callable] = None):
        """
        Initialize memory manager

        Args:
            db: MemoryDB instance
            llm_provider: Optional LLM function with signature: (prompt: str, temperature: float, max_tokens: int) -> str
                          If not provided, uses simple rule-based extraction
        """
        self.db = db
        self.llm_provider = llm_provider
        self._lock = threading.Lock()  # Thread-safe updates

        # Extraction prompt template
        self.extraction_prompt = """
Convert this interaction into structured memory cells.

Return ONLY a JSON array with objects containing:
- scene: Topic identifier (e.g., "week-5-cron", "user-preferences")
- cell_type: One of [fact, plan, preference, decision, task, risk]
- salience: Float 0-1 (higher = more important, 0.9+ = critical)
- content: Compressed, factual representation (max 50 words)

User: {user}
Assistant: {assistant}

Remember: Return ONLY the JSON array, nothing else.
"""

        # Consolidation prompt template
        self.consolidation_prompt = """
Summarize these memory cells into a stable, reusable scene summary (under 100 words).

Scene: {scene}

Cells:
{cells}

Focus on:
- Key facts and decisions
- Important plans and tasks
- Critical preferences and risks
"""

    def extract_cells(self, user: str, assistant: str) -> List[Dict]:
        """
        Extract memory cells from user-assistant interaction

        Args:
            user: User message
            assistant: Assistant response

        Returns:
            List of memory cell dictionaries
        """
        if self.llm_provider:
            # Use LLM for extraction
            return self._extract_with_llm(user, assistant)
        else:
            # Use rule-based extraction (fallback)
            return self._extract_rules(user, assistant)

    def _extract_with_llm(self, user: str, assistant: str) -> List[Dict]:
        """Extract cells using LLM"""
        prompt = self.extraction_prompt.format(
            user=user,
            assistant=assistant
        )

        try:
            raw_result = self.llm_provider(prompt, temperature=0.1, max_tokens=500)

            # Clean markdown code blocks
            raw_result = re.sub(r"```json|```", "", raw_result).strip()

            cells = json.loads(raw_result)
            return cells if isinstance(cells, list) else []

        except Exception as e:
            # Fallback to rule-based if LLM fails
            print(f"LLM extraction failed: {e}, using rule-based approach")
            return self._extract_rules(user, assistant)

    def _extract_rules(self, user: str, assistant: str) -> List[Dict]:
        """Rule-based extraction (simple fallback)"""
        cells = []

        # Detect scene/topics from interaction
        text = f"{user} {assistant}".lower()

        scene = "general"

        if "week" in text and ("5" in text or "week 5" in text):
            scene = "week-5-tasks"
        elif "user" in text and "prefer" in text:
            scene = "user-preferences"
        elif "task" in text or "todo" in text:
            scene = "tasks"
        elif "agent" in text:
            scene = "agent-army"
        elif "cron" in text:
            scene = "automation"

        # Detect cell types
        cell_type = "fact"
        salience = 0.7

        if "plan" in text or "will" in text or "going to" in text:
            cell_type = "plan"
            salience = 0.8
        elif "prefer" in text or "like" in text or "want" in text:
            cell_type = "preference"
            salience = 0.85
        elif "decide" in text or "choose" in text or "select" in text:
            cell_type = "decision"
            salience = 0.9
        elif "task" in text or "do" in text:
            cell_type = "task"
            salience = 0.8
        elif "risk" in text or "limitation" in text or "concern" in text:
            cell_type = "risk"
            salience = 0.75

        # Compress content
        content = self._compress_content(f"{user} {assistant}")

        if content:  # Only add if we got meaningful content
            cells.append({
                "scene": scene,
                "cell_type": cell_type,
                "salience": salience,
                "content": content
            })

        return cells

    def _compress_content(self, text: str, max_words: int = 50) -> Optional[str]:
        """Compress text to key facts"""
        words = text.split()
        if len(words) <= max_words:
            return " ".join(words)

        # Simple truncation for now (could use LLM for better compression)
        return " ".join(words[:max_words]) + "..."

    def consolidate_scene(self, scene: str) -> Optional[str]:
        """
        Consolidate all cells in a scene into a summary (FIXED VERSION - stores summary)

        Args:
            scene: Scene identifier

        Returns:
            Consolidated summary or None
        """
        # Get all cells for scene
        cells = self.db.get_cells_by_scene(scene)

        if not cells:
            return None

        # Unpack content
        cell_contents = []
        for cell in cells:
            content_json = json.loads(cell["content"])
            cell_contents.append(
                f"{cell_type_to_emoji(cell['cell_type'])} (salience={cell['salience']}) {content_json}"
            )

        # Generate summary
        if self.llm_provider:
            # Use LLM for consolidation
            summary = self._consolidate_with_llm(scene, cell_contents)
        else:
            # Use simple concatenation (fallback)
            summary = self._consolidate_simple(cell_contents)

        # Store summary in database
        if summary:
            self.db.upsert_scene(scene, summary)

        return summary

    def _consolidate_with_llm(self, scene: str, cells: List[str]) -> str:
        """Consolidate scene using LLM"""
        prompt = self.consolidation_prompt.format(
            scene=scene,
            cells="\n".join(cells)
        )

        try:
            return self.llm_provider(prompt, temperature=0.05, max_tokens=200)
        except Exception as e:
            print(f"LLM consolidation failed: {e}, using simple approach")
            return self._consolidate_simple(cells)

    def _consolidate_simple(self, cells: List[str]) -> str:
        """Simple consolidation by concatenation"""
        return " | ".join(cells)[:200]

    def update(self, user: str, assistant: str) -> List[int]:
        """
        Update memory with new interaction

        Args:
            user: User message
            assistant: Assistant response

        Returns:
            List of inserted cell IDs
        """
        with self._lock:  # Thread-safe
            cells = self.extract_cells(user, assistant)

            inserted_ids = []

            for cell in cells:
                # Insert cell
                cell_id = self.db.insert_cell(cell)
                inserted_ids.append(cell_id)

            # Consolidate scenes
            scenes = set(c["scene"] for c in cells)
            for scene in scenes:
                self.consolidate_scene(scene)

            return inserted_ids

    def retrieve_context_for_query(self, query: str, limit: int = 6) -> str:
        """
        Retrieve relevant context for a query

        Args:
            query: User query
            limit: Maximum number of cells

        Returns:
            Formatted context string
        """
        cells = self.db.retrieve_context(query, limit)

        # Group by scene
        scenes = set(c["scene"] for c in cells)

        summaries = []

        for scene in scenes:
            summary = self.db.retrieve_scene_summary(scene)
            if summary:
                summaries.append(f"[Scene: {scene}]\n{summary}")

        return "\n\n".join(summaries)


def cell_type_to_emoji(cell_type: str) -> str:
    """Convert cell type to emoji for display"""
    emojis = {
        "fact": "📌",
        "plan": "📋",
        "preference": "❤️",
        "decision": "✅",
        "task": "⏰",
        "risk": "⚠️"
    }
    return emojis.get(cell_type, "📝")


# Convenience function for quick memory manager access
_memory_manager_instance = None


def get_memory_manager(llm_provider: Optional[Callable] = None) -> MemoryManager:
    """
    Get singleton instance of memory manager

    Args:
        llm_provider: Optional LLM function

    Returns:
        MemoryManager instance
    """
    global _memory_manager_instance

    if _memory_manager_instance is None:
        from memory_db import get_memory_db
        db = get_memory_db()
        _memory_manager_instance = MemoryManager(db, llm_provider)

    return _memory_manager_instance
