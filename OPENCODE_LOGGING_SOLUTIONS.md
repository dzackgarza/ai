# OpenCode Logging & Session Management Solutions
## Quick Reference Guide

### Table of Contents
1. [Top Picks by Use Case](#top-picks-by-use-case)
2. [Full Comparison Table](#full-comparison-table)
3. [Installation Quick Start](#installation-quick-start)
4. [Decision Guide](#decision-guide)

---

## Top Picks by Use Case

| Use Case | Recommended Stack | Complexity | Cost | Why This Stack |
|----------|------------------|-----------|------|----------------|
| **Solo Dev - Cost Tracking** | OCsight + @ccusage/opencode | 1-2/5 | Free | Real-time + historical analysis, zero external deps |
| **Team Collaboration** | OpenSync | 2/5 | Paid | Real-time cloud sync, multi-tool support, eval tagging |
| **Enterprise Audit Trail** | opencode-database-plugin + PostgreSQL | 4/5 | Free | Persistent storage, SQL-queryable, full event logging |
| **LLM Monitoring** | Helicone + opencode-helicone-session | 2/5 | Freemium | Provider-level observability, request inspection |
| **Multi-Tool Unified View** | OpenSync | 2/5 | Paid | Only solution supporting OpenCode + Claude Code + Codex |
| **Local Only - Zero Setup** | @nogataka/opencode-viewer + @ccusage/opencode | 1/5 | Free | No external dependencies, pure local analysis |

---

## Full Comparison Table

### Cloud-Hosted Solutions

| Tool | Author | Status | Setup | Cost | Real-time | Persistent | Dashboard | Best For |
|------|--------|--------|-------|------|-----------|-----------|-----------|----------|
| **OpenSync** | Wayne Sutton | ✅ Active | 2/5 | Paid | ✅ | ✅ | ✅✅✅ | Team collaboration, multi-tool |
| **Helicone** | Helicone + H2Shami | ✅ Active | 2/5 | Freemium | ✅ | ✅ | ✅✅ | LLM request monitoring |
| **Portkey** | Portkey AI | ✅ Active | 3/5 | Paid | ✅ | ✅ | ✅✅ | Enterprise cost control |

### Local CLI Tools

| Tool | Author | Status | Setup | Cost | Real-time | Persistent | Dashboard | Best For |
|------|--------|--------|-------|------|-----------|-----------|-----------|----------|
| **OCsight** | Huynh Gia Buu | ✅ Active | 2/5 | Free | ✅ | Local | ✅ | Real-time cost dashboard |
| **@ccusage/opencode** | ccusage | ✅ Active | 1/5 | Free | ❌ | Local | ❌ | Quick analysis & reports |
| **OpenCode Monitor** | Community | ✅ Active | 2/5 | Free | ✅ | Local | ✅ | Usage analytics & optimization |

### Session Storage & Viewers

| Tool | Author | Status | Setup | Cost | Real-time | Features | Best For |
|------|--------|--------|-------|------|-----------|----------|----------|
| **@nogataka/opencode-viewer** | Nogataka | ✅ Active | 1/5 | Free | ✅ | Web UI, file watching, search | Local session browsing |
| **opencode-session-metadata** | Crayment | ✅ Active | 2/5 | Free | ✅ | Metadata storage API | Custom session tagging |
| **opencode-database-plugin** | aemr3 | ✅ Active | 4/5 | Free | ✅ | PostgreSQL, full audit trail | Enterprise logging |

### Specialized Plugins

| Tool | Author | Status | Setup | Cost | What It Does | Best For |
|------|--------|--------|-------|------|-------------|----------|
| **@ramtinj95/opencode-tokenscope** | ramtinj95 | ✅ Active | 2/5 | Free | Token analysis, cost breakdown | Token debugging, subagent costs |
| **opencode-wakatime** | angristan | ✅ Active | 2/5 | Free/Paid | Activity tracking integration | Developer productivity metrics |
| **opencode-plugin-inspector** | ericc-ch | ✅ Active | 3/5 | Free | Real-time hook debugging | Plugin development |

### Web Interfaces

| Tool | Author | Status | Setup | Cost | Features | Best For |
|------|--------|--------|-------|------|----------|----------|
| **opencode-web** | chris-tse | ✅ Active | 2/5 | Free | React web UI, chat interface | Browser-based interaction |
| **OpenChamber** | Community | ✅ Active | 2/5 | Free | VS Code + Web/Desktop | IDE integration |

---

## Installation Quick Start

### Fastest: Local-Only Cost Tracking
```bash
# Real-time dashboard
bunx ocsight

# Historical analysis (one-time)
npx @ccusage/opencode@latest daily

# Session browser
npx @nogataka/opencode-viewer@latest
```

### Cloud-Hosted: OpenSync
```bash
# Add to ~/.config/opencode/opencode.json
echo '{
  "plugin": ["opencode-sync-plugin"]
}' >> ~/.config/opencode/opencode.json

# First run: Follow setup wizard
opencode
```

### Enterprise: PostgreSQL Logging
```bash
# 1. Setup PostgreSQL
docker run -d -e POSTGRES_PASSWORD=password postgres:15

# 2. Add plugin to config
echo '{"plugin": ["opencode-database-plugin"]}' >> ~/.config/opencode/opencode.json

# 3. Configure DB connection
export OPENCODE_DB_URL=postgresql://user:password@localhost/opencode
```

### Token Analysis
```bash
# Add to config
echo '{"plugin": ["@ramtinj95/opencode-tokenscope"]}' >> ~/.config/opencode/opencode.json

# Then in sessions
/tokenscope  # Show token breakdown
```

---

## Decision Guide

### Question 1: How many people use this?
- **Just me** → OCsight or @ccusage/opencode
- **My team** → OpenSync
- **Enterprise** → opencode-database-plugin

### Question 2: Where should logs live?
- **Local only** → @nogataka/opencode-viewer + CLI tools
- **Cloud** → OpenSync
- **Company database** → opencode-database-plugin

### Question 3: What's most important?
- **Cost visibility** → OCsight + @ramtinj95/opencode-tokenscope
- **Session history** → @nogataka/opencode-viewer
- **Audit trail** → opencode-database-plugin
- **Team collaboration** → OpenSync
- **LLM monitoring** → Helicone

### Question 4: How much setup tolerance?
- **0 effort** → @ccusage/opencode (npx only)
- **5 min setup** → OCsight or @nogataka/opencode-viewer
- **30 min setup** → OpenSync
- **2+ hours** → opencode-database-plugin (need DB admin)

---

## What's NOT Solved (Gaps)

❌ **No native OpenTelemetry support** - Community workaround exists but not in core  
❌ **No official web dashboard** - Community options available  
❌ **No full-text session search** - Local tools limited to sorting/filtering  
❌ **No multi-agent cost attribution** - Requires manual calculation  
❌ **No real-time plugin metrics** - Plugin ecosystem not instrumented  

---

## Native Storage Format (For Custom Tools)

OpenCode stores everything as JSON in `~/.local/share/opencode/storage/`:

```
storage/
├── session/{projectHash}/{sessionID}.json          # Session metadata
├── message/{sessionID}/msg_{messageID}.json        # Individual messages
├── part/                                           # Tool execution details
└── session-metadata/{projectHash}/                 # Custom metadata
```

**Key fields in messages:**
- `role`: "user" | "assistant" | "tool"
- `content`: Text content
- `usage`: { `inputTokens`, `outputTokens`, `cacheReadTokens`, `cacheCreationTokens` }
- `timestamp`: ISO string
- `toolUse`: { `toolName`, `toolInput`, `result` }

---

## Ecosystem Links

- **Official Docs**: https://opencode.ai/docs/plugins/
- **Awesome OpenCode**: https://github.com/awesome-opencode/awesome-opencode
- **OpenSync**: https://www.opensync.dev/
- **Plugin Examples**: https://opencode.ai/docs/plugins/ (env-protection.js, etc.)

---

## Maintenance Status (as of March 2026)

✅ = Actively maintained  
⚠️ = Sporadic updates  
❌ = Archived  

All recommended tools show ✅ status.

---

## Cost Breakdown

| Type | Cost | Notes |
|------|------|-------|
| **Local tools** | Free | OCsight, ccusage, viewer |
| **Cloud dashboards** | $0-50/month | OpenSync uses Convex (pay-as-you-go) |
| **Database** | Free* | PostgreSQL self-hosted or managed (AWS, Azure, etc.) |
| **LLM monitoring** | Free tier + paid | Helicone freemium |
| **Custom development** | Time | Building custom plugin |

*PostgreSQL: self-hosted = free, managed services = $10-100+/month

---

## Next Actions for This Repository

1. **Immediate**: Add @ramtinj95/opencode-tokenscope for token insights
2. **Short-term**: Evaluate OCsight for real-time cost awareness
3. **Medium-term**: Consider opencode-database-plugin if audit trails needed
4. **Long-term**: If team collaboration needed, evaluate OpenSync

