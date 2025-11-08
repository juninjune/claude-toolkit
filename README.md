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
- **smart-commit**: Analyze git changes and create logical, well-structured commits with Conventional Commits format in Korean
- **session-journal**: Automatic session documentation system with keyword extraction and cross-linking

**Install:**
```bash
/plugin install universal@jun-toolkit
```

**Usage:**
- Say "커밋 정리해줘" or "smart commit" when ready to commit changes
- Say "세션 리뷰" or "세션 정리" to document your work session

## Repository Structure

This repository serves dual purposes:
1. **Marketplace**: Public plugin catalog deployed to GitHub
2. **Workspace**: Local development environment (not in Git)

### Public (Deployed)
```
claude-toolkit/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace definition
├── plugins/
│   └── universal/                # Production plugins
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
└── README.md
```

### Local Only (Not in Git)
```
claude-toolkit/
├── .dev-journal/                 # Development session logs
├── .claude/                      # Local Claude Code settings
└── workspace/                    # Development workspace
    ├── drafts/                   # Work-in-progress plugins
    ├── experiments/              # Feature testing
    ├── templates/                # Reusable templates
    └── docs/                     # Development guides & references
        └── claude-code-guide.md
```

See [STRUCTURE.md](./STRUCTURE.md) for detailed structure explanation.

## For Plugin Developers

If you want to develop new plugins:

1. **Start in workspace**: Create new plugin in `workspace/drafts/`
2. **Use templates**: Copy from `workspace/templates/`
3. **Test locally**: Add to marketplace.json and test
4. **Deploy**: Move to `plugins/` when ready
5. **Commit**: Git will only track `plugins/`, not `workspace/`

See [workspace/README.md](./workspace/README.md) for development workflow.

## Documentation

- [STRUCTURE.md](./STRUCTURE.md) - Repository structure and dual-purpose explanation
- Claude Code Complete Guide (in `workspace/docs/`) - Local development reference

## Future Plugins

Planned specialized plugins:
- **flutter**: Flutter development workflows
- **web**: Web development tools
- **korean**: Korean language processing utilities

## License

MIT
