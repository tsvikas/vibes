"""resources for vibes."""

from importlib import resources

files = resources.files(__name__)
prompt_md = files / "prompt.md"
message_style_emoji_md = files / "message-style-emoji.md"
