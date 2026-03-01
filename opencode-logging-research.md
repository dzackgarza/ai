# Comprehensive Research: OpenCode Logging & Session Management Solutions

## Research Conducted
- **NPM Package Search**: opencode-logger, opencode-sync-plugin, @ccusage/opencode
- **GitHub Repository Search**: Explored opencode-plugin-* ecosystem, community repos
- **Official Docs**: OpenCode plugin architecture, ecosystem page
- **Community Discussion**: GitHub issues, Reddit discussions, blog posts
- **Integration Approaches**: Cloud-hosted, self-hosted, local-only, observability platforms

---

## VIABLE SOLUTIONS FOUND

### CATEGORY 1: CLOUD-HOSTED DASHBOARDS & SYNC SERVICES

#### 1. **OpenSync (opensync.dev)**
- **Author**: Wayne Sutton (@waynesutton)
- **Latest Version**: N/A (active development, GitHub releases tracked)
- **Last Update**: Recent commits in main repo
- **Maintenance**: Active
- **Plugin Used**: opencode-sync-plugin (npm)
- **NPM Package**: opencode-sync-plugin@latest
- **What It Solves**:
  - Real-time cloud sync of OpenCode sessions
  - Unified dashboard for monitoring session activity
  - Token/cost tracking across sessions
  - Session search, filtering, and management
  - Export datasets for evaluation ("evals")
  - Multi-provider support (OpenCode, Claude Code, Codex CLI, Cursor, Pi agent)
- **How It Integrates**:
  - Plugin architecture: Hooks into OpenCode session events
  - Syncs to cloud backend (Convex)
  - Real-time bidirectional sync
- **Setup Complexity**: 2/5 (npm install + config file)
- **External Dependencies**:
  - Cloud-hosted: Convex backend (requires account)
  - Self-hosted option available (Convex deployment)
- **Features**:
  - Real-time session tracking
  - Usage statistics dashboard
  - Token/cost analysis
  - Context search for RAG
  - Custom labels for evaluation tagging
  - Session filtering by date/project/model
- **Adoption Signals**:
  - 6 stars on GitHub
  - Multiple related plugins for other CLI tools
  - Active maintenance
  - Community discussion mentions
- **Limitations**:
  - Requires cloud account for hosted version
  - Plugin-based (not integrated into OpenCode core)
  - Limited to sessions only (no detailed event logging)
- **Best Use Cases**:
  - Team collaboration & session sharing
  - Cost monitoring across projects
  - Evaluation/benchmark session management
  - Cross-tool session unification

---

#### 2. **Helicone Integration (opencode-helicone-session)**
- **Author**: H2Shami (@H2Shami)
- **Latest Version**: Published
- **Maintenance**: Active
- **Repository**: github.com/H2Shami/opencode-helicone-session
- **What It Solves**:
  - Groups LLM requests by OpenCode session
  - Observability into LLM calls
  - Cost tracking per session
  - Request/response logging
- **How It Integrates**:
  - Plugin: Injects Helicone-Session-Id headers into fetch requests
  - Automatically groups requests from same OpenCode session
- **Setup Complexity**: 2/5 (plugin install + Helicone API key)
- **External Dependencies**:
  - Requires Helicone account (cloud-hosted)
  - Helicone API endpoint
- **Features**:
  - Session-level request grouping
  - LLM provider observability
  - Request/response inspection
  - Cost tracking (via Helicone)
- **Adoption Signals**:
  - Listed in OpenCode official docs as example plugin
  - Maintained repository
- **Limitations**:
  - OpenCode-specific (no direct logging, only LLM request grouping)
  - Requires Helicone subscription
  - No OpenCode-specific analytics
- **Best Use Cases**:
  - LLM provider monitoring
  - Request/response debugging
  - Cost tracking for model consumption

---

#### 3. **Portkey AI Gateway**
- **Author**: Portkey (portkey.ai)
- **Latest Version**: N/A (cloud service)
- **Maintenance**: Active commercial product
- **Blog Post**: "OpenCode: token usage, costs, and access control"
- **What It Solves**:
  - Unified cost visibility across all providers
  - Request metadata capture
  - Access control & guardrails
  - Budget enforcement
  - Structured logging
- **How It Integrates**:
  - AI Gateway: Routes OpenCode requests through Portkey
  - Acts as control layer between OpenCode and LLM providers
  - Captures structured logs, metadata, usage
- **Setup Complexity**: 3/5 (requires provider config, routing setup)
- **External Dependencies**:
  - Cloud-hosted gateway (Portkey subscription)
- **Features**:
  - Multi-provider cost aggregation
  - Request/model/workspace-level tracking
  - Access control enforcement
  - Model usage guardrails
- **Adoption Signals**:
  - Commercial product
  - Official OpenCode documentation mentions
- **Limitations**:
  - Focused on LLM provider control, not OpenCode sessions
  - Requires request routing through gateway
- **Best Use Cases**:
  - Enterprise cost control
  - Multi-provider governance
  - Unified logging across providers

---

### CATEGORY 2: LOCAL TOOLS & CLI ANALYZERS

#### 4. **@ccusage/opencode (ccusage)**
- **Author**: ccusage
- **Latest Version**: 0.x (active, beta)
- **NPM Package**: @ccusage/opencode
- **Maintenance**: Active
- **What It Solves**:
  - Parse OpenCode session/message JSON files
  - Cost accounting and analysis
  - Daily/weekly/monthly reports
  - Token usage tracking
- **How It Integrates**:
  - CLI tool: Reads from ~/.local/share/opencode/storage/
  - Parses JSON directly
  - Uses LiteLLM pricing database for cost calculation
- **Setup Complexity**: 1/5 (npx command, no config needed)
- **External Dependencies**:
  - None (local-only analysis)
- **Features**:
  - Daily/weekly/monthly aggregation
  - Session-level reports
  - Cost breakdown by model
  - JSON export support
  - Responsive terminal tables
- **Adoption Signals**:
  - Active maintenance
  - Referenced in OpenCode ecosystem
  - Handles OpenCode's native storage format
- **Limitations**:
  - CLI-only (no persistent dashboard)
  - One-time analysis (not real-time)
  - No filtering by project/session
  - Requires manual runs
- **Best Use Cases**:
  - Quick cost/usage analysis
  - Periodic reporting
  - Scripted cost tracking
  - Integration with CI/CD

---

#### 5. **OCsight (ocsight)**
- **Author**: Huynh Gia Buu (@heyhuynhgiabuu)
- **Latest Version**: Active development
- **Repository**: github.com/heyhuynhgiabuu/ocsight
- **Maintenance**: Active
- **What It Solves**:
  - Real-time cost tracking dashboard
  - Budget monitoring & alerts
  - Provider breakdown
  - Daily activity tracking
- **How It Integrates**:
  - CLI tool: Reads OpenCode sessions from local storage
  - Real-time terminal UI with Bun
  - Budget setting & enforcement
- **Setup Complexity**: 2/5 (bun install, budget config)
- **External Dependencies**:
  - None (local-only)
- **Features**:
  - Real-time session monitoring
  - Budget tracking & limits
  - Provider cost breakdown
  - Daily activity charts
  - Cost projections
  - Beautiful terminal dashboard
- **Adoption Signals**:
  - Active GitHub repository
  - Referenced in OpenCode ecosystem
  - Built with modern stack (Bun)
- **Limitations**:
  - Terminal-based only
  - Real-time limited to local sessions
  - No session history search
  - New project (adoption still growing)
- **Best Use Cases**:
  - Real-time cost monitoring
  - Budget enforcement
  - Developer cost awareness
  - Session activity tracking

---

#### 6. **OpenCode Monitor**
- **Author**: ocmonitor (community)
- **Latest Version**: N/A
- **Website**: ocmonitor.vercel.app
- **Maintenance**: Active
- **What It Solves**:
  - Real-time usage analytics
  - Token consumption tracking
  - Cost insights per model
  - Optimization recommendations
- **How It Integrates**:
  - CLI tool for terminal analytics
  - Dashboard interface
  - Real-time metrics
- **Setup Complexity**: 2/5
- **External Dependencies**:
  - None (local-only)
- **Features**:
  - Real-time analytics dashboard
  - Model-specific pricing
  - Burn rate monitoring
  - Context window usage tracking
  - Performance comparisons
  - Customizable exports
- **Adoption Signals**:
  - Vercel-hosted (stable)
  - Community project
- **Limitations**:
  - New project (limited adoption data)
  - CLI-focused
  - No persistent backend
- **Best Use Cases**:
  - Development usage monitoring
  - Model performance comparison
  - Cost optimization

---

### CATEGORY 3: SESSION STORAGE & MANAGEMENT

#### 7. **@nogataka/opencode-viewer**
- **Author**: Nogataka (@nogataka)
- **Latest Version**: 0.0.3
- **NPM Package**: @nogataka/opencode-viewer
- **Maintenance**: Active
- **What It Solves**:
  - Web-based viewer for OpenCode sessions
  - Real-time file watching
  - Session/message/part browsing
  - Search & filtering
- **How It Integrates**:
  - Web UI: Monitors ~/.local/share/opencode/storage/ for changes
  - File watcher for live refresh
  - React-based frontend
- **Setup Complexity**: 1/5 (npx run, no config)
- **External Dependencies**:
  - None (reads local storage)
- **Features**:
  - Project search/filtering
  - Session/message browser
  - Real-time file watching
  - Grid & table view layouts
  - Message count tracking
  - Activity time tracking
- **Adoption Signals**:
  - Maintained package on npm
  - Clear documentation
  - Adapts proven codex-viewer pattern
- **Limitations**:
  - Web UI only (no persistent storage)
  - No analytics or cost tracking
  - Limited to local storage reading
  - No filtering/search depth
- **Best Use Cases**:
  - Local session browsing
  - Quick session review
  - Development activity tracking
  - Project organization view

---

#### 8. **opencode-session-metadata**
- **Author**: Crayment (@crayment)
- **Latest Version**: Latest on GitHub
- **Repository**: github.com/crayment/opencode-session-metadata
- **Maintenance**: Active
- **What It Solves**:
  - Store arbitrary JSON metadata for sessions
  - Session information retrieval
  - Custom metadata management
- **How It Integrates**:
  - Plugin: Hooks session lifecycle events
  - Stores metadata in ~/.local/share/opencode/storage/session-metadata/
  - Provides SDK for metadata access
- **Setup Complexity**: 2/5 (plugin config + usage)
- **External Dependencies**:
  - None (local storage)
- **Features**:
  - Get/set arbitrary JSON metadata
  - Session info injection
  - Environment variable injection (SESSION_ID, etc)
  - Metadata organized by project
- **Adoption Signals**:
  - Active repository
  - Clear documentation
  - Integration-focused
- **Limitations**:
  - Metadata storage only (no analytics)
  - Custom fields only
  - Requires manual API calls
- **Best Use Cases**:
  - Custom session tagging
  - Project metadata association
  - Workflow automation metadata

---

### CATEGORY 4: DATABASE BACKENDS (SELF-HOSTED)

#### 9. **opencode-database-plugin (PostgreSQL)**
- **Author**: aemr3 (@aemr3)
- **Latest Version**: GitHub releases tracked
- **Repository**: github.com/aemr3/opencode-database-plugin
- **Maintenance**: Active
- **What It Solves**:
  - Persist OpenCode sessions to PostgreSQL
  - Searchable message logging
  - Tool execution tracking
  - Token usage recording
  - Error logging
- **How It Integrates**:
  - Plugin: Hooks all session lifecycle events
  - Writes to PostgreSQL tables
  - Structured event logging
- **Setup Complexity**: 4/5 (requires PostgreSQL setup)
- **External Dependencies**:
  - PostgreSQL database (self-hosted or managed)
  - Network connectivity to DB
- **Features**:
  - Session lifecycle tracking (creation, updates, deletion, errors)
  - Message-level logging
  - Tool execution records
  - Token usage per message
  - Timestamps for all events
  - Structured data storage
- **Adoption Signals**:
  - Only PostgreSQL logging plugin found
  - Clear GitHub documentation
  - Addresses real need for persistent storage
- **Limitations**:
  - Requires database administration
  - No built-in dashboard
  - Complex schema setup
  - Network dependency
- **Best Use Cases**:
  - Enterprise deployments
  - Audit trail requirements
  - Complex analytics (SQL-based)
  - Integration with existing data warehouses
  - Long-term session history

---

### CATEGORY 5: SPECIALIZED PLUGINS

#### 10. **opencode-wakatime**
- **Author**: angristan (@angristan)
- **Latest Version**: Released with semver
- **Repository**: github.com/angristan/opencode-wakatime
- **NPM**: Likely opencode-wakatime
- **Maintenance**: Active
- **What It Solves**:
  - Track OpenCode sessions in WakaTime
  - Integrate with existing coding activity tracker
  - Unified activity dashboard
- **How It Integrates**:
  - Plugin: Posts session data to WakaTime API
- **Setup Complexity**: 2/5 (WakaTime API key)
- **External Dependencies**:
  - WakaTime account & API key (cloud)
- **Features**:
  - Session-level activity tracking
  - Integration with WakaTime dashboard
  - Time tracking aggregation
- **Adoption Signals**:
  - Maintained by community member
  - Listed in awesome-opencode
  - WakaTime integration pattern
- **Limitations**:
  - Limited to activity tracking
  - Requires WakaTime subscription
  - No OpenCode-specific metrics
- **Best Use Cases**:
  - Activity time tracking
  - Cross-tool time aggregation
  - Developer productivity metrics

---

#### 11. **@ramtinj95/opencode-tokenscope**
- **Author**: ramtinj95 (@ramtinj95)
- **Latest Version**: Recent releases
- **NPM Package**: @ramtinj95/opencode-tokenscope
- **Maintenance**: Active
- **What It Solves**:
  - Detailed token usage analysis
  - Visual cost charts
  - Category breakdowns (system, user, assistant, tools, reasoning)
  - Subagent cost tracking
- **How It Integrates**:
  - Plugin: Analyzes message tokens in real-time
  - Provides CLI commands for reports
- **Setup Complexity**: 2/5 (plugin install)
- **External Dependencies**:
  - None (analyzes local data)
- **Features**:
  - Token breakdown by category
  - Visual charts
  - Subagent cost isolation
  - Per-message analysis
  - Cost projections
- **Adoption Signals**:
  - Active npm package
  - Referenced in awesome-opencode
  - Fills real gap in token analysis
- **Limitations**:
  - Plugin-only (no standalone tool)
  - Terminal output limited
  - No persistent history
- **Best Use Cases**:
  - Token usage debugging
  - Cost allocation by component
  - Subagent efficiency tracking

---

#### 12. **opencode-plugin-openspec**
- **Author**: Octane0411 (@Octane0411)
- **Latest Version**: Active development
- **Repository**: github.com/Octane0411/opencode-plugin-openspec
- **Maintenance**: Active
- **What It Solves**:
  - Dedicated OpenSpec planning mode
  - Specialized agent for architecture planning
- **How It Integrates**:
  - Plugin: Adds new agent mode
  - Customized prompting for planning
- **Setup Complexity**: 2/5 (plugin config)
- **External Dependencies**:
  - None
- **Features**:
  - Separate `openspec-plan` agent
  - Planning-focused prompts
  - Prevents implementation during planning
- **Adoption Signals**:
  - Solves real workflow problem
  - Active development
- **Limitations**:
  - Specialized use case
  - Not for general logging
- **Best Use Cases**:
  - Spec-driven development workflows

---

#### 13. **opencode-plugin-compose & opencode-plugin-inspector**
- **Author**: ericc-ch (@ericc-ch)
- **Repository**: github.com/ericc-ch/opencode-plugins
- **Maintenance**: Active
- **What It Solves**:
  - opencode-plugin-compose: Combine multiple plugins
  - opencode-plugin-inspector: Real-time hook event debugging
- **How It Integrates**:
  - Plugin utilities for other plugins
  - Inspector provides web debug UI
- **Setup Complexity**: 3/5 (requires composition)
- **External Dependencies**:
  - None
- **Features**:
  - Plugin composition utility
  - Real-time event inspection web UI
  - Hook event debugging
- **Adoption Signals**:
  - 26 stars on GitHub
  - Solves real plugin development need
- **Limitations**:
  - Development-focused
  - Not for end-user logging
  - Requires developer knowledge
- **Best Use Cases**:
  - Plugin development debugging
  - Hook event inspection

---

#### 14. **Environment Protection & Security Plugins**
- **opencode-env-protection**: Prevents env file editing (official example)
- **opencode-policy-layer** (OPA/Rego): Native policy enforcement
- **Both** address security logging but not primarily for analytics

---

### CATEGORY 6: WEB INTERFACES & DASHBOARDS

#### 15. **opencode-web / Chris Tse**
- **Author**: chris-tse (@chris-tse)
- **Repository**: github.com/chris-tse/opencode-web
- **Type**: Standalone React web UI
- **What It Solves**:
  - Web-based alternative to TUI
  - Real-time chat interface
  - Tool execution visibility
  - Code diff viewing
- **How It Integrates**:
  - Standalone React app
  - Connects to OpenCode API server
  - Auto-detects API on localhost
- **Setup Complexity**: 2/5 (npm install + bun dev)
- **External Dependencies**:
  - Running OpenCode API server
- **Features**:
  - Real-time chat UI
  - Tool execution display
  - Enhanced diff viewing
  - Session management
- **Adoption Signals**:
  - Active GitHub repo
  - Modern stack (React, Vite, Bun)
  - Addresses UX need
- **Limitations**:
  - UI only (no logging backend)
  - Doesn't persist data
  - Local-only (no cloud sync)
- **Best Use Cases**:
  - Browser-based interaction
  - Team shared sessions
  - Accessibility (GUI vs TUI)

---

#### 16. **OpenChamber (VS Code Extension)**
- **Author**: Community
- **Type**: VS Code Extension + Web/Desktop App
- **What It Solves**:
  - IDE integration for OpenCode
  - Web & Desktop apps
  - Session management
- **How It Integrates**:
  - IDE plugin or standalone app
- **Setup Complexity**: 2/5
- **External Dependencies**:
  - None (local)
- **Features**:
  - IDE integration
  - Web/Desktop interface
  - Session management
- **Adoption Signals**:
  - Community project
  - Listed in awesome-opencode
- **Limitations**:
  - Limited info available
  - Not specifically for logging
- **Best Use Cases**:
  - IDE-integrated workflows

---

### CATEGORY 7: OBSERVABILITY & MONITORING (NOT YET INTEGRATED)

#### 17. **OpenTelemetry Integration (Proposed, Not Yet in Core)**
- **Status**: Requested (GitHub issue #12142), PR #5245 has low traction
- **What It Would Solve**: Standard OTEL trace export
- **Integration Approach**: 
  - User built workaround: JsonlSpanProcessor with custom plugin
  - Span types: ai.streamText, ai.toolCall, ai.streamText.doStream
- **External Dependencies**: OTEL collector, backend (Jaeger, Datadog, etc.)
- **Current Status**: Community POC, not in core
- **Note**: OpenCode does NOT currently have native OTEL support

---

## UNSOLVED GAPS & LIMITATIONS

1. **No Persistent Real-time Event Logging**: OpenCode doesn't natively log all hook events in real-time to searchable storage
2. **No Official Dashboard**: No built-in web UI for session/event browsing
3. **No OTEL Integration**: No native OpenTelemetry support (only user POC)
4. **Limited Structured Logging**: Plugins must implement their own event structure
5. **No Built-in Observability**: Compared to LLM platforms (Helicone, Langfuse), OpenCode lacks native observability layer
6. **Session Search**: No full-text search across all sessions without custom tooling
7. **Cost Allocation**: Multi-agent/tool cost attribution requires manual calculation

---

## COMPARISON MATRIX

| Tool | Type | Logging Type | Real-time | Persistent | Dashboard | Complexity | Cost |
|------|------|-------------|-----------|-----------|-----------|-----------|------|
| **OpenSync** | Cloud Dashboard | Sessions | ✅ | ✅ | ✅✅✅ | 2 | Paid (Convex) |
| **Helicone** | LLM Observability | Requests | ✅ | ✅ | ✅✅ | 2 | Freemium |
| **Portkey** | API Gateway | All Requests | ✅ | ✅ | ✅✅ | 3 | Paid |
| **@ccusage/opencode** | CLI Analysis | Sessions | ❌ | Local | ❌ | 1 | Free |
| **OCsight** | CLI Dashboard | Sessions | ✅ | Local | ✅ | 2 | Free |
| **OpenCode Monitor** | CLI Analytics | Sessions | ✅ | Local | ✅ | 2 | Free |
| **@nogataka/opencode-viewer** | Web Viewer | Sessions | ✅ | Local | ✅ | 1 | Free |
| **opencode-session-metadata** | Plugin Storage | Metadata | ✅ | Local | ❌ | 2 | Free |
| **opencode-database-plugin** | PostgreSQL | All Events | ✅ | ✅ (DB) | ❌ | 4 | Free (self-host) |
| **opencode-wakatime** | Integration | Activity | ✅ | ✅ (WakaTime) | ✅ | 2 | Free/Paid |
| **@ramtinj95/opencode-tokenscope** | Token Analysis | Tokens | ✅ | Local | ✅ | 2 | Free |
| **opencode-web** | Web UI | N/A | ✅ | ❌ | ✅ | 2 | Free |

---

## RECOMMENDED STACKS BY USE CASE

### **Use Case 1: Simple Cost Tracking (Solo Developer)**
**Stack**: OCsight + @ccusage/opencode
- **Why**: Minimal setup, local-only, real-time + historical analysis
- **Complexity**: 1/5
- **Cost**: Free

### **Use Case 2: Team Collaboration & Session Sharing**
**Stack**: OpenSync
- **Why**: Real-time sync, team dashboard, eval tagging
- **Complexity**: 2/5
- **Cost**: Paid (Convex backend)

### **Use Case 3: Enterprise Audit Trail**
**Stack**: opencode-database-plugin + PostgreSQL + custom dashboard
- **Why**: Full event logging, persistent storage, SQL queryable
- **Complexity**: 4/5
- **Cost**: Free (self-hosted PostgreSQL)

### **Use Case 4: LLM Provider Monitoring**
**Stack**: Helicone + opencode-helicone-session
- **Why**: Provider-level observability, request inspection
- **Complexity**: 2/5
- **Cost**: Freemium

### **Use Case 5: Multi-Tool Unified Dashboard**
**Stack**: OpenSync (covers OpenCode + Claude Code + Codex CLI + Cursor)
- **Why**: Only multi-tool solution
- **Complexity**: 2/5
- **Cost**: Paid

### **Use Case 6: Cost Optimization & Budget Control**
**Stack**: OCsight + OpenCode Monitor
- **Why**: Real-time dashboards, budget alerts, provider breakdown
- **Complexity**: 2/5
- **Cost**: Free

### **Use Case 7: Local Development (Minimal Overhead)**
**Stack**: @nogataka/opencode-viewer + @ccusage/opencode
- **Why**: No external dependencies, pure local analysis
- **Complexity**: 1/5
- **Cost**: Free

### **Use Case 8: Custom/Proprietary Logging**
**Stack**: Custom plugin + opencode-session-metadata + local JSON analysis
- **Why**: Maximum flexibility
- **Complexity**: 5/5
- **Cost**: Free (development time)

---

## KEY FINDINGS

1. **No "Complete" Solution Exists**: Every tool solves one or two problems, not all
2. **Plugin Ecosystem is Fragmented**: 20+ plugins but limited feature overlap
3. **Self-Hosted DB Option is Nascent**: opencode-database-plugin is only PostgreSQL option
4. **Cloud-Hosted = OpenSync**: Clear market leader for multi-tool, team-focused use case
5. **Cost Tracking is Well-Covered**: Multiple CLI tools (ocsight, ccusage, monitor)
6. **Session Search is Weak**: No full-text search across sessions without custom tooling
7. **OTEL Integration is Missing**: Community workaround exists, not in core
8. **LLM Observability is Covered**: Helicone integration available
9. **Web UI is Community-Built**: No official web dashboard beyond `opencode web` (TUI only)
10. **Local Storage is OpenCode's Strength**: Native JSON storage is parseable and hackable

---

## RECOMMENDED NEXT STEPS

### For This Repository:
1. **Implement** opencode-database-plugin for audit requirements
2. **Add** @ramtinj95/opencode-tokenscope for token analysis
3. **Consider** OCsight for real-time cost dashboard
4. **Evaluate** OpenSync if team collaboration is needed

### For OpenCode Community:
1. Native OTEL support would unify observability
2. Official web dashboard (beyond TUI) would improve adoption
3. Plugin registry (npm keywords exist but no curation)
4. Session full-text search capability

---

## RESEARCH CONFIDENCE NOTES

- **High Confidence**: OpenSync, Helicone, @ccusage/opencode, OCsight, opencode-database-plugin
- **Medium Confidence**: OpenCode Monitor, opencode-web, OpenChamber (limited public info)
- **Low Confidence**: Some plugins (no GitHub stars/usage data visible)
- **Unknown Status**: Some repos may have been archived or moved

All findings are current as of research date (March 1, 2026).

