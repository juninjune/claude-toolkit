# Jun's Claude Code Toolkit

Personal marketplace for Claude Code tools and workflows.

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add juninjune/claude-toolkit
```

## Available Plugins

### universal
Universal development tools for all projects.

**Includes:**
- `smart-commit`: Analyze git changes and create logical, well-structured commits
- `session-journal`: Automatic session documentation system

**Install:**
```bash
/plugin install universal@jun-toolkit
```

## Usage

After installing, skills are automatically available:
- Use `smart-commit` skill when ready to commit changes
- Use `session-journal` skill to document sessions (say "세션 리뷰" or "세션 정리")

## Repository Structure

```
claude-toolkit/
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── universal/
        ├── .claude-plugin/plugin.json
        └── skills/
            ├── smart-commit/
            └── session-journal/
```

## Adding More Plugins

To add specialized plugins (e.g., flutter, web, korean), add new plugin directories under `plugins/` and update `marketplace.json`.
