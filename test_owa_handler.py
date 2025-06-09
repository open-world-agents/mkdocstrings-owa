#!/usr/bin/env python3
"""Test script for the OWA handler."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from mkdocstrings_handlers.owa import get_handler


def test_owa_handler():
    """Test the OWA handler functionality."""
    print("Testing OWA Handler for mkdocstrings")
    print("=" * 50)

    # Create a mock config
    class MockConfig:
        config_file_path = "./mkdocs.yml"

    # Create handler
    handler = get_handler({}, MockConfig())
    print(f"✓ Handler created: {handler.name} (domain: {handler.domain})")

    # Set up Jinja environment
    template_dir = Path("src/mkdocstrings_handlers/owa/templates/material")
    env = Environment(loader=FileSystemLoader(template_dir))
    handler.env = env
    print("✓ Jinja environment configured")

    # Test plugin discovery
    if handler._plugin_discovery:
        discovered, failed = handler._plugin_discovery.get_plugin_info()
        print(f"✓ Plugin discovery working: {len(discovered)} plugins discovered")
        print(f"  - Discovered: {list(discovered.keys())}")
        if failed:
            print(f"  - Failed: {list(failed.keys())}")
    else:
        print("✗ Plugin discovery not available")
        return False

    # Test OWA plugin collection and rendering
    print("\nTesting OWA plugin handling:")
    for plugin_name in ["example", "desktop"]:
        try:
            options = handler.get_options({})
            plugin_data = handler.collect(plugin_name, options)
            rendered = handler.render(plugin_data, options)
            print(f"✓ {plugin_name} plugin: collected and rendered successfully")
            print(f"  - Type: {type(plugin_data).__name__}")
            print(f"  - Namespace: {plugin_data.namespace}")
            print(f"  - Version: {plugin_data.version}")
            print(f"  - Name: {plugin_data.name}")
            print(f"  - Kind: {plugin_data.kind.value}")
            print(f"  - Components: {list(plugin_data.components.keys())}")
        except Exception as e:
            print(f"✗ {plugin_name} plugin failed: {e}")
            return False

    # Test Python module fallback
    print("\nTesting Python module fallback:")
    try:
        options = handler.get_options({})
        python_data = handler.collect("os", options)
        print(f"✓ Python module 'os': collected successfully")
        print(f"  - Name: {python_data.name}")
        print(f"  - Kind: {python_data.kind.value}")
    except Exception as e:
        print(f"✗ Python module fallback failed: {e}")
        return False

    print("\n" + "=" * 50)
    print("✓ All tests passed! OWA handler is working correctly.")
    return True


if __name__ == "__main__":
    success = test_owa_handler()
    exit(0 if success else 1)
