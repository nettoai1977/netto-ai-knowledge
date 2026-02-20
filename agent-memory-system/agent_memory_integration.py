"""
Agent Memory Integration Module
Integrates self-organizing memory system with OpenClaw/Nanobot
"""

import os
import sys
from typing import Optional, Callable

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from memory_db import get_memory_db, MemoryDB
from memory_manager import get_memory_manager, MemoryManager, cell_type_to_emoji


class AgentMemoryIntegration:
    """
    Integration layer between self-organizing memory and OpenClaw/Nanobot

    Usage:
        # Initialize with LLM provider (optional, uses NVIDIA GLM if available)
        memory = AgentMemoryIntegration(llm_provider=llm_function)

        # Update memory with interaction
        memory.update(user_message, assistant_response)

        # Retrieve context for queries
        context = memory.retrieve_context(query)
    """

    def __init__(
        self,
        llm_provider: Optional[Callable] = None,
        db_path: Optional[str] = None
    ):
        """
        Initialize agent memory integration

        Args:
            llm_provider: Optional LLM function with signature: (prompt: str, temperature: float, max_tokens: int) -> str
                         If not provided, uses rule-based extraction
            db_path: Optional path to SQLite database
        """
        self.db = get_memory_db(db_path)
        self.manager = MemoryManager(self.db, llm_provider)

    def update(self, user: str, assistant: str) -> int:
        """
        Update memory with new user-assistant interaction

        Args:
            user: User message
            assistant: Assistant response

        Returns:
            Number of memory cells inserted
        """
        cell_ids = self.manager.update(user, assistant)
        return len(cell_ids)

    def retrieve_context(self, query: str, limit: int = 6) -> str:
        """
        Retrieve relevant context for a query

        Args:
            query: User query or context
            limit: Maximum number of memory cells to retrieve

        Returns:
            Formatted context string with scene summaries
        """
        context = self.manager.retrieve_context_for_query(query, limit)

        if not context:
            return "No relevant memory found."

        return f"""
🧠 MEMORY RETRIEVED:

{context}

---
Memory retrieval completed
        """.strip()

    def get_statistics(self) -> dict:
        """
        Get memory statistics

        Returns:
            Dict with statistics
        """
        return self.db.get_statistics()

    def list_all_scenes(self) -> str:
        """
        List all scenes in memory

        Returns:
            Formatted string with scene summaries
        """
        scenes = self.db.get_all_scenes()

        if not scenes:
            return "No scenes found in memory."

        output = "📚 MEMORY SCENES:\n\n"

        for scene in scenes:
            output += f"🏷️ {scene['scene']}\n"
            output += f"   {scene['summary'][:150]}{'...' if len(scene['summary']) > 150 else ''}\n\n"

        return output.strip()

    def search_by_type(self, cell_type: str, limit: int = 10) -> str:
        """
        Search memory cells by type

        Args:
            cell_type: One of [fact, plan, preference, decision, task, risk]
            limit: Maximum number of results

        Returns:
            Formatted string with matching cells
        """
        valid_types = ["fact", "plan", "preference", "decision", "task", "risk"]

        if cell_type not in valid_types:
            return f"Invalid cell_type. Must be one of: {', '.join(valid_types)}"

        cells = self.db.search_by_type(cell_type, limit)

        if not cells:
            return f"No {cell_type} cells found in memory."

        emoji = cell_type_to_emoji(cell_type)
        output = f"{emoji} {cell_type.upper()} CELLS:\n\n"

        for cell in cells:
            content = " ".join(cell["content"].split()[:30])  # Truncate
            output += f"• [{cell['scene']}] {content}...\n\n"

        return output.strip()

    def get_scene_details(self, scene_name: str) -> str:
        """
        Get details for a specific scene

        Args:
            scene_name: Scene identifier

        Returns:
            Formatted string with scene details
        """
        scene_summary = self.db.retrieve_scene_summary(scene_name)

        if not scene_summary:
            return f"Scene '{scene_name}' not found."

        cells = self.db.get_cells_by_scene(scene_name)

        output = f"🏷️ SCENE: {scene_name}\n\n"
        output += f"📝 SUMMARY:\n{scene_summary}\n\n"

        if cells:
            output += f"📌 CELLS ({len(cells)}):\n"
            for cell in cells[:20]:  # Limit display
                emoji = cell_type_to_emoji(cell["cell_type"])
                content = " ".join(cell["content"].split()[:25])
                output += f"{emoji} [{cell['cell_type']}] {content}...\n"

        return output.strip()

    def search_memory(self, query: str, limit: int = 6) -> str:
        """
        Search memory for a query

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            Formatted search results
        """
        cells = self.db.retrieve_context(query, limit)

        if not cells:
            return f"No results for query: '{query}'"

        output = f"🔍 SEARCH RESULTS: '{query}'\n\n"

        for cell in cells:
            emoji = cell_type_to_emoji(cell["cell_type"])
            content = " ".join(cell["content"].split()[:30])
            output += f"{emoji} [{cell['scene']}] {content}... \n"

        return output.strip()

    def export_memory_backup(self) -> str:
        """
        Export memory data as JSON backup

        Returns:
            JSON string of all memory data
        """
        import json
        from datetime import datetime

        scenes = self.db.get_all_scenes()

        backup_data = {
            "exported_at": datetime.utcnow().isoformat(),
            "total_scenes": len(scenes),
            "scenes": scenes
        }

        return json.dumps(backup_data, indent=2)


# Singleton instance
_memory_integration_instance = None


def get_agent_memory(
    llm_provider: Optional[Callable] = None,
    db_path: Optional[str] = None
) -> AgentMemoryIntegration:
    """
    Get singleton instance of agent memory integration

    Args:
        llm_provider: Optional LLM function
        db_path: Optional database path

    Returns:
        AgentMemoryIntegration instance
    """
    global _memory_integration_instance

    if _memory_integration_instance is None:
        _memory_integration_instance = AgentMemoryIntegration(
            llm_provider=llm_provider,
            db_path=db_path
        )

    return _memory_integration_instance


# --- Example Usage ---

def example_usage():
    """Example usage of agent memory integration"""

    # Initialize (without LLM provider for now - uses rule-based extraction)
    memory = get_agent_memory()

    # Update memory with interaction
    print("Updating memory...")
    memory.update(
        user="I want to deploy cron automation for daily briefings",
        assistant="I'll help you set up daily (8:00 AM) and weekly (Sunday 10:00 AM) cron jobs."
    )

    # Retrieve context
    print("\nRetrieving context...")
    context = memory.retrieve_context("cron automation")
    print(context)

    # Get statistics
    print("\nMemory statistics:")
    stats = memory.get_statistics()
    print(f"Total cells: {stats['total_cells']}")
    print(f"Total scenes: {stats['total_scenes']}")
    print(f"Cells by type: {stats['cells_by_type']}")

    # List scenes
    print("\n" + memory.list_all_scenes())

    # Search by type
    print("\n" + memory.search_by_type("task"))

    # Search memory
    print("\n" + memory.search_memory("automation"))


if __name__ == "__main__":
    example_usage()
