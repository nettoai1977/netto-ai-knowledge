/**
 * AGENT LIGHTNING CONFIGURATION FOR OPENCLAW MAIN AGENT
 * 
 * Purpose: Train the Main Coordinator agent to make better routing decisions
 * 
 * This setup adds telemetry to task routing decisions, allowing Agent Lightning
 * to learn which specialist agent performs best for which task types.
 * 
 * Installation: pip install agentlightning
 * 
 * Usage: Import this module in your Main agent's initialization
 */

const fs = require('fs');
const path = require('path');

// Path to Lightning storage (in OpenClaw workspace)
const LIGHTNING_DIR = path.join(process.env.OPENCLAW_DIR || path.join(os.homedir(), '.openclaw'), 'lightning');

/**
 * Logging function - helpful for debugging
 */
function log(level, message, data = {}) {
  const timestamp = new Date().toISOString();
  const entry = `[${timestamp}] [${level}] ${message}` + (Object.keys(data).length > 0 ? ` ${JSON.stringify(data)}` : '');
  const logFile = path.join(LIGHTNING_DIR, 'training.log');
  
  try {
    fs.mkdirSync(LIGHTNING_DIR, { recursive: true });
    fs.appendFileSync(logFile, entry + '\n', 'utf8');
  } catch (e) {
    console.error('Failed to write to log:', e.message);
  }
}

/**
 * Initialize Agent Lightning for OpenClaw Main Agent
 */
function initAgentLightning() {
  try {
    // Ensure lightning directory exists
    fs.mkdirSync(LIGHTNING_DIR, { recursive: true });
    log('INFO', 'Agent Lightning directory initialized', { path: LIGHTNING_DIR });
    
    // Create configuration file
    const configPath = path.join(LIGHTNING_DIR, 'config.json');
    
    if (!fs.existsSync(configPath)) {
      const config = {
        setup: {
          project: 'openclaw-main-agent',
          description: 'Main Coordinator routing optimization',
          agentId: 'main',
          llm: 'openai:gpt-4o', // Main model used
          environment: 'development',
        },
        dataset: {
          type: 'agentlightning-traces',
          storage: 'local',
          path: path.join(LIGHTNING_DIR, 'traces'),
        },
        training: {
          algorithm: 'trpo', // or 'ppo', 'auto_opt', 'supervised'
          },
        },
        logging: {
          level: 'info',
          captureMetrics: true
        }
      };
      
      fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');
      log('INFO', 'Created Agent Lightning configuration');
    }
    
    log('INFO', 'Agent Lightning initialized successfully');
    return true;
    
  } catch (e) {
    log('ERROR', 'Failed to initialize Agent Lightning', { error: e.message || e });
    return false;
  }
}

/**
 * Add routing telemetry to Main agent decisions
 * Call this whenever Main agent assigns a task to a specialist
 */
function emitRoutingDecision(task, selectedAgent, context = {}) {
  // Check if agentlightning is available
  try {
    const agl = require('agentlightning');
    
    // Format the task routing decision
    const routingData = {
      type: 'routing_decision',
      taskId: context.taskId || 'unknown',
      task: context.task || 'unknown',
      selectedAgent: selectedAgent,
      availableAgents: context.availableAgents || [],
      taskMetadata: context.taskMetadata || {},
      timestamp: Date.now()
    };
    
    // Emit the routing decision
    log('INFO', 'Routing decision recorded', routingData);
    
    // Track reward (placeholder - you can add actual reward logic)
    // When agent completes the task, you'll call emitReward()
    
  } catch (e) {
    log('WARN', 'Agent Lightning not available, telemetry not recorded', { error: e.message });
  }
}

/**
 * Reward function - call when agent completes a task
 */
function emitReward(taskId, reward, outcome = 'success') {
  try {
    const agl = require('agentlightning');
    
    const rewardData = {
      type: 'task_completion',
      taskId: taskId,
      reward: reward,
      outcome: outcome,
      timestamp: Date.now()
    };
    
    log('INFO', 'Reward emitted', rewardData);
    log('INFO', 'Outcome', outcome);
    
    // Agent Lightning will store this and adjust policy
    // Over time, routing improves for that task type
    
  } catch (e) {
    log('WARN', 'Agent Lightning not available, reward not recorded', { error: e.message });
  }
}

/**
 * Emit tool call from agent
 * Call whenever agent uses a tool
 */
function emitToolCall(toolName, parameters = {}) {
  try {
    const agl = require('agentlightning');
    
    const toolData = {
      type: 'tool_call',
      tool: toolName,
      parameters: parameters,
      timestamp: Date.now()
    };
    
    log('INFO', 'Tool called', toolData);
    
  } catch (e) {
    log('WARN', 'Agent Lightning not available, tool call not tracked', { error: e.message });
  }
}

/**
 * Emit message from/to agent
 * Call for all agent messages
 */
function emitMessage(role, content, metadata = {}) {
  try {
    const agl = require('agentlightning');
    
    const messageData = {
      type: 'message',
      role: role,
      content: content,
      metadata: metadata,
      timestamp: Date.now()
    };
    
    // Don't log full message content to save space
    const metaSummary = {
      length: content?.length || 0,
      hasMetadata: Object.keys(metadata || {}).length > 0
    };
    
    log('INFO', 'Message emitted', { role, ...metaSummary });
    
  } catch (e) {
    log('WARN', 'Agent Lightning not available, message not tracked', { error: e.message });
  }
}

/**
 * Get trained routing policy (after or during training)
 * Returns the routing policy learned by Agent Lightning
 */
function getRoutingPolicy() {
  try {
    const policyPath = path.join(LIGHTNING_DIR, 'routing_policy.json');
    
    if (fs.existsSync(policyPath)) {
      const policy = JSON.parse(fs.readFileSync(policyPath, 'utf8'));
      log('INFO', 'Using learned routing policy', { routes: Object.keys(policy || {}), lastUpdated: policy.lastUpdated });
      return policy;
    }
    
    // Default heuristic policy (matches your WORKING.md routing guide)
    const defaultPolicy = generateDefaultPolicy();
    return defaultPolicy;
    
  } catch (e) {
    log('WARN', 'Failed to get routing policy, using defaults', { error: e.message });
    return generateDefaultPolicy();
  }
}

/**
 * Generate default routing policy based on WORKING.md heuristics
 */
function generateDefaultPolicy() {
  return {
    version: 'v1.0',
    type: 'routing_policy',
    lastUpdated: Date.now(),
    policies: {
      // Architecture & Deep Analysis → Atlas
      'monolithic': { 'agent': 'atlas', 'weight': 0.9 },
      'microservices': { 'agent': 'atlas', 'weight': 0.9 },
      'architecture': { 'agent': 'atlas', 'weight': 0.9 },
      'system design': { 'agent': 'atlas', 'weight': 0.9 },
      'trade-offs': { 'agent': 'atlas', 'weight': 0.9 },
      
      // Creative → Luna
      'branding': { 'agent': 'luna', 'weight': 0.1 },
      'naming': { 'agent': 'luna', 'weight': 0.9 },
      'taglines': { 'agent': 'luna', 'weight': 0.8 },
      'content': { 'agent': 'luna', 'weight': 0.9 },
      
      // Technical Analysis → Orion
      'debug': { 'agent': 'orion', 'weight': 0.9 },
      'database': { 'agent': 'orion', 'weight': 0.9 },
      'optimization': { 'agent': 'orion', 'weight': 0.9 },
      'api': { 'agent': 'orion', 'weight': 0.9 },
      'query': { 'agent': 'orion', 'weight': 0.9 },
      'data': { 'agent': 'orion', 'weight': 0.8 },
      
      // Operations/Development → Coder
      'code review': { 'agent': 'coder', 'weight': 0.9 },
      'bug fix': { 'agent': 'coder', 'weight': 0.9 },
      'implement': { 'agent': 'coder', 'weight': 0.8 },
      'refactor': { 'agent': 'coder', 'weight': 0.7 },
      'typescript': { 'agent': 'coder', 'weight': 0.8 },
      
      // Speed → Flash
      'quick': { 'agent': 'flash', 'weight': 0.9 },
      'optimization': { 'agent': 'agent:flash', 'weight': 0.8 },
      'simple': { 'agent': 'agent:', 'weight': 0.7 },
      
      // Strategy → Nova
      'planning': { 'agent': 'nova', 'weight': 0.9 },
      'go-to-market': { 'agent': 'nova', 'weight': 0.9 },
      'launch': { 'agent': 'nova', 'weight': 0.8 },
      'growth': { 'agent': 'nova', 'weight': 0.7 },
      
      // Contemplation → Zen
      'ethics': { 'agent': 'zen', 'weight': 0.9 },
      'philosophical': { 'agent': 'zen', 'weight': 0.9 },
      'long-term': { 'agent': 'zen', 'weight': 0.8 },
      'analysis': { 'agent': 'zen', 'weight': 0.8 },
      'consider': { 'agent': 'zen', 'weight': 0.9 },
      
      // Heavy Compute → Titan
      'scale': { 'agent': 'titan', 'weight': 0.9 },
      'performance': { 'agent': 'titan', 'weight': 0.9 },
      'architecture': { 'agent': 'titan', 'weight': 0.8 },
      'infrastructure': { 'agent': 'titan', 'weight': 0.9 },
      
      // Heavy Lifting → Max
      'analysis': { 'agent': 'max', 'weight': 0.9 },
      'refactoring': { 'agent': 'max', 'weight': 0.9 },
      'optimization': { 'agent': 'max', 'weight': 0.9 },
      'profiling': { 'agent': 'max', 'weight': 0.8 },
      
      // Quick Wins → Spark
      'tips': { 'agent': 'spark', 'weight': 0.9 },
      'shortcuts': { 'agent': 'spark', 'weight': 0.8 },
      'productivity': { 'agent': 'spark', 'weight': 0.9 },
      'hack': { 'agent': 'spark', 'weight': 0.7 },
      
      // Visual → Vision
      'ui-ux': { 'agent': 'vision', 'weight': 0.9 },
      'diagrams': { 'agent': 'vision', 'weight': 0.9 },
      'visualization': { 'agent': 'vision', 'weight': 0.8 },
      'charts': { 'agent': 'vision', 'weight': 0.7 },
      
      // Fallback
      'other': { 'agent': 'main', 'weight': 0.5 }
    },
    metadata: {
      source: 'WORKING.md heuristic rules',
      lastExport: Date.now(),
      agentLightning: 'not trained yet, using heuristics'
    }
  };
}

/**
 * Create a quick training example
 * This demonstrates how to collect routing traces for training
 */
function createTrainingExample() {
  const examplePath = path.join(LIGHTNING_DIR, 'examples', 'README.md');
  
  const example = `# Agent Lightning Training Example for OpenClaw Main Agent

## Overview
This shows how to collect routing traces for training the Main Coordinator agent to make better task routing decisions.

## Step 1: Instrument Your Routing Logic

Add telemetry calls to your task routing logic:

\`\`\`bash
# In your Main agent's routing function
import agl
from openclaw_lightning import emitRoutingDecision

def routeTask(task, available_agents):
    # Your existing routing logic here
    selected = agent = your_existing_routing_function(task, available_agents)
    
    # EMIT TELEMETRY BEFORE assigning
    emitRoutingDecision(
      task=task,
      selectedAgent=selected,
      context={
        taskId=task.get('id'),
        availableAgents=[a.id for a in available_agents],
        taskMetadata={
          type: task.get('type'),
          priority: task.get('priority'),
          tags: task.get('tags', []),
          deadline: task.get('deadline')
        }
      }
    )
    
    return selected
\`\`

## Step 2: Define Reward Function

After task completion, call emitReward with the reward:

\`\`bash
# When agent completes task successfully
from openclaw_lightning import emitReward

def completeTask(task, outcome='success'):
    # Your task completion logic here
    
    # Calculate reward
    if outcome == 'success':
        reward = calculate_success_reward(task)
    else:
        reward = -1  # Penalty for failure
    else:
        reward = 0 # Neutral
    
    # EMIT REWARD
    emitReward(task.get('id'), reward, outcome)
\`\`

## Step 3: Collect Traces

The traces are automatically collected to ~/openclaw/lightning/traces/ and can be used for training.

## Step 4: Train the Model

\`\`bash
# From your workspace
cd ~/openclaw/workspace/projects
npx agentlightning train \\
    --config ~/openclaw/lightning/config.json \\
    --data ~/openclaw/lightning/traces/ \\
    --algorithm trpo
\`\`

## Step 5: Deploy Trained Policy

The trained policy will be saved to ~/openclaw/lightning/routing_policy.json.

From your Main agent, you can then use the learned policy instead of heuristics:

\`\`bash
from openclaw_lightning import getRoutingPolicy

policy = getRoutingPolicy()
agent = policy['policies'][task_type]
selected = agent['agent']
\`\`
`;

  try {
    // Write the example if it doesn't exist
    const examplesDir = path.join(LIGHTNING_DIR, 'examples');
    fs.mkdirSync(examplesDir, { recursive: true });
    
    fs.writeFileSync(examplePath, example, 'utf8');
    log('INFO', 'Training example created', { path: examplePath });
    
  } catch (e) {
    log('ERROR', 'Failed to create training example', { error: e.message });
  }
}

module.exports = {
  initAgentLightning,
  emitRoutingDecision,
  emitReward,
  emitToolCall,
  emitMessage,
  getRoutingPolicy,
  createTrainingExample,
  LIGHTNING_DIR
};
