# Minion Plugins Marketplace

Plugin marketplace for Minion development tools and workflows. Installable via Claude Code's plugin discovery system.

## Plugins

| Plugin | Category | Description | Portable? |
|--------|----------|-------------|-----------|
| [fork-sync](plugins/fork-sync/) | development | Multi-phase fork sync with upstream evaluation | Yes |
| [lessons-learned](plugins/lessons-learned/) | productivity | Post-task iterative improvement capture | Yes |
| [provision-server](plugins/provision-server/) | deployment | Remote server provisioning for Minion | Minion-specific |
| [pr-workflow](plugins/pr-workflow/) | development | Three-phase PR review/prepare/merge pipeline | Yes |
| [mintlify](plugins/mintlify/) | development | Mintlify documentation platform expert | Yes |
| [minion-docs](plugins/minion-docs/) | development | Minion codebase docs and code review | Minion-specific |
| [minion-engineering](plugins/minion-engineering/) | development | Namespaced engineering, technical-writing, and advisory prose-audit skills | Minion-specific |

## Installation

### As a marketplace source

Add this repository as a marketplace source in Claude Code:

```
/plugin add nikolasp98/minion_plugins
```

### Individual plugin (local path)

```
/plugin add /path/to/minion_plugins/plugins/fork-sync
```

## Creating a new plugin

Use the template at `templates/plugin-template/` as a starting point:

```bash
cp -r templates/plugin-template plugins/my-new-plugin
```

Then:

1. Edit `.claude-plugin/plugin.json` with your plugin metadata
2. Rename `skills/example-skill/` to your skill name
3. Write your `SKILL.md` with triggers, description, and workflow
4. Add companion files (scripts, references) as needed
5. Add your plugin entry to `.claude-plugin/marketplace.json`

## Plugin structure

Each plugin follows the Claude Code plugin convention:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (name, version, keywords)
├── skills/
│   └── skill-name/
│       └── SKILL.md         # Skill definition with frontmatter
├── scripts/                 # Optional: bundled helper scripts
└── README.md                # Plugin documentation
```

Key conventions:

- Use `${CLAUDE_PLUGIN_ROOT}` for all intra-plugin path references
- Skills auto-discover from `skills/*/SKILL.md`
- Scripts should be self-contained bash with no external dependencies beyond standard tools
- Keep `plugin.json` minimal — rely on auto-discovery

## Contributing

1. Create a new plugin directory under `plugins/`
2. Follow the structure from `templates/plugin-template/`
3. Add your plugin entry to `.claude-plugin/marketplace.json`
4. Submit a PR

## License

MIT
