"""
Historical Data Import Script
Imports data from MEMORY.md into self-organizing memory system
"""

import os
import re
import json
from typing import List, Dict, Optional
from datetime import datetime

# Import memory system
from memory_db import get_memory_db, MemoryDB
from memory_manager import MemoryManager


def parse_memory_markdown(memory_path: str) -> List[Dict]:
    """
    Parse MEMORY.md and extract structured memories

    Args:
        memory_path: Path to MEMORY.md file

    Returns:
        List of memory cell dictionaries
    """
    cells = []

    with open(memory_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract HEARTBEAT LOG section
    heartbeat_match = re.search(r'## 📋 HEARTBEAT LOG\s+(.*?)(?=\n##|\Z)', content, re.DOTALL)

    if heartbeat_match:
        heartbeat_content = heartbeat_match.group(1)

        # Extract date entries
        date_matches = re.finditer(
            r'### (\d{4}-\d{2}-\d{2}.*?)(?=### \d{4}|\Z)',
            heartbeat_content,
            re.DOTALL
        )

        for match in date_matches:
            date_section = match.group(1)
            date_line = match.group(1).split('\n')[0]

            # Determine scene from date section
            scene = "general"
            if "user" in date_section.lower() and "prefer" in date_section.lower():
                scene = "user-preferences"
            elif "sub-agent" in date_section.lower():
                scene = "subagent-capacity"
            elif "system health" in date_section.lower():
                scene = "system-health"

            # Extract facts from section
            facts = extract_facts_from_text(date_section, scene)
            cells.extend(facts)

    # Extract other structured sections
    sections = [
        ("agent-army", "Agent Army"),
        ("productivity", "Productivity"),
        ("skills", "Skills"),
    ]

    for scene_name, keyword in sections:
        pattern = rf'## [^#]*{keyword}[^\n]+\s+(.*?)(?=\n##|\Z)'
        match = re.search(pattern, content, re.DOTALL)

        if match:
            section_content = match.group(1)
            facts = extract_facts_from_text(section_content, scene_name)
            cells.extend(facts)

    return cells


def extract_facts_from_text(text: str, default_scene: str) -> List[Dict]:
    """
    Extract fact cells from text

    Args:
        text: Text content
        default_scene: Default scene identifier

    Returns:
        List of memory cell dictionaries
    """
    cells = []

    # Split into lines
    lines = text.split('\n')

    for line in lines:
        line = line.strip()

        # Skip empty lines, headers, bullet marks
        if not line or line.startswith('#') or line.startswith('*'):
            continue

        # Skip very short lines
        if len(line) < 20:
            continue

        # Determine cell type
        cell_type = "fact"
        salience = 0.7

        line_lower = line.lower()

        if any(word in line_lower for word in ["plan", "will", "going to", "next step"]):
            cell_type = "plan"
            salience = 0.8
        elif any(word in line_lower for word in ["prefer", "like", "want", "user"]):
            cell_type = "preference"
            salience = 0.85
        elif any(word in line_lower for word in ["decide", "choose", "select"]):
            cell_type = "decision"
            salience = 0.9
        elif any(word in line_lower for word in ["task", "do", "complete"]):
            cell_type = "task"
            salience = 0.8
        elif any(word in line_lower for word in ["limit", "capacity", "risk", "practical"]):
            cell_type = "risk"
            salience = 0.75

        # Compress content
        content = compress_content(line, max_words=30)

        if content:
            cells.append({
                "scene": default_scene,
                "cell_type": cell_type,
                "salience": salience,
                "content": content
            })

    return cells


def compress_content(text: str, max_words: int = 30) -> Optional[str]:
    """
    Compress text to key facts

    Args:
        text: Input text
        max_words: Maximum words

    Returns:
        Compressed content or None
    """
    words = text.split()

    # Remove markdown symbols and special chars
    words = [re.sub(r'[*_`#-]', '', word) for word in words]
    words = [word for word in words if word]

    if len(words) < 5:  # Skip too short
        return None

    if len(words) <= max_words:
        return " ".join(words)

    return " ".join(words[:max_words]) + "..."


def import_week_progress(workspace_path: str) -> List[Dict]:
    """
    Import week progress files as plan and task cells

    Args:
        workspace_path: Path to workspace directory

    Returns:
        List of memory cell dictionaries
    """
    cells = []

    # Look for week files
    week_files = []

    for root, dirs, files in os.walk(workspace_path):
        for file in files:
            if re.match(r'WEEK\d+_', file) or re.match(r'week-\d+', file):
                week_files.append(os.path.join(root, file))

    for week_file in week_files:
        with open(week_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract week number
        week_match = re.search(r'WEEK ?(\d+)', week_file, re.IGNORECASE)

        if week_match:
            week_num = week_match.group(1)
            scene = f"week-{week_num}-progress"
        else:
            # Fallback: use filename as scene
            scene = os.path.basename(week_file).replace('.md', '')


        # Extract objectives
        objectives = re.findall(r'•\s+(.*?)(?=•|\n|$)', content)

        for obj in objectives:
            obj = obj.strip()

            if len(obj) > 10:
                cells.append({
                    "scene": scene,
                    "cell_type": "task",
                    "salience": 0.8,
                    "content": obj[:50] + ("..." if len(obj) > 50 else "")
                })

    return cells


def import_from_memory_md(workspace_path: str) -> int:
    """
    Import historical data from MEMORY.md

    Args:
        workspace_path: Path to workspace directory

    Returns:
        Number of cells imported
    """
    memory_path = os.path.join(workspace_path, "MEMORY.md")

    if not os.path.exists(memory_path):
        print(f"MEMORY.md not found at: {memory_path}")
        return 0

    print("Parsing MEMORY.md...")
    cells = parse_memory_markdown(memory_path)

    print(f"Parsing week progress files...")
    week_cells = import_week_progress(workspace_path)
    cells.extend(week_cells)

    print(f"Total cells extracted: {len(cells)}")

    # Import into memory database
    print("Importing into memory database...")

    db = get_memory_db()

    imported_count = 0

    for cell in cells:
        try:
            db.insert_cell(cell)
            imported_count += 1
        except Exception as e:
            print(f"Error inserting cell: {e}")

    # Consolidate scenes
    print("Consolidating scenes...")

    scenes = set(c["scene"] for c in cells)
    manager = MemoryManager(db, llm_provider=None)

    for scene in scenes:
        try:
            manager.consolidate_scene(scene)
        except Exception as e:
            print(f"Error consolidating scene '{scene}': {e}")

    print(f"\n✅ Import complete!")
    print(f"   Cells imported: {imported_count}")
    print(f"   Scenes consolidated: {len(scenes)}")

    # Print statistics
    stats = db.get_statistics()
    print(f"\n📊 Database statistics:")
    print(f"   Total cells: {stats['total_cells']}")
    print(f"   Total scenes: {stats['total_scenes']}")
    print(f"   Cells by type: {stats['cells_by_type']}")

    return imported_count


def main():
    """Main import function"""
    workspace_path = "/Users/michaelnetto/.openclaw/workspace/"

    print("🚀 Starting historical data import...\n")

    import_from_memory_md(workspace_path)

    print("\n✅ Import complete!")
    print(f"\nDatabase location: {os.path.join(workspace_path, 'agent-memory-system/agent_memory.db')}")


if __name__ == "__main__":
    main()
