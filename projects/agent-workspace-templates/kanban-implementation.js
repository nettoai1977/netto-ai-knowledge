// ============================================
// KANBAN BOARD IMPLEMENTATION
// Inspired by Clawe (https://github.com/getclawe/clawe)
// ============================================

// Task data structure
const KANBAN_COLUMNS = [
  { id: 'inbox', title: '📥 Inbox', color: 'var(--blue)' },
  { id: 'in-progress', title: '🔄 In Progress', color: 'var(--yellow)' },
  { id: 'review', title: '👀 Review', color: 'var(--purple)' },
  { id: 'done', title: '✅ Done', color: 'var(--green)' }
];

let kanbanTasks = [];

// Initialize Kanban board
async function initKanbanBoard() {
  try {
    const res = await authFetch(`${API_BASE}/api/tasks`);
    const data = await res.json();
    kanbanTasks = data.tasks || [];
    renderKanbanBoard();
  } catch (e) {
    console.error('Failed to load tasks:', e);
    // Initialize with empty tasks
    kanbanTasks = [];
    renderKanbanBoard();
  }
}

// Render Kanban board
function renderKanbanBoard() {
  const board = document.getElementById('kanban-board');
  if (!board) return;

  board.innerHTML = KANBAN_COLUMNS.map(column => `
    <div class="kanban-column" style="min-width:300px;background:var(--bg-secondary);border-radius:12px;padding:16px;border:1px solid var(--border);">
      <div class="kanban-column-header" style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid var(--border);">
        <h3 style="margin:0;color:${column.color};">${column.title}</h3>
        <span class="task-count" style="background:${column.color}20;color:${column.color};padding:4px 8px;border-radius:12px;font-size:12px;">${kanbanTasks.filter(t => t.status === column.id).length}</span>
      </div>
      <div class="kanban-tasks" data-column="${column.id}" style="display:flex;flex-direction:column;gap:12px;min-height:200px;">
        ${renderTaskCards(column.id)}
      </div>
      <button onclick="addQuickTask('${column.id}')" style="margin-top:12px;padding:8px;background:var(--bg-tertiary);border:1px solid var(--border);border-radius:8px;color:var(--text-muted);cursor:pointer;font-size:13px;">
        ➕ Add task
      </button>
    </div>
  `).join('');
}

// Render task cards for a column
function renderTaskCards(columnId) {
  const tasks = kanbanTasks.filter(t => t.status === columnId);
  
  if (tasks.length === 0) {
    return '<div style="text-align:center;padding:20px;color:var(--text-muted);font-size:13px;">No tasks</div>';
  }
  
  return tasks.map(task => `
    <div class="kanban-card" data-task-id="${task.id}" style="background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:12px;cursor:pointer;" onclick="viewTask('${task.id}')">
      <div style="font-weight:600;margin-bottom:8px;color:var(--text-primary);">${escapeHtml(task.title)}</div>
      ${task.description ? `<div style="font-size:13px;color:var(--text-secondary);margin-bottom:12px;">${escapeHtml(task.description.substring(0, 100))}${task.description.length > 100 ? '...' : ''}</div>` : ''}
      <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px;">
        <div style="display:flex;gap:4px;">
          ${task.priority ? `<span style="background:${getPriorityColor(task.priority)}20;color:${getPriorityColor(task.priority)};padding:2px 8px;border-radius:4px;font-size:11px;">${task.priority}</span>` : ''}
          ${task.assignee ? `<span style="background:var(--accent)20;color:var(--accent);padding:2px 8px;border-radius:4px;font-size:11px;">${getAgentIcon(task.assignee)}</span>` : ''}
        </div>
        <span style="font-size:11px;color:var(--text-muted);">${formatTimestamp(task.createdAt)}</span>
      </div>
      ${task.subtasks && task.subtasks.length > 0 ? `
        <div style="margin-top:8px;padding-top:8px;border-top:1px solid var(--border);">
          <div style="font-size:11px;color:var(--text-secondary);margin-bottom:4px;">
            ✓ ${task.subtasks.filter(s => s.done).length}/${task.subtasks.length} subtasks
          </div>
          <div style="height:4px;background:var(--bg-tertiary);border-radius:2px;overflow:hidden;">
            <div style="height:100%;background:var(--green);width:${(task.subtasks.filter(s => s.done).length / task.subtasks.length) * 100}%"></div>
          </div>
        </div>
      ` : ''}
    </div>
  `).join('');
}

// Priority colors
function getPriorityColor(priority) {
  const colors = {
    'urgent': 'var(--red)',
    'high': 'var(--orange)',
    'normal': 'var(--blue)',
    'low': 'var(--text-muted)'
  };
  return colors[priority] || colors.normal;
}

// Agent icons
function getAgentIcon(agentId) {
  const icons = {
    'main': '⭐',
    'atlas': '🧠',
    'luna': '🌙',
    'orion': '🔭',
    'nova': '💫',
    'zen': '🧘',
    'flash': '⚡',
    'titan': '🏔️',
    'coder': '💻',
    'max': '💪',
    'spark': '✨',
    'vision': '👁️'
  };
  return icons[agentId] || '🤖';
}

// Format timestamp
function formatTimestamp(ts) {
  const diff = Date.now() - ts;
  if (diff < 60000) return 'just now';
  if (diff < 3600000) return Math.floor(diff / 60000) + 'm ago';
  if (diff < 86400000) return Math.floor(diff / 3600000) + 'h ago';
  return Math.floor(diff / 86400000) + 'd ago';
}

// Create task modal
function showCreateTaskModal() {
  const modal = document.getElementById('taskModal');
  if (!modal) {
    // Create modal if it doesn't exist
    document.body.insertAdjacentHTML('beforeend', `
      <div id="taskModal" class="modal" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:1000;align-items:center;justify-content:center;">
        <div style="background:var(--bg-card);border-radius:12px;padding:24px;max-width:600px;width:90%;max-height:80vh;overflow-y:auto;">
          <h2 style="margin-top:0;margin-bottom:20px;">Create New Task</h2>
          <div style="display:flex;flex-direction:column;gap:16px;">
            <div>
              <label style="display:block;margin-bottom:8px;">Title *</label>
              <input type="text" id="taskTitle" placeholder="Task title" style="width:100%;padding:12px;background:var(--bg-secondary);border:1px solid var(--border);border-radius:8px;color:var(--text-primary);">
            </div>
            <div>
              <label style="display:block;margin-bottom:8px;">Description</label>
              <textarea id="taskDescription" rows="3" placeholder="Task description" style="width:100%;padding:12px;background:var(--bg-secondary);border:1px solid var(--border);border-radius:8px;color:var(--text-primary);resize:none;"></textarea>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
              <div>
                <label style="display:block;margin-bottom:8px;">Assign To</label>
                <select id="taskAssignee" style="width:100%;padding:12px;background:var(--bg-secondary);border:1px solid var(--border);border-radius:8px;color:var(--text-primary);">
                  <option value="">Unassigned</option>
                  <option value="main">⭐ Main (Coordinator)</option>
                  <option value="atlas">🧠 Atlas (Deep Reasoning)</option>
                  <option value="luna">🌙 Luna (Creative)</option>
                  <option value="orion">🔭 Orion (Technical)</option>
                  <option value="nova">💫 Nova (Strategy)</option>
                  <option value="zen">🧘 Zen (Contemplation)</option>
                  <option value="flash">⚡ Flash (Speed)</option>
                  <option value="titan">🏔️ Titan (Heavy Compute)</option>
                  <option value="coder">💻 Coder (Development)</option>
                  <option value="max">💪 Max (Heavy Lifting)</option>
                  <option value="spark">✨ Spark (Quick Wins)</option>
                  <option value="vision">👁️ Vision (Visual)</option>
                </select>
              </div>
              <div>
                <label style="display:block;margin-bottom:8px;">Priority</label>
                <select id="taskPriority" style="width:100%;padding:12px;background:var(--bg-secondary);border:1px solid var(--border);border-radius:8px;color:var(--text-primary);">
                  <option value="normal">Normal</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                  <option value="low">Low</option>
                </select>
              </div>
            </div>
            <div style="display:flex;justify-content:flex-end;gap:12px;margin-top:20px;">
              <button onclick="hideTaskModal()" style="padding:10px 20px;background:var(--bg-secondary);border:1px solid var(--border);border-radius:8px;color:var(--text-primary);cursor:pointer;">Cancel</button>
              <button onclick="createTask()" style="padding:10px 20px;background:linear-gradient(135deg,var(--accent),#6366f1);color:white;border:none;border-radius:8px;cursor:pointer;">Create Task</button>
            </div>
          </div>
        </div>
      </div>
    `);
    document.getElementById('taskModal').style.display = 'flex';
  } else {
    modal.style.display = 'flex';
  }
}

function hideTaskModal() {
  const modal = document.getElementById('taskModal');
  if (modal) modal.style.display = 'none';
}

function createTask() {
  const title = document.getElementById('taskTitle').value.trim();
  const description = document.getElementById('taskDescription').value.trim();
  const assignee = document.getElementById('taskAssignee').value;
  const priority = document.getElementById('taskPriority').value;
  
  if (!title) {
    alert('Title is required');
    return;
  }
  
  const task = {
    id: 'task-' + Date.now(),
    id: 'task-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9),
    title,
    description,
    assignee: assignee || null,
    priority,
    status: 'inbox',
    subtasks: [],
    createdAt: Date.now(),
    updatedAt: Date.now()
  };
  
  kanbanTasks.push(task);
  renderKanbanBoard();
  hideTaskModal();
  
  // Clear form
  document.getElementById('taskTitle').value = '';
  document.getElementById('taskDescription').value = '';
  document.getElementById('taskAssignee').value = '';
  document.getElementById('taskPriority').value = 'normal';
  
  showToast('Task created successfully', 'success');
}

function addQuickTask(columnId) {
  const title = prompt('Enter task title:');
  if (title) {
    const task = {
      id: 'task-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9),
      title: title.trim(),
      description: '',
      assignee: null,
      priority: 'normal',
      status: columnId,
      subtasks: [],
      createdAt: Date.now(),
      updatedAt: Date.now()
    };
    
    kanbanTasks.push(task);
    renderKanbanBoard();
    showToast('Task added', 'success');
  }
}

function viewTask(taskId) {
  const task = kanbanTasks.find(t => t.id === taskId);
  if (!task) return;
  
  const modal = document.getElementById('taskDetailModal');
  if (!modal) {
    document.body.insertAdjacentHTML('beforeend', `
      <div id="taskDetailModal" class="modal" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:1000;align-items:center;justify-content:center;">
        <div style="background:var(--bg-card);border-radius:12px;padding:24px;max-width:700px;width:90%;max-height:80vh;overflow-y:auto;">
          <div id="taskDetailContent"></div>
        </div>
      </div>
    `);
  }
  
  const content = `
    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;">
      <h2 style="margin:0;">${escapeHtml(task.title)}</h2>
      <button onclick="hideTaskDetailModal()" style="background:none;border:none;font-size:20px;color:var(--text-muted);cursor:pointer;">✕</button>
    </div>
    <div style="display:flex;gap:12px;margin-bottom:20px;">
      ${task.priority ? `<span style="background:${getPriorityColor(task.priority)}20;color:${getPriorityColor(task.priority)};padding:4px 12px;border-radius:12px;">${task.priority}</span>` : ''}
      ${task.assignee ? `<span style="background:var(--accent)20;color:var(--accent);padding:4px 12px;border-radius:12px;">${getAgentIcon(task.assignee)} ${task.assignee}</span>` : ''}
      <span style="background:var(--bg-tertiary);padding:4px 12px;border-radius:12px;color:var(--text-muted);">${formatTimestamp(task.createdAt)}</span>
    </div>
    ${task.description ? `<div style="margin-bottom:20px;padding:16px;background:var(--bg-secondary);border-radius:8px;">${escapeHtml(task.description)}</div>` : ''}
    <div style="margin-bottom:20px;">
      <label style="display:block;margin-bottom:8px;">Status</label>
      <select id="taskStatus" style="width:100%;padding:10px;background:var(--bg-secondary);border:1px solid var(--border);border-radius:8px;">
        ${KANBAN_COLUMNS.map(col => `<option value="${col.id}" ${task.status === col.id ? 'selected' : ''}>${col.title}</option>`).join('')}
      </select>
    </div>
    ${task.subtasks && task.subtasks.length > 0 ? `
      <div style="margin-bottom:20px;">
        <label style="display:block;margin-bottom:8px;">Subtasks</label>
        ${task.subtasks.map((sub, idx) => `
          <div style="display:flex;align-items:center;gap:8px;padding:8px;background:var(--bg-secondary);border-radius:6px;margin-bottom:8px;">
            <input type="checkbox" ${sub.done ? 'checked' : ''} onchange="toggleSubtask('${task.id}', ${idx})">
            <span style="${sub.done ? 'text-decoration:line-through;color:var(--text-muted);' : ''}">${escapeHtml(sub.title)}</span>
          </div>
        `).join('')}
      </div>
    ` : ''}
    <div style="display:flex;gap:12px;">
      <button onclick="updateTask('${task.id}')" style="flex:1;padding:10px;background:linear-gradient(135deg,var(--accent),#6366f1);color:white;border:none;border-radius:8px;cursor:pointer;">Save Changes</button>
      <button onclick="deleteTask('${task.id}')" style="padding:10px;background:var(--red);color:white;border:none;border-radius:8px;cursor:pointer;">Delete</button>
    </div>
  `;
  
  document.getElementById('taskDetailContent').innerHTML = content;
  document.getElementById('taskDetailModal').style.display = 'flex';
}

function hideTaskDetailModal() {
  const modal = document.getElementById('taskDetailModal');
  if (modal) modal.style.display = 'none';
}

function updateTask(taskId) {
  const task = kanbanTasks.find(t => t.id === taskId);
  if (!task) return;
  
  const status = document.getElementById('taskStatus').value;
  task.status = status;
  task.updatedAt = Date.now();
  
  renderKanbanBoard();
  hideTaskDetailModal();
  showToast('Task updated', 'success');
}

function deleteTask(taskId) {
  if (confirm('Are you sure you want to delete this task?')) {
    kanbanTasks = kanbanTasks.filter(t => t.id !== taskId);
    renderKanbanBoard();
    hideTaskDetailModal();
    showToast('Task deleted', 'success');
  }
}

function toggleSubtask(taskId, subtaskIdx) {
  const task = kanbanTasks.find(t => t.id === taskId);
  if (task && task.subtasks[subtaskIdx]) {
    task.subtasks[subtaskIdx].done = !task.subtasks[subtaskIdx].done;
    task.updatedAt = Date.now();
  }
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Initialize kanban when Tasks page is shown
document.querySelectorAll('.nav-item').forEach(item => {
  item.addEventListener('click', () => {
    const page = item.dataset.page;
    if (page === 'tasks') {
      initKanbanBoard();
    }
  });
});
