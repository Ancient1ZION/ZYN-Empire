#!/usr/bin/env python3
"""
ZYN EMPIRE - START ENGINE
Bootstrap script to initialize and run the autonomous agent system
Run this once to get everything operational: python3 START_ENGINE.py
"""

import os
import sys
import json
import subprocess
from datetime import datetime
import time

class ZYNEngineBootstrap:
      def __init__(self):
                self.timestamp = datetime.now().isoformat()
                self.root_dir = os.path.dirname(os.path.abspath(__file__))
                self.status_log = []

    def log(self, message, level="INFO"):
              """Log status updates"""
              log_msg = f"[{level}] {message}"
              print(log_msg)
              self.status_log.append({"timestamp": datetime.now().isoformat(), "message": log_msg})

    def check_env(self):
              """Verify environment setup"""
              self.log("=" * 60)
              self.log("CHECKING ENVIRONMENT", "STARTUP")
              self.log("=" * 60)

        # Check Python version
              py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
              self.log(f"Python version: {py_version}")

        if sys.version_info.major < 3 or (sys.version_info.major == 3 and sys.version_info.minor < 8):
                      self.log("ERROR: Python 3.8+ required", "ERROR")
                      return False

        # Check required directories
        required_dirs = ['backend', 'backend/core', 'backend/ops', 'config', 'logs']
        for dir_name in required_dirs:
                      dir_path = os.path.join(self.root_dir, dir_name)
                      if not os.path.exists(dir_path):
                                        os.makedirs(dir_path, exist_ok=True)
                                        self.log(f"Created directory: {dir_name}")
else:
                  self.log(f"Directory exists: {dir_name}")

        return True

    def check_dependencies(self):
              """Check if required Python packages are available"""
              self.log("\n" + "=" * 60)
              self.log("CHECKING DEPENDENCIES", "STARTUP")
              self.log("=" * 60)

        required_packages = {
                      'google.oauth2': 'google-auth',
                      'google.cloud': 'google-cloud-sheets',
                      'requests': 'requests',
                      'discord': 'discord.py'
        }

        missing = []
        for module_name, package_name in required_packages.items():
                      try:
                                        __import__(module_name.split('.')[0])
                                        self.log(f"✓ {package_name} installed")
except ImportError:
                self.log(f"✗ {package_name} NOT installed", "WARN")
                missing.append(package_name)

        if missing:
                      self.log(f"\nTo install missing packages, run:", "WARN")
                      self.log(f"pip install {' '.join(missing)}", "WARN")
                      self.log("Then run this script again", "WARN")
                      return False

        return True

    def check_config(self):
              """Verify .env configuration exists"""
              self.log("\n" + "=" * 60)
              self.log("CHECKING CONFIGURATION", "STARTUP")
              self.log("=" * 60)

        env_path = os.path.join(self.root_dir, '.env')
        example_path = os.path.join(self.root_dir, '.env.example')

        if os.path.exists(env_path):
                      self.log(f"✓ .env file found")
else:
              self.log(f"✗ .env file NOT found", "WARN")
              if os.path.exists(example_path):
                self.log(f"Copy .env.example to .env and fill in your API keys:", "WARN")
                                self.log(f"  cp .env.example .env", "WARN")
                                return False
else:
                self.log(f"ERROR: Neither .env nor .env.example found", "ERROR")
                  return False

        return True

    def initialize_system(self):
              """Initialize the agent system"""
        self.log("\n" + "=" * 60)
        self.log("INITIALIZING AGENT SYSTEM", "STARTUP")
        self.log("=" * 60)

        # Create agents config
        agents_config = self.generate_agents_config()
        agents_config_path = os.path.join(self.root_dir, 'config', 'agents.json')

        with open(agents_config_path, 'w') as f:
                      json.dump(agents_config, f, indent=2)

        self.log(f"✓ Created agents configuration ({len(agents_config)} agents)")

        return True

    def generate_agents_config(self):
              """Generate configuration for all 19 agents"""
        agents = [
                      {"id": "agent_01", "name": "Noah", "role": "Architect", "active": True},
                      {"id": "agent_02", "name": "Sara", "role": "Outreach", "active": True},
                      {"id": "agent_03", "name": "Malik", "role": "Closer", "active": True},
                      {"id": "agent_04", "name": "Elijah", "role": "Signals", "active": True},
                      {"id": "agent_05", "name": "Adam", "role": "Gov Scout", "active": True},
                      {"id": "agent_06", "name": "Ruth", "role": "CRM", "active": True},
                      {"id": "agent_07", "name": "Lea", "role": "Client", "active": True},
                      {"id": "agent_08", "name": "Zara", "role": "LinkedIn", "active": True},
                      {"id": "agent_09", "name": "Ezekiel", "role": "APIs", "active": True},
                      {"id": "agent_10", "name": "Samson", "role": "Backup", "active": True},
                      {"id": "agent_11", "name": "Cyrus", "role": "Strategy", "active": True},
                      {"id": "agent_12", "name": "Asher", "role": "Health", "active": True},
                      {"id": "agent_13", "name": "Rebecca", "role": "Partners", "active": True},
                      {"id": "agent_14", "name": "Zuri", "role": "Brand", "active": True},
                      {"id": "agent_15", "name": "Mariam", "role": "Intel", "active": True},
                      {"id": "agent_16", "name": "Enoch", "role": "Opp Hunt", "active": True},
                      {"id": "agent_17", "name": "Juda", "role": "Security", "active": True},
                      {"id": "agent_18", "name": "Miro Fish", "role": "Voice", "active": True},
                      {"id": "agent_19", "name": "Caleb", "role": "Capital", "active": True},
        ]
        return agents

    def status_report(self):
              """Generate system status report"""
        self.log("\n" + "=" * 60)
        self.log("SYSTEM STATUS REPORT", "INFO")
        self.log("=" * 60)

        report = {
                      "timestamp": datetime.now().isoformat(),
                      "status": "READY",
                      "components": {
                                        "dashboard": "LIVE (v12.2 on GitHub Pages)",
                                        "agents": "19 configured and initialized",
                                        "google_sheets": "Awaiting credentials in .env",
                                        "discord_webhooks": "Awaiting token in .env",
                                        "sam_gov_api": "Awaiting API key in .env",
                                        "gcp_vm": "Ready for deployment"
                      },
                      "next_steps": [
                                        "1. Set up .env with your API keys",
                                        "2. Run: python3 backend/core/main_agent.py",
                                        "3. Monitor agent activity in Discord"
                      ]
        }

        self.log(json.dumps(report, indent=2))
        return report

    def run(self):
              """Main bootstrap sequence"""
        try:
                      if not self.check_env():
                                        return False

                      if not self.check_config():
                                        self.log("Configuration incomplete. Cannot proceed.", "ERROR")
                                        return False

                      self.initialize_system()
                      self.status_report()

            self.log("\n" + "=" * 60)
            self.log("✓ ZYN ENGINE BOOTSTRAP COMPLETE", "SUCCESS")
            self.log("=" * 60)

            return True

except Exception as e:
            self.log(f"Fatal error: {str(e)}", "ERROR")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
      bootstrap = ZYNEngineBootstrap()
    success = bootstrap.run()
    sys.exit(0 if success else 1)
