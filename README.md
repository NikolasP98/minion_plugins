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

### Project-local install for Cursor and Codex

The `minion-engineering` skills run outside Claude Code too. Outside a plugin install
`${CLAUDE_PLUGIN_ROOT}` is unset, so their scripts resolve against `.agents/skills/` in
the nearest parent directory. Copy the skill tree to the target project root:

```bash
mkdir -p /path/to/project/.agents/skills
cp -r /path/to/minion_plugins/plugins/minion-engineering/skills/. /path/to/project/.agents/skills/
```

That produces the layout the skills expect:

```
/path/to/project/.agents/skills/
├── minion-engineering/SKILL.md
├── minion-technical-writing/SKILL.md
└── minion-unslop/
    ├── SKILL.md
    └── scripts/audit.py
```

The vendored UNSLOP scanners are pinned at
[theclaymethod/unslop](https://github.com/theclaymethod/unslop) commit
`d81f5196167ded24f46fced04958c0c12d681798` and need only Python 3 from the standard
library. Re-copy the tree to pick up a pin bump; see
`plugins/minion-engineering/THIRD_PARTY_NOTICES.md` for attribution and the upstream
NO-SHIP safety status.

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
- Scripts should be self-contained bash, or Python 3 using only the standard library, with no external dependencies beyond standard tools
- Keep `plugin.json` minimal — rely on auto-discovery

## Contributing

1. Create a new plugin directory under `plugins/`
2. Follow the structure from `templates/plugin-template/`
3. Add your plugin entry to `.claude-plugin/marketplace.json`
4. Submit a PR

## License

MIT
