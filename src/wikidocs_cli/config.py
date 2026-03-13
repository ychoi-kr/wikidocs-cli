import configparser
import os
from pathlib import Path


CONFIG_DIR = Path.home() / ".wikidocs"
CREDENTIALS_FILE = CONFIG_DIR / "credentials"


def _read_credentials():
    """Read the credentials INI file."""
    config = configparser.ConfigParser()
    config.read(CREDENTIALS_FILE)
    return config


def save_token(token: str, profile: str = "default"):
    """Save a token to ~/.wikidocs/credentials."""
    CONFIG_DIR.mkdir(exist_ok=True)
    config = _read_credentials()
    if not config.has_section(profile) and profile != "default":
        config.add_section(profile)
    if profile == "default" and not config.has_section("default"):
        config.add_section("default")
    config.set(profile, "token", token)
    CREDENTIALS_FILE.write_text(config_to_string(config))
    os.chmod(CREDENTIALS_FILE, 0o600)


def load_token(profile: str = "default") -> str | None:
    """Load a token from ~/.wikidocs/credentials."""
    config = _read_credentials()
    if config.has_option(profile, "token"):
        return config.get(profile, "token")
    return None


def remove_token(profile: str = "default"):
    """Remove a token from ~/.wikidocs/credentials."""
    config = _read_credentials()
    if config.has_section(profile):
        config.remove_section(profile)
        CREDENTIALS_FILE.write_text(config_to_string(config))


def config_to_string(config: configparser.ConfigParser) -> str:
    """Convert a ConfigParser to string."""
    import io
    buf = io.StringIO()
    config.write(buf)
    return buf.getvalue()
