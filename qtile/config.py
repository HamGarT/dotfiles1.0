import os
import subprocess
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration
from qtile_extras.widget.decorations import PowerLineDecoration


mod = "mod4"
terminal = guess_terminal()
@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([script])


keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn("alacritty"), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "space", lazy.spawn("rofi -show run")),
    Key([mod, "shift"], "m", lazy.spawn("rofi -show")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
    # pulseaudio volume
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"),
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"),
    ),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([mod, "shift"], "s", lazy.spawn("flameshot gui")),
]

# --------------------------------------------------------
# Groups
# --------------------------------------------------------


for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


# groups = [Group(i) for i in "123456789"]
groups = [
    Group("1", label="󰬺",layout="monadtall"),
    Group("2", label="󰬻", layout="monadtall"),
    Group("3", label="󰬼", layout="monadtall"),
    Group("4", label="󰬽", layout="monadtall"),
    Group("5", label="󰬾", layout="monadtall"),
    Group("6", label="󰣇 "),
    Group("7", label="󰓓 "),
    Group("8", label="󱘗 "),
]

for i in groups:
    keys.extend(
        [
            # mod1 + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

# --------------------------------------------------------
# Scratchpads
# --------------------------------------------------------

# groups.append(ScratchPad("6", [
#     DropDown("chatgpt", "firefox --app=https://chat.openai.com", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False ),
#     DropDown("mousepad", "", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False ),
#     DropDown("terminal", "alacritty", x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False ),
#     DropDown("scrcpy", "", x=0.8, y=0.05, width=0.15, height=0.6, on_focus_lost_hide=False )
# ]))

# keys.extend([
#     Key([mod], 'F10', lazy.group["6"].dropdown_toggle("chatgpt")),
#     Key([mod], 'F11', lazy.group["6"].dropdown_toggle("mousepad")),
#     Key([mod], 'F12', lazy.group["6"].dropdown_toggle("terminal")),
#     Key([mod], 'F9', lazy.group["6"].dropdown_toggle("scrcpy"))
# ])


# --------------------------------------------------------
# Layouts
# --------------------------------------------------------

layouts = [
    layout.Columns(border_width=1, margin=5, border_focus="#8f8888", border_normal="#333f40.8"),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    #layout.Matrix(),
    #layout.MonadTall(),
    # layout.MonadWide(),
    #layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    #layout.Zoomy(),
]

# --------------------------------------------------------
# Decorations
# https://qtile-extras.readthedocs.io/en/stable/manual/how_to/decorations.html
# --------------------------------------------------------

# decor_left = {
#     "decorations": [
#         PowerLineDecoration(
#             path="arrow_left"
#             # path="rounded_left"
#             # path="forward_slash"
#             # path="back_slash"
#         )
#     ],
# }

# decor_right = {
#     "decorations": [
#         PowerLineDecoration(
#             path="arrow_right"
#             # path="rounded_right"
#             # path="forward_slash"
#             # path="back_slash"
#         )
#     ],
# }

# --------------------------------------------------------
# Widgets
#https://gitlab.com/stephan-raabe/dotfiles/-/blob/main/qtile/config.py?ref_type=heads
# --------------------------------------------------------

widget_defaults = dict(
    font="CaskaydiaCove Nerd Font",
    fontsize=9,
    padding=5,
)

# widget_list = [
#     widget.GroupBox(
#         font="CaskaydiaCove Nerd Font",
#         fontsize=20,
#         margin_y=3,
#         margin_x=0,
#         padding_y=5,
#         padding_x=5,
#         borderwidth=2,
#         active="#fffbc5",  # color para el grupo actual
#         inactive="#cccccc",  # color para los grupos inactivos
#         rounded=False,
#         highlight_method="block",
#         this_current_screen_border="#3c4247",
#         other_current_screen_border="#cccccc",
#         foreground="#ffffff",
#         background="#273030",
#     ),
   
#     widget.WindowName(),
#     widget.CPU(
#         padding=0,
#         fontsize=12,
#         format='{load_percent}%'
#     ),
#     widget.TextBox(
#         text=" ",
#         foreground="fffbc5",
#         fontsize=18,
#     ),
#     widget.Memory(
#         padding=0,
#         fontsize=11,
#         measure_mem="G",
#         format="{MemUsed:.0f}{mm}",
#     ),
#     widget.TextBox(
#         text="",
#         foreground="fffbc5",
#         fontsize=18,
#     ),
#     widget.TextBox(
#         text=" "
#     ),
#     # widget.TextBox(
#     #     text="󰕾",
#     #     foreground="fffbc5",
#     #     fontsize=18,
#     # ),
#     widget.PulseVolume(
#         fontsize=18,
#         foreground='fffbc5',
#         # padding=10,
#         emoji=True,
#         emoji_list=['󰸈','󰕿','󰖀','󰕾'],
#         # volume_down_command = 'pactl set-sink-volume @DEFAULT_SINK@ -5%',
#         # volume_app='pulseaudio',
#         format='{}',
#     ),
#     widget.Battery(
#         fontsize=13,
#         format='{percent:2.0%}'
#     ),
#      widget.TextBox(
#         padding=0,
#         background="",
#         text=" ",
#         foreground="fffbc5",
#         fontsize=18,
#     ),
    
#     widget.Systray(),
    
#     widget.TextBox(
#         background="",
#         text=" 󰃰",
#         foreground="fffbc5",
#         fontsize=18,
#     ),
#     widget.Clock(
#         fontsize=11,
#         padding=10,
#         format="%I:%M %p\n%d-%m-%y",
#     ),
#      widget.TextBox(
#         text=" ",
#     ),
# ]

extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Gap(38),
        # top=bar.Bar(
        #     widget_list,
        #     30,
        #     #padding=40,
        #     opacity=1,
        #     border_width=[0, 0, 0, 0],
        #     margin=[0, 0, 0, 0],
        #     background="#273030",
        # ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"



   
