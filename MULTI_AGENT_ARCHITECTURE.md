# Multi-Agent Agentic Architecture for Desktop Auto

## Current Architecture
Your system currently has:
- **Orchestrator Pattern**: `main.py` (monolithic) → TradingAnalyzer (sequential AI calls)
- **Three AI Providers**: Perplexity, Claude, Google AI (run sequentially)
- **UI Automation**: TradingView & Symbolik automation (linear workflow)
- **Email Alerts**: Triggered by consolidated decision
- **Output**: HTML reports and email notifications

## Proposed Multi-Agent Architecture

### 1. Agent Types & Responsibilities

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Orchestrator                        │
│              (Main Supervisor / Coordinator)                 │
└────────┬──────────────────────────────────────────────────────┘
         │
    ┌────┴────────────────────────────────────────────────────────────┐
    │                                                                  │
    ▼                                                                  ▼
┌──────────────────────────┐                        ┌──────────────────────────┐
│   UI AUTOMATION AGENTS   │                        │  AI ANALYSIS AGENTS      │
│  (Parallel Execution)    │                        │  (Parallel Execution)    │
└──────────────────────────┘                        └──────────────────────────┘
    │        │        │                                  │        │        │
    ▼        ▼        ▼                                  ▼        ▼        ▼
  ┌─────┐ ┌─────┐ ┌─────────┐                    ┌─────────┐┌──────┐┌──────────┐
  │ TV  │ │ TV  │ │Symbolik │                    │Perplex ││Claude││Google AI│
  │Win1 │ │Win2 │ │ Agent   │                    │  Agent ││Agent ││  Agent   │
  └─────┘ └─────┘ └─────────┘                    └─────────┘└──────┘└──────────┘
    │        │        │                                  │        │        │
    └────┬───┴────┬───┘                                 └────┬───┴────┬───┘
         │        │                                         │        │
         ▼        ▼                                         ▼        ▼
    ┌──────────────────┐                            ┌──────────────────┐
    │ Screenshot Pool  │                            │ Analysis Results │
    │  (Concurrent)    │                            │  Aggregator      │
    └──────────────────┘                            └──────────────────┘
         │                                                 │
         └─────────────────────┬─────────────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │Decision Agent        │
                    │(Consolidate + Email) │
                    └──────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
                ┌─────────┐          ┌──────────┐
                │HTML     │          │Email     │
                │Reporter │          │Agent     │
                └─────────┘          └──────────┘
```

### 2. Individual Agents Definition

#### **2.1 Agent Orchestrator** (Main Supervisor)
```python
class AgentOrchestrator:
    """Main coordinator that manages agent lifecycle and communication"""
    - initialize_agents()              # Boot all agents
    - dispatch_tasks()                 # Send work to agents
    - collect_results()               # Aggregate responses
    - handle_failures()               # Retry logic
    - generate_final_report()         # Synthesize outputs
```

**Responsibilities:**
- Agent lifecycle management (initialization, monitoring, shutdown)
- Task distribution and load balancing
- Result collection and aggregation
- Error handling and retry strategies
- Inter-agent communication coordination

---

#### **2.2 UI Automation Agents** (3 agents for TradingView windows + 1 for Symbolik)

```python
class UIAutomationAgent:
    """Base agent for UI automation tasks"""
    - analyze_window(symbol)           # Capture and analyze one window
    - retry_on_failure()               # Automated recovery
    - log_state()                      # Window state tracking
    
class TradingViewWindowAgent(UIAutomationAgent):
    """Specialized agent for each TradingView window"""
    - handle_window_1(symbol)          # Trend Analysis
    - handle_window_2(symbol)          # Heiken Ashi
    - handle_window_3(symbol)          # Volume Layout
    - handle_window_4(symbol)          # Volume Profile
    
class SymbolikAgent(UIAutomationAgent):
    """Agent for Symbolik.com automation"""
    - navigate_symbolik(symbol)
    - capture_symbolik()
```

**Capabilities:**
- **Concurrent Execution**: All 4 agents can run simultaneously on different windows
- **Independent Retry Logic**: Each agent retries its own tasks
- **State Tracking**: Each maintains its own state (window position, focus, etc.)
- **Failure Isolation**: One agent's failure doesn't block others

**Communication:**
- Reports screenshots to `ScreenshotAggregator` agent
- Updates progress to Orchestrator
- Receives task assignments from Orchestrator

---

#### **2.3 AI Analysis Agents** (3 agents for each LLM provider)

```python
class AIAnalysisAgent:
    """Base agent for AI analysis"""
    - analyze_screenshots(files)        # Process images
    - parse_response()                  # Extract decision
    - handle_rate_limits()              # Exponential backoff
    - store_result()                    # Save analysis
    
class PerplexityAgent(AIAnalysisAgent):
    """Perplexity-specific analysis agent"""
    - configure_model()                 # sonar
    - call_perplexity_api()            # OpenAI-compatible
    
class ClaudeAgent(AIAnalysisAgent):
    """Claude-specific analysis agent"""
    - configure_model()                 # claude-sonnet-4-5
    - call_anthropic_api()             # Anthropic API
    
class GoogleAIAgent(AIAnalysisAgent):
    """Google AI-specific analysis agent"""
    - configure_model()                 # gemini-3-pro-preview
    - call_google_api()                # Gemini API
```

**Capabilities:**
- **Parallel Analysis**: All 3 can analyze same screenshots simultaneously
- **API-Specific Logic**: Each handles its own rate limiting, retry logic, authentication
- **Standardized Interface**: All return same output format
- **Toggle-able**: Can be enabled/disabled via environment variables
- **Fallback Chains**: If one fails, others continue

**Communication:**
- Receives screenshot batch from Orchestrator
- Reports analysis results to `ResultsAggregator`
- Signals completion to Orchestrator

---

#### **2.4 Screenshot Pool Agent**
```python
class ScreenshotPoolAgent:
    """Manages concurrent screenshot capture and distribution"""
    - collect_screenshots(symbols)     # Gather from UI agents
    - validate_screenshots()            # Quality check
    - distribute_to_analysis()         # Send to AI agents
    - cleanup_cache()                  # Memory management
```

**Responsibilities:**
- Receives screenshots from 4 UI automation agents
- Validates and caches screenshots
- Distributes same set to all 3 AI agents (avoiding re-capture)
- Manages memory and cleanup

---

#### **2.5 Results Aggregator Agent**
```python
class ResultsAggregator:
    """Collects and standardizes analysis from all AI agents"""
    - collect_results()                 # Gather from AI agents
    - normalize_format()                # Standardize output
    - calculate_consensus()             # Voting logic
    - trigger_decision_agent()          # Signal consolidation
```

**Capabilities:**
- Waits for results from enabled providers only
- Normalizes different output formats to standard schema
- Calculates consensus scores (bullish/bearish %)
- Triggers Decision Agent when threshold met

---

#### **2.6 Decision Agent**
```python
class DecisionAgent:
    """Generates final trading decision and triggers actions"""
    - generate_consolidated_decision() # Synthesize analysis
    - determine_signal()               # Buy/Sell/Hold
    - calculate_confidence()           # Confidence score
    - notify_email_agent()             # Trigger alerts
```

**Logic:**
- Receives aggregated results
- Applies weighting to provider confidence
- Generates consolidated recommendation
- Determines email threshold trigger

---

#### **2.7 HTML Reporter Agent**
```python
class HTMLReporterAgent:
    """Generates comprehensive HTML reports"""
    - generate_report()                # Create HTML
    - include_provider_insights()      # Per-provider sections
    - add_visualizations()             # Charts and graphs
    - save_report()                    # File management
```

**Report Sections:**
- All 3 provider individual analyses
- Consensus recommendation
- Confidence metrics per provider
- Trading signal history
- Screenshot gallery

---

#### **2.8 Email Agent**
```python
class EmailAgent:
    """Handles email notifications"""
    - send_alert(decision, confidence) # Send email
    - format_message()                  # Email template
    - handle_smtp_errors()              # Error recovery
    - log_delivery()                    # Tracking
```

**Capabilities:**
- Sends when decision confidence > threshold
- Formats multi-provider insights into email
- Includes attached HTML report
- Logs all attempts and delivery status

---

### 3. Agent Communication Patterns

#### **Message Queue System**
```python
class Message:
    """Standard message format for inter-agent communication"""
    - sender_id: str
    - recipient_id: str
    - message_type: str
    - payload: Dict
    - timestamp: datetime
    - priority: int

class MessageBus:
    """Central message routing system"""
    - publish(message)           # Send message
    - subscribe(agent_id)        # Agent registration
    - get_messages(agent_id)     # Retrieve messages
    - broadcast(message)         # Send to all
```

#### **Communication Patterns**

**Pattern 1: Request-Response**
```
UI Agent → Screenshot Pool: "Here are screenshots for SNAP"
Screenshot Pool → AI Agent: "Process these images"
AI Agent → Results Aggregator: "Analysis complete: BULLISH"
```

**Pattern 2: Publish-Subscribe**
```
Orchestrator → [All UI Agents]: "Process symbols: [SNAP, QBTS, NVDA]"
[All UI Agents] → Screenshot Pool: Screenshots as ready
Screenshot Pool → [All AI Agents]: "New screenshots available"
[All AI Agents] → Results Aggregator: Results as complete
```

**Pattern 3: Event-Driven**
```
Results Aggregator → Decision Agent: "Consensus reached (3/3 bullish)"
Decision Agent → Email Agent: "Send alert: confidence=95%"
Decision Agent → HTMLReporter Agent: "Generate report"
```

---

### 4. Implementation Strategy

#### **Phase 1: Infrastructure**
```
1. Create message bus and agent base class
2. Implement AgentOrchestrator
3. Create Message and MessageBus classes
4. Add agent registry and lifecycle management
```

#### **Phase 2: UI Automation Agents**
```
1. Extract TradingView window logic → 4 UI agents
2. Implement concurrent execution (threading/asyncio)
3. Add state tracking per agent
4. Screenshot Pool agent for aggregation
```

#### **Phase 3: AI Analysis Agents**
```
1. Convert current analyzers → individual agents
2. Add agent-specific retry/rate-limit logic
3. Implement Results Aggregator
4. Add consensus calculation
```

#### **Phase 4: Decision & Output Agents**
```
1. Create Decision Agent (consolidation logic)
2. Create Email Agent (notification)
3. Create HTMLReporter Agent (reporting)
4. Add inter-agent communication
```

#### **Phase 5: Full Integration**
```
1. Connect all agents via message bus
2. Add configuration for agent behavior
3. Implement monitoring and logging
4. Add graceful shutdown
```

---

### 5. Configuration for Multi-Agent System

```env
# AGENT CONFIGURATION
# ==================

# Enable/Disable Individual Agents
AGENT_ORCHESTRATOR_ENABLED=True
UI_AUTOMATION_AGENT_ENABLED=True
AI_ANALYSIS_AGENT_ENABLED=True
DECISION_AGENT_ENABLED=True
EMAIL_AGENT_ENABLED=True
HTML_REPORTER_AGENT_ENABLED=True

# Agent Execution Mode
AGENT_EXECUTION_MODE=async          # async or threaded
AGENT_MAX_WORKERS=8
AGENT_TIMEOUT_SECONDS=300

# UI Agent Configuration
UI_AGENT_PARALLEL=True              # Run all 4 UI agents concurrently
UI_AGENT_RETRY_ATTEMPTS=3
UI_AGENT_RETRY_DELAY=2

# AI Agent Configuration
AI_AGENT_PARALLEL=True              # Run all 3 analysis agents concurrently
AI_AGENT_WAIT_TIMEOUT=60            # Max wait for results
PERPLEXITY_AGENT_ENABLED=True
CLAUDE_AGENT_ENABLED=True
GOOGLE_AI_AGENT_ENABLED=True

# Message Bus Configuration
MESSAGE_BUS_TYPE=in_process         # in_process, redis, or kafka
MESSAGE_QUEUE_SIZE=1000
MESSAGE_RETENTION_SECONDS=3600

# Monitoring & Logging
AGENT_MONITORING_ENABLED=True
AGENT_LOG_LEVEL=INFO
AGENT_PERFORMANCE_METRICS=True
```

---

### 6. Benefits of Multi-Agent Architecture

| Aspect | Current | Multi-Agent |
|--------|---------|-------------|
| **UI Automation Speed** | Sequential (4 windows) | Parallel (~4x faster) |
| **AI Analysis Speed** | Sequential (3 providers) | Parallel (~3x faster) |
| **Failure Isolation** | One failure stops all | Fails gracefully, continues with others |
| **Scalability** | Hard to add new providers | Easy to add new agent types |
| **Monitoring** | Single monolithic log | Per-agent dashboards |
| **Testing** | Integration tests only | Unit test each agent independently |
| **Reusability** | Tightly coupled | Agents are reusable components |
| **Load Balancing** | N/A | Dynamic task distribution |
| **Rate Limiting** | Global | Per-agent with independent backoff |

---

### 7. Code Example: Minimal Multi-Agent Implementation

```python
# agents/base.py
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict
import logging

class Agent(ABC):
    """Base class for all agents"""
    
    def __init__(self, agent_id: str, message_bus):
        self.agent_id = agent_id
        self.message_bus = message_bus
        self.logger = logging.getLogger(self.agent_id)
        self.status = "idle"
    
    @abstractmethod
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming task. Implemented by subclasses."""
        pass
    
    async def send_message(self, recipient_id: str, message_type: str, payload: Dict):
        """Send message to another agent"""
        message = {
            "sender_id": self.agent_id,
            "recipient_id": recipient_id,
            "message_type": message_type,
            "payload": payload,
            "timestamp": datetime.now()
        }
        await self.message_bus.publish(message)
    
    async def broadcast_message(self, message_type: str, payload: Dict):
        """Send message to all subscribed agents"""
        await self.message_bus.broadcast({
            "sender_id": self.agent_id,
            "message_type": message_type,
            "payload": payload,
            "timestamp": datetime.now()
        })

# agents/orchestrator.py
class AgentOrchestrator(Agent):
    """Main coordinator agent"""
    
    def __init__(self, message_bus):
        super().__init__("orchestrator", message_bus)
        self.agents = {}
        self.tasks_pending = {}
    
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch work to appropriate agents"""
        task_type = task.get("type")
        
        if task_type == "analyze_symbol":
            symbol = task.get("symbol")
            await self.dispatch_analysis(symbol)
        
        return {"status": "dispatched"}
    
    async def dispatch_analysis(self, symbol: str):
        """Send analysis request to all enabled agents"""
        # Dispatch to UI agents
        await self.broadcast_message("capture_screenshots", {"symbol": symbol})
        
        # Wait for screenshots
        screenshots = await self.wait_for_results("screenshots_ready", timeout=60)
        
        # Dispatch to AI agents
        await self.broadcast_message("analyze_screenshots", screenshots)
        
        # Wait for analysis
        results = await self.wait_for_results("analysis_complete", timeout=60)
        
        # Trigger decision
        await self.send_message("decision_agent", "consolidate", results)

# agents/ui_automation.py
class UIAutomationAgent(Agent):
    """UI automation for TradingView windows"""
    
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        if task.get("message_type") == "capture_screenshots":
            symbol = task.get("payload", {}).get("symbol")
            screenshots = await self.capture_window(symbol)
            await self.send_message("screenshot_pool", "screenshots_ready", screenshots)
    
    async def capture_window(self, symbol: str):
        # Existing capture logic here
        pass

# main_agentic.py
import asyncio
from agents.orchestrator import AgentOrchestrator
from agents.ui_automation import UIAutomationAgent
from agents.ai_analysis import PerplexityAgent, ClaudeAgent, GoogleAIAgent
from agents.decision import DecisionAgent
from agents.email import EmailAgent

async def main():
    # Create message bus
    message_bus = MessageBus()
    
    # Create and register agents
    orchestrator = AgentOrchestrator(message_bus)
    ui_agents = [UIAutomationAgent(f"ui_agent_{i}", message_bus) for i in range(4)]
    ai_agents = [
        PerplexityAgent(message_bus),
        ClaudeAgent(message_bus),
        GoogleAIAgent(message_bus)
    ]
    decision_agent = DecisionAgent(message_bus)
    email_agent = EmailAgent(message_bus)
    
    # Start all agents
    tasks = [agent.start() for agent in ui_agents + ai_agents + [orchestrator, decision_agent, email_agent]]
    await asyncio.gather(*tasks)
    
    # Send initial task
    await orchestrator.handle_task({
        "type": "analyze_symbol",
        "symbol": "SNAP"
    })

if __name__ == "__main__":
    asyncio.run(main())
```

---

### 8. Migration Path from Current to Multi-Agent

**Step 1:** Keep existing code, add agent layer on top
**Step 2:** Gradually migrate components to agents
**Step 3:** Run both systems in parallel during transition
**Step 4:** Switch to multi-agent when tested and stable
**Step 5:** Remove old code

This allows gradual migration with minimal disruption.

---

### 9. Advanced Features (Future)

- **Agent Clustering**: Distribute agents across multiple machines
- **Dynamic Scaling**: Add/remove agents based on load
- **Learning Agents**: Improve decision-making over time
- **Hierarchical Agents**: Manager agents oversee worker agents
- **Graph Reasoning**: Use LLM agents for complex strategy planning
- **Real-time Dashboards**: Monitor all agents' status
- **Self-healing**: Agents detect and fix their own errors
- **Knowledge Sharing**: Agents learn from each other

---

## Recommendation

**Implement incrementally:**

1. **Immediate (Week 1):** Parallelize UI automation (4 TradingView agents + Screenshot Pool)
   - Fastest ROI, lowest complexity
   - Expected 3-4x speed improvement

2. **Short-term (Week 2-3):** Parallelize AI analysis (3 provider agents + Results Aggregator)
   - Moderate complexity, high value
   - Better error isolation

3. **Medium-term (Week 4+):** Full agentic system with Decision, Email, Reporter agents
   - Complete refactor to async/await pattern
   - Adds monitoring and dashboard capabilities

This approach lets you benefit from parallelization immediately while planning full migration.
