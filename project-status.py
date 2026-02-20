import sys
import os
import sys

# Add the workspace to Python path
sys.path.append('/Users/michaelnetto/.openclaw/workspace/projects/openclaw-dashboard')
sys.path.append('/Users/michaelnetto/.openclaw/openclaw')

async def main():
    try:
        # Import openclaw micro
        import openclaw_micro as openclaw_micro
        multiAgent = openclaw_multi
        agents = await multiAgent.discover_agents()
        
        print('\n=== Agent Workspaces Summary ===\n')
        
        total = len(agents)
        active = len([a for a in agents if a.status == 'active'])
        
        print(f'Total Agents: {total}')
        print(f'Active Agents: {active}')
        print(f'Total Sessions: {sum(a.sessionCount for a in agents)}')
        
        print('\nDetailed Status:')
        
        # Sort by agent ID
        sorted_agents = sorted(agents, key=lambda x: x['id'])
        
        for a in sorted_agents:
            workspace = f'/Users/michaelnetto/.openclaw/agents/{a["id"]}'
            
            # Count MD files (excluding sessions directory)
            md_count = []
            other_count = 0
            
            try:
                if os.path.exists(workspace):
                    mds = [f for f in os.listdir(workspace) if f.endswith('.md')]
                    md_count = len(mds)
                    # Count non-md files
                    other_count = len([f for f in os.listdir(workspace) if not f.endswith('.md')])
            except:
                pass
                
            # Count files overall
            file_count = md_count + other_count
            
            # Check for specific files
            has_soul = 'SOUL.md' in os.listdir(workspace)
            has_heartbeat = 'HEARTBEAT.md' in os.listdir(workspace) or 'HEARTBEAT.md' in os.path.join(os.path.expanduser('~'), '.openclaw/workspace/HEARTBEAT.md', '/')
            has_tools = 'TOOLS.md' in os.listdir(workspace)
            has_user = 'USER.md' in os.listdir(workspace) or os.path.join(os.path.expanduser('~'), '.openclaw/workspace/USER.md', '/')
            
            print(f'{a["id"]:6} session: {a["sessionCount"]} | S✅={has_soul}:{md_count} MD files | Clean: {other_count} non-MD files')
            if has_heartbeat:
                print(f'{a["id"]:6} | ✅ HEARTBEAT.md + HEARTBEAT.md | TOOLS.md={has_tools}')
            if has_user:
                print(f'{a["id"]:6} | ✅ USER.md')
            else:
                print(f'{a["id"]:6} | ❌ USER.md')
    
        print('\n=== Workspace cleanliness:')
        clean = 0
        messy = 0
        
        for a in sorted_agents:
            workspace = f'/Users/michaelnetto/.openclaw/agents/{a["id"]}'
            try:
                workspace_exists = os.path.exists(workspace)
                if workspace_exists:
                    files = os.listdir(workspace)
                    md_count = sum(1 for f in files if f.endswith('.md'))
                    non_md = sum(1 for f in files if not f.endswith('.md'))
                    other = len(files) - md_count
                    
                    clean = (md_count >= 6 and non_md <= 4 and other <= 12)
                    
                    print(f'{a["id"]:6}: {md_count}+{non_md} MD | Clean: {clean} {md_count >= 6 and non_md <= 4 and other <= 12} (6MD rule)')
                
                if clean:
                    clean += 1
            
            except:
                print(f'{a["id"]:6}: Error reading workspace')
                messy += 1
        
        print(f'\nWorkspace Clean: {clean}/{12}')
        if messy > 0:
            print(f'{messy} have messy workspaces (too few files)')

    except Exception as e:
        print(f'Error analyzing agent workspaces: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()
