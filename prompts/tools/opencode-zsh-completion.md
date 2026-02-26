# Opencode Zsh Completion with Fzf

Zsh completion function for `opencode` that provides fzf-powered model selection with caching.

## Features

- **Fzf integration**: Type `opencode -m **<TAB>` for fzf model picker
- **Cached models**: Models cached for 24 hours to avoid slow `opencode models` calls
- **Lazy loading**: Cache only populated on first completion use
- **Full option support**: Completions for all major `opencode` flags

## Installation

Add to `.zshrc` (requires oh-my-zsh fzf plugin):

```zsh
# Opencode dynamic model completion with fzf
_opencode_models() {
    local cache_file="$ZSH_CACHE_DIR/opencode_models"
    
    # Return cached models if valid (< 1 hour old)
    if [[ -f "$cache_file" ]]; then
        local cache_age=$(( $(date +%s) - $(stat -c %Y "$cache_file" 2>/dev/null || echo 0) ))
        if [[ $cache_age -lt 3600 ]]; then
            cat "$cache_file"
            return 0
        fi
    fi
    
    # Fetch and cache
    local models=("${(@f)$(opencode models 2>/dev/null)}")
    if [[ ${#models[@]} -gt 0 ]]; then
        print -rl -- $models > "$cache_file" 2>/dev/null
    fi
    print -rl -- $models
}

_opencode() {
    local state cache_file models
    
    _arguments \
        '-m[Model to use]:model:->models' \
        '-c[Continue last session]' \
        '-s[Session ID]:session_id:_opencode_sessions' \
        '--print-logs[Print logs to stderr]' \
        '--log-level[Log level]:(DEBUG INFO WARN ERROR)' \
        '--port[Port to listen on]:port:' \
        '--hostname[Hostname to listen on]:hostname:' \
        '--mdns[Enable mDNS service discovery]' \
        '--mdns-domain[Custom mDNS domain]:domain:' \
        '--cors[Additional CORS domains]:cors:' \
        '--continue[Continue the last session]' \
        '--session[Session ID to continue]:session_id:' \
        '--fork[Fork session when continuing]' \
        '--prompt[Prompt to use]:prompt:' \
        '--agent[Agent to use]:agent:' \
        '*::arguments:_default'
    
    case $state in
        (models)
            cache_file="$ZSH_CACHE_DIR/opencode_models"
            
            if [[ -f "$cache_file" ]]; then
                local cache_age=$(( $(date +%s) - $(stat -c %Y "$cache_file" 2>/dev/null || echo 0) ))
                if [[ $cache_age -lt 3600 ]]; then
                    models=("${(@f)$(<"$cache_file")}")
                else
                    models=("${(@f)$(opencode models 2>/dev/null)}")
                    print -rl -- $models > "$cache_file" 2>/dev/null
                fi
            else
                models=("${(@f)$(opencode models 2>/dev/null)}")
                print -rl -- $models > "$cache_file" 2>/dev/null
            fi
            
            compadd "$@" -a models
            ;;
    esac
}

# Fzf integration for opencode -m
_fzf_complete_opencode() {
    _fzf_complete +m -- "$@" < <(_opencode_models)
}

_fzf_complete_opencode_post() {
    # Extract just the model name (remove any descriptions if added later)
    awk '{print $1}'
}

_opencode_sessions() {
    compadd "$@" $(opencode session list 2>/dev/null | awk '{print $1}')
}

compdef _opencode opencode
```

## Usage

### Standard tab completion

```bash
opencode -m <TAB>        # Shows model list
opencode --log-level <TAB>  # Shows DEBUG INFO WARN ERROR
```

### Fzf completion (recommended)

```bash
opencode -m **<TAB>      # Opens fzf picker with all models
```

## How it works

1. **`_opencode_models()`**: Helper function that returns model list from cache or `opencode models`
2. **`_opencode()`**: Main completion function using `_arguments` for option parsing
3. **`_fzf_complete_opencode()`**: Fzf integration that feeds models to fzf
4. **`_fzf_complete_opencode_post()`**: Post-processor to extract selection
5. **`compdef _opencode opencode`**: Registers completion for `opencode` command

## Cache

- Location: `$ZSH_CACHE_DIR/opencode_models` (usually `~/.cache/oh-my-zsh/opencode_models`)
- TTL: 24 hours
- Format: One model per line (raw output from `opencode models`)
