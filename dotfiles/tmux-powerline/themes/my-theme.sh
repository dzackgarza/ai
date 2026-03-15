# shellcheck shell=bash
# Custom Theme - Catppuccin Macchiato colorscheme
# https://github.com/catppuccin/catppuccin

# Catppuccin Macchiato palette
thm_bg="#24273A"
thm_fg="#c6d0f5"
thm_cyan="#99d1db"
thm_gray="#414559"
thm_magenta="#ca9ee6"
thm_pink="#f4b8e4"
thm_blue="#8caaee"
thm_green="#a6d189"
thm_yellow="#e5c890"
thm_red="#e78284"
thm_peach="#ef9f76"
thm_teal="#81c8be"
thm_surface0="#414559"
thm_surface1="#51576d"
thm_surface2="#626880"

if tp_patched_font_in_use; then
	TMUX_POWERLINE_SEPARATOR_LEFT_BOLD=""
	TMUX_POWERLINE_SEPARATOR_LEFT_THIN=""
	TMUX_POWERLINE_SEPARATOR_RIGHT_BOLD=""
	TMUX_POWERLINE_SEPARATOR_RIGHT_THIN=""
else
	TMUX_POWERLINE_SEPARATOR_LEFT_BOLD="◀"
	TMUX_POWERLINE_SEPARATOR_LEFT_THIN="❮"
	TMUX_POWERLINE_SEPARATOR_RIGHT_BOLD="▶"
	TMUX_POWERLINE_SEPARATOR_RIGHT_THIN="❯"
fi

TMUX_POWERLINE_DEFAULT_BACKGROUND_COLOR=${TMUX_POWERLINE_DEFAULT_BACKGROUND_COLOR:-$thm_bg}
TMUX_POWERLINE_DEFAULT_FOREGROUND_COLOR=${TMUX_POWERLINE_DEFAULT_FOREGROUND_COLOR:-$thm_fg}
TMUX_POWERLINE_SEG_AIR_COLOR=$(tp_air_color)

TMUX_POWERLINE_DEFAULT_LEFTSIDE_SEPARATOR=${TMUX_POWERLINE_DEFAULT_LEFTSIDE_SEPARATOR:-$TMUX_POWERLINE_SEPARATOR_RIGHT_BOLD}
TMUX_POWERLINE_DEFAULT_RIGHTSIDE_SEPARATOR=${TMUX_POWERLINE_DEFAULT_RIGHTSIDE_SEPARATOR:-$TMUX_POWERLINE_SEPARATOR_LEFT_BOLD}

if [ -z "$TMUX_POWERLINE_WINDOW_STATUS_CURRENT" ]; then
	TMUX_POWERLINE_WINDOW_STATUS_CURRENT=(
		"#[$(tp_format inverse)]"
		" #I "
		"$TMUX_POWERLINE_SEPARATOR_RIGHT_THIN"
		" #W "
		"#[$(tp_format regular)]"
		"$TMUX_POWERLINE_DEFAULT_LEFTSIDE_SEPARATOR"
	)
fi

if [ -z "$TMUX_POWERLINE_WINDOW_STATUS_STYLE" ]; then
	TMUX_POWERLINE_WINDOW_STATUS_STYLE=(
		"$(tp_format regular)"
	)
fi

if [ -z "$TMUX_POWERLINE_WINDOW_STATUS_FORMAT" ]; then
	TMUX_POWERLINE_WINDOW_STATUS_FORMAT=(
		"#[$(tp_format regular)]"
		"  #I "
		"$TMUX_POWERLINE_SEPARATOR_RIGHT_THIN"
		" #W "
	)
fi

# Format: "segment_name foreground_color background_color [separator] [sep_bg] [sep_fg] [spacing] [separator_disable]"
TMUX_POWERLINE_LEFT_STATUS_SEGMENTS=(
)

TMUX_POWERLINE_RIGHT_STATUS_SEGMENTS=(
	"uptime $thm_peach $thm_bg"
	"disk_usage $thm_blue $thm_bg"
	"ram $thm_yellow $thm_bg"
	"cpu $thm_green $thm_bg"
	"claude_limits $thm_magenta $thm_bg"
	"time $thm_cyan $thm_bg"
	"rainbarf $thm_red $thm_surface0"
)
