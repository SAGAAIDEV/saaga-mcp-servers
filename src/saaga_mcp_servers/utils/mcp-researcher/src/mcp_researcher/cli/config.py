"""Configuration management CLI using Fire."""

import fire

from ..core.config import Settings
from ..core.constants import DEFAULT_CONFIG_PATH
from ..core.logging import logger


class ConfigCLI:
    """Configuration management commands for MCP Researcher."""
    
    def init(self) -> None:
        """Initialize a new configuration file.
        
        Creates a new config file with default values at ~/mcp-researcher/config.yaml
        """
        try:
            config_path = Settings.init_config_file()
            logger.info(f"✅ Configuration file created successfully!")
            logger.info(f"📁 Location: file://{config_path}")
            logger.info("📝 Edit this file to add your API keys and customize settings")
            logger.info("\nTo edit the file, run:")
            logger.info(f"  open {config_path}  # macOS")
            logger.info(f"  xdg-open {config_path}  # Linux")
            logger.info(f"  notepad {config_path}  # Windows")
        except FileExistsError:
            logger.error(f"❌ Configuration file already exists at: file://{DEFAULT_CONFIG_PATH}")
            logger.info("Use 'clean' command to reset it to defaults")
        except Exception as e:
            logger.error(f"❌ Failed to create config file: {e}")
    
    def clean(self) -> None:
        """Reset the configuration file to default values.
        
        WARNING: This will remove all custom settings including API keys!
        """
        try:
            # Check if config exists
            if not DEFAULT_CONFIG_PATH.exists():
                logger.error(f"❌ No configuration file found at: {DEFAULT_CONFIG_PATH}")
                logger.info("Use 'init' command to create a new one")
                return
            
            # Show what will be lost
            logger.warning("⚠️  This will reset your configuration to default values")
            logger.warning("⚠️  All custom settings and API keys will be removed!")
            logger.info(f"📁 Config location: file://{DEFAULT_CONFIG_PATH}")
            
            # Ask for confirmation
            response = input("\nAre you sure you want to continue? (yes/no): ")
            
            if response.lower() in ['yes', 'y']:
                config_path = Settings.reset_config_file()
                logger.info(f"✅ Configuration reset successfully!")
                logger.info(f"📁 Location: file://{config_path}")
                logger.info("📝 Don't forget to add your API keys again")
            else:
                logger.info("❌ Reset cancelled")
        except Exception as e:
            logger.error(f"❌ Failed to reset config: {e}")
    
    def show(self) -> None:
        """Show the current configuration file location and status."""
        logger.info("📋 MCP Researcher Configuration")
        logger.info(f"📁 Location: file://{DEFAULT_CONFIG_PATH}")
        logger.info(f"✅ Exists: {DEFAULT_CONFIG_PATH.exists()}")
        
        if DEFAULT_CONFIG_PATH.exists():
            logger.info(f"📏 Size: {DEFAULT_CONFIG_PATH.stat().st_size} bytes")
            logger.info("\nTo view the file, run:")
            logger.info(f"  cat {DEFAULT_CONFIG_PATH}")
            logger.info("\nTo edit the file, run:")
            logger.info(f"  open {DEFAULT_CONFIG_PATH}  # macOS")
            logger.info(f"  xdg-open {DEFAULT_CONFIG_PATH}  # Linux")
            logger.info(f"  notepad {DEFAULT_CONFIG_PATH}  # Windows")


def main():
    """Entry point for the config CLI."""
    fire.Fire(ConfigCLI)


if __name__ == "__main__":
    main()