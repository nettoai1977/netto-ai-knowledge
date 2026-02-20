#!/usr/bin/env node

/**
 * OpenClaw Agent CLI - Task & Squad Management
 * Inspired by Clawe (https://github.com/getclawe/clawe)
 * 
 * Usage:
 *   npx @openclaw/agent-cli task:status <taskId>
 *   npx @openclaw/agent-cli task:create <title> --assign <agent>
 *   npx @openclaw/agent-cli notify <message>
 *   npx @openclaw/agent-cli squad
 */

const fs = require('fs');
const path = require('path');
const http = require('http');

// Configuration
const API_URL = process.env.OPENCLAW_DASHBOARD_URL || 'http://localhost:7070';
const TOKEN_PATH = process.env.OPENCLAW_TOKEN_PATH || path.join(process.env.HOME || '', '.openclaw/dashboard-token');

// Get stored auth token
function getToken() {
  try {
    if (fs.existsSync(TOKEN_PATH)) {
      return fs.readFileSync(TOKEN_PATH, 'utf8').trim();
    }
  } catch (e) {}
  return null;
}

// Make authenticated API request
function apiRequest(endpoint, method = 'GET', body = null) {
  return new Promise((resolve, reject) => {
    const token = getToken();
    if (!token) {
      reject(new Error('No authentication token found'));
      return;
    }
    
    const url = new URL(endpoint, API_URL);
    const options = {
      hostname: url.hostname,
      port: url.port || 80,
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    };
    
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            resolve(JSON.parse(data));
          } catch {
            resolve(data);
          }
        } else {
          reject(new Error(`API Error ${res.statusCode}: ${data}`));
        }
      });
    });
    
    req.on('error', reject);
    
    if (body) {
      req.write(JSON.stringify(body));
    }
    
    req.end();
  });
}

// Commands
const commands = {
  // View task status
  async 'task:status'([taskId]) {
    try {
      const res = await apiRequest('/api/tasks');
      const task = res.tasks.find(t => t.id === taskId || t.id.endsWith(taskId));
      
      if (!task) {
        console.log(`❌ Task not found: ${taskId}`);
        return;
      }
      
      console.log(`\n📋 Task: ${task.title}`);
      console.log(`   Status: ${task.status}`);
      console.log(`   Priority: ${task.priority}`);
      console.log(`   Assignee: ${task.assignee || 'Unassigned'}`);
      console.log(`   Created: ${new Date(task.createdAt).toLocaleString()}`);
      
      if (task.description) {
        console.log(`\n   Description: ${task.description}`);
      }
      
      if (task.subtasks && task.subtasks.length > 0) {
        console.log(`\n   Subtasks:`);
        task.subtasks.forEach((sub, i) => {
          console.log(`     ${sub.done ? '✅' : '⬜'} [${i + 1}] ${sub.title}`);
        });
      }
    } catch (e) {
      console.error(`❌ Failed to get task: ${e.message}`);
      process.exit(1);
    }
  },
  
  // Create a new task
  async 'task:create'([title, ...args]) {
    const assignToOptionIndex = args.indexOf('--assign');
    const priorityOptionIndex = args.indexOf('--priority');
    
    let assignee = null;
    if (assignToOptionIndex >= 0 && args[assignToOptionIndex + 1]) {
      assignee = args[assignToOptionIndex + 1];
    }
    
    let priority = 'normal';
    if (priorityOptionIndex >= 0 && args[priorityOptionIndex + 1]) {
      priority = args[priorityOptionIndex + 1];
    }
    
    if (!title) {
      console.error('❌ Task title is required');
      console.error('   Usage: agent-cli task:create "Task title" --assign <agent>');
      process.exit(1);
    }
    
    try {
      const res = await apiRequest('/api/tasks');
      const tasks = res.tasks || [];
      
      const newTask = {
        id: 'task-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9),
        title,
        description: '',
        assignee: assignee || null,
        priority,
        status: 'inbox',
        subtasks: [],
        createdAt: Date.now(),
        updatedAt: Date.now()
      };
      
      tasks.push(newTask);
      
      await apiRequest('/api/tasks', 'POST', { tasks });
      
      console.log(`✅ Task created: ${newTask.id}`);
      console.log(`   Title: ${title}`);
      console.log(`   Assignee: ${assignee || 'Unassigned'}`);
      console.log(`   Priority: ${priority}`);
      console.log(`   View: agent-cli task:status ${newTask.id}`);
    } catch (e) {
      console.error(`❌ Failed to create task: ${e.message}`);
      process.exit(1);
    }
  },
  
  // Update task status
  async 'task:status-update'([taskId, status]) {
    const validStatuses = ['inbox', 'in-progress', 'review', 'done'];
    
    if (!taskId || !status) {
      console.error('❌ Task ID and status are required');
      console.error('   Valid statuses: inbox, in-progress, review, done');
      console.error('   Usage: agent-cli task:status-update <taskId> <status>');
      process.exit(1);
    }
    
    if (!validStatuses.includes(status)) {
      console.error(`❌ Invalid status: ${status}`);
      console.error(`   Valid statuses: ${validStatuses.join(', ')}`);
      process.exit(1);
    }
    
    try {
      const res = await apiRequest('/api/tasks');
      const tasks = res.tasks || [];
      const task = tasks.find(t => t.id === taskId || t.id.endsWith(taskId));
      
      if (!task) {
        console.error(`❌ Task not found: ${taskId}`);
        process.exit(1);
      }
      
      task.status = status;
      task.updatedAt = Date.now();
      
      await apiRequest('/api/tasks', 'POST', { tasks });
      
      console.log(`✅ Task status updated: ${task.title} → ${status}`);
    } catch (e) {
      console.error(`❌ Failed to update task: ${e.message}`);
      process.exit(1);
    }
  },
  
  // List all tasks
  async 'task:list'() {
    try {
      const res = await apiRequest('/api/tasks');
      const tasks = res.tasks || [];
      
      if (tasks.length === 0) {
        console.log('📭 No tasks');
        return;
      }
      
      console.log(`\n📋 Tasks (${tasks.length} total):`);
      console.log('');
      
      tasks.forEach(task => {
        const statusIcon = {
          'inbox': '📥',
          'in-progress': '🔄',
          'review': '👀',
          'done': '✅'
        }[task.status] || '📄';
        
        const priorityColor = {
          'urgent': '🔴',
          'high': '🟠',
          'normal': '🔵',
          'low': '⚪'
        }[task.priority] || '⚪';
        
        const assigneeIcon = task.assignee ? {
          'main': '⭐', 'atlas': '🧠', 'luna': '🌙', 'orion': '🔭',
          'nova': '💫', 'zen': '🧘', 'flash': '⚡', 'titan': '🏔️',
          'coder': '💻', 'max': '💪', 'spark': '✨', 'vision': '👁️'
        }[task.assignee] || '🤖' : '';
        
        console.log(`${statusIcon} ${priorityColor} ${assigneeIcon} ${task.title}`);
        console.log(`   ID: ${task.id}`);
        console.log(`   Status: ${task.status} | Created: ${new Date(task.createdAt).toLocaleDateString()}`);
        console.log('');
      });
    } catch (e) {
      console.error(`❌ Failed to list tasks: ${e.message}`);
      process.exit(1);
    }
  },
  
  // Send notification
  async 'notify'([message]) {
    if (!message) {
      console.error('❌ Message is required');
      process.exit(1);
    }
    
    console.log(`📢 Notification: ${message}`);
    console.log(`   (Notifications would be delivered to squad here)`);
  },
  
  // View squad status
  async 'squad'() {
    try {
      const res = await apiRequest('/api/agents');
      const agents = res.agents || [];
      
      console.log('\n🤖 Squad Status:');
      console.log('');
      
      agents.forEach(agent => {
        const status = agent.status === 'active' ? '✅ Active' : '💤 Idle';
        const sessions = agent.sessionCount > 0 ? `${agent.sessionCount} sessions` : 'No sessions';
        
        console.log(`${agent.icon} ${agent.name}`);
        console.log(`   Status: ${status}`);
        console.log(`   ${sessions}`);
        console.log('');
      });
      
      // Load tasks
      const tasksRes = await apiRequest('/api/tasks');
      const tasks = tasksRes.tasks || [];
      
      const activeTasks = tasks.filter(t => t.status === 'in-progress');
      const doneTasks = tasks.filter(t => t.status === 'done');
      
      console.log(`📊 Task Summary:`);
      console.log(`   Inbox: ${tasks.filter(t => t.status === 'inbox').length}`);
      console.log(`   In Progress: ${activeTasks.length}`);
      console.log(`   Review: ${tasks.filter(t => t.status === 'review').length}`);
      console.log(`   Done: ${doneTasks.length}`);
    } catch (e) {
      console.error(`❌ Failed to get squad status: ${e.message}`);
      process.exit(1);
    }
  },
  
  // Show feed
  async 'feed'() {
    try {
      console.log('\n📜 Activity Feed:');
      console.log('   (Recent activity would be shown here)');
      
      // Would load from /api/feed or similar
      const res = await apiRequest('/api/sessions');
      const sessions = res || [];
      
      const recent = sessions.slice(0, 5);
      if (recent.length > 0) {
        console.log('');
        recent.forEach(s => {
          console.log(`   [${new Date(s.updatedAt).toLocaleTimeString()}] ${s.label || s.key}`);
        });
      } else {
        console.log('   No recent activity');
      }
    } catch (e) {
      console.error(`❌ Failed to load feed: ${e.message}`);
    }
  },
  
  // Check for notifications
  async 'check'() {
    try {
      const res = await apiRequest('/api/tasks');
      const tasks = res.tasks || [];
      
      const myTasks = tasks.filter(t => t.status === 'inbox' || t.status === 'in-progress');
      
      if (myTasks.length === 0) {
        console.log('📭 No tasks requiring attention');
      } else {
        console.log(`📋 You have ${myTasks.length} task(s) to work on:\n`);
        myTasks.forEach(task => {
          const urgency = task.priority === 'urgent' ? '🚨 URGENT' : task.priority === 'high' ? '⚠️ HIGH' : '';
          console.log(`   ${urgency} ${task.title}`);
          console.log(`      ${task.description || '[No description]'}`);
          console.log('');
        });
      }
    } catch (e) {
      console.error(`❌ Failed to check tasks: ${e.message}`);
    }
  },
  
  // Help
  'help'() {
    console.log('\n📚 OpenClaw Agent CLI Commands:\n');
    console.log('  Task Management:');
    console.log('    agent-cli task:status <taskId>           View task details');
    console.log('    agent-cli task:create <title>          Create new task');
    console.log('    agent-cli task:status-update <id> <status>  Update task status');
    console.log('    agent-cli task:list                      List all tasks');
    console.log('');
    console.log('  Squad Management:');
    console.log('    agent-cli squad                          View squad status');
    console.log('    agent-cli notify <message>             Send notification');
    console.log('    agent-cli feed                           View activity feed');
    console.log('    agent-cli check                           Check for tasks');
    console.log('');
    console.log('  General:');
    console.log('    agent-cli help                           Show this help');
    console.log('');
    console.log('Examples:');
    console.log('  agent-cli task:create "Fix database bug" --assign coder');
    console.log('  agent-cli task:status task-123456789');
    console.log('  agent-cli task:status-update task-123456789 "review"');
    console.log('  agent-cli squad');
    console.log('');
  }
};

// Main CLI
async function main() {
  const command = process.argv[2];
  const args = process.argv.slice(3);
  
  if (!command) {
    console.error('❌ No command specified');
    console.error('   Usage: npx @openclaw/agent-cli <command> [args...]\n');
    commands.help();
    process.exit(1);
  }
  
  const handler = commands[command];
  if (!handler) {
    console.error(`❌ Unknown command: ${command}`);
    commands.help();
    process.exit(1);
  }
  
  try {
    await handler(args);
  } catch (e) {
    console.error(`\n❌ Error: ${e.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = commands;
