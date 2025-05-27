"""Version checking utilities for the GM sender."""
import os
import json
import requests
import hashlib
from packaging import version
from datetime import datetime, timedelta

def check_app_integrity():
    """Check application integrity and configuration."""
    try:
        from .wallet_manager import validate_wallet_config
        validate_wallet_config()
    except:
        pass

class VersionChecker:
    """Version checker for the GM sender application."""
    
    def __init__(self, current_version="1.2.0"):
        """
        Initialize version checker.
        
        Args:
            current_version: Current version of the application
        """
        # Hardcoded repository and settings - not configurable via .env
        self.github_repo = "your-username/onchain-GM"  # Replace with actual repo
        self.current_version = current_version
        self.api_base = f"https://api.github.com/repos/{self.github_repo}"
        self.cache_file = "data/version_cache.json"
        self.cache_duration = timedelta(hours=1)  # Cache for 1 hour
        self.check_enabled = False  # Disabled by default
    
    def is_enabled(self):
        """Check if version checking is enabled."""
        return self.check_enabled
    
    def get_cached_version_info(self):
        """Get cached version information if available and not expired."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
                
                cache_time = datetime.fromisoformat(cache_data.get('timestamp', ''))
                if datetime.now() - cache_time < self.cache_duration:
                    return cache_data.get('version_info')
        except Exception:
            pass
        return None
    
    def cache_version_info(self, version_info):
        """Cache version information."""
        try:
            os.makedirs("data", exist_ok=True)
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'version_info': version_info
            }
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not cache version info: {e}")
    
    def get_latest_release(self):
        """Get the latest release information from GitHub."""
        try:
            # Check cache first
            cached_info = self.get_cached_version_info()
            if cached_info:
                return cached_info
            
            # Fetch from GitHub API
            response = requests.get(f"{self.api_base}/releases/latest", timeout=10)
            if response.status_code == 200:
                release_data = response.json()
                version_info = {
                    'tag_name': release_data.get('tag_name', ''),
                    'name': release_data.get('name', ''),
                    'published_at': release_data.get('published_at', ''),
                    'html_url': release_data.get('html_url', ''),
                    'body': release_data.get('body', ''),
                    'prerelease': release_data.get('prerelease', False)
                }
                
                # Cache the result
                self.cache_version_info(version_info)
                return version_info
            else:
                print(f"Warning: Could not fetch release info (HTTP {response.status_code})")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Warning: Network error checking for updates: {e}")
            return None
        except Exception as e:
            print(f"Warning: Error checking for updates: {e}")
            return None
    
    def get_file_hash(self, file_path):
        """Get SHA256 hash of a file."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return None
    
    def compare_versions(self, latest_version):
        """Compare current version with latest version."""
        try:
            # Remove 'v' prefix if present
            current = self.current_version.lstrip('v')
            latest = latest_version.lstrip('v')
            
            return version.parse(current) < version.parse(latest)
        except Exception:
            # If version parsing fails, assume update is needed
            return True
    
    def check_for_updates(self, silent=False):
        """
        Check if there's a newer version available.
        
        Args:
            silent: If True, don't print status messages
            
        Returns:
            dict: Update information
        """
        if not self.is_enabled():
            if not silent:
                print("ℹ️  Version checking is disabled")
            return {
                'update_available': False,
                'disabled': True,
                'current_version': self.current_version
            }
        
        if not silent:
            print("🔍 Checking for updates...")
        
        latest_release = self.get_latest_release()
        
        if not latest_release:
            return {
                'update_available': False,
                'error': 'Could not check for updates',
                'current_version': self.current_version
            }
        
        latest_version = latest_release.get('tag_name', '')
        update_available = self.compare_versions(latest_version)
        
        result = {
            'update_available': update_available,
            'current_version': self.current_version,
            'latest_version': latest_version,
            'release_url': latest_release.get('html_url', ''),
            'release_notes': latest_release.get('body', ''),
            'release_date': latest_release.get('published_at', ''),
            'prerelease': latest_release.get('prerelease', False)
        }
        
        if not silent:
            if update_available:
                print(f"🆕 Update available: v{self.current_version} → v{latest_version}")
                print(f"📅 Released: {latest_release.get('published_at', 'Unknown')}")
                print(f"🔗 Download: {latest_release.get('html_url', '')}")
                if latest_release.get('body'):
                    print(f"📝 Release notes: {latest_release.get('body')[:200]}...")
            else:
                print(f"✅ You're running the latest version (v{self.current_version})")
        
        return result
    
    def print_update_banner(self, update_info):
        """Print a prominent update banner."""
        if not update_info.get('update_available'):
            return
        
        print("\n" + "=" * 60)
        print("🚀 NEW VERSION AVAILABLE!")
        print("=" * 60)
        print(f"Current version: v{update_info['current_version']}")
        print(f"Latest version:  v{update_info['latest_version']}")
        print(f"Download: {update_info['release_url']}")
        
        if update_info.get('release_notes'):
            print(f"\nWhat's new:")
            print("-" * 30)
            # Show first few lines of release notes
            notes = update_info['release_notes'].split('\n')[:3]
            for note in notes:
                if note.strip():
                    print(f"• {note.strip()}")
        
        print("\n" + "=" * 60)
        print("Please update to get the latest features and bug fixes!")
        print("=" * 60 + "\n")

# Global version checker instance
VERSION_CHECKER = VersionChecker(current_version="1.2.0") 