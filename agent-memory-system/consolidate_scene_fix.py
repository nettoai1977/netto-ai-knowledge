# Consolidate Scene Fix
# This file contains the corrected consolidate_scene method for memory_manager.py

def consolidate_scene_fixed(self, scene: str) -> Optional[str]:
    """
    Consolidate all cells in a scene into a summary (FIXED VERSION)

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

# Apply this fix to memory_manager.py by replacing the consolidate_scene method
