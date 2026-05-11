#!/usr/bin/env python3
"""
ZYN EMPIRE - MASTER CONTROL
Central orchestration hub for all 19 agents
Coordinates initialization, health monitoring, and graceful shutdown
"""

import json
import os
import sys
import time
import signal
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configuration
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'agents_config.json')
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
STATE_FILE = os.path.join(LOG_DIR, 'master_state.json')


class MasterController:
    """Central orchestrator for ZYN Empire"""

    def __init__(self):
        self.start_time = datetime.now().isoformat()
        self.agents: Dict[str, Any] = {}
        self.agent_status: Dict[str, Dict] = {}
        self.running = True
        self.cycle_count = 0
        self.total_tasks_processed = 0
        self.errors = 0

        # Ensure log directory exists
        os.makedirs(LOG_DIR, exist_ok=True)

        # Register signal handlers
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def shutdown(self, signum, frame):
        """Graceful shutdown handler"""
        print(f"\n[MASTER] Received signal {signum}, initiating graceful shutdown...")
        self.running = False
        self.save_state()
        print("[MASTER] Shutdown complete.")
        sys.exit(0)

    def load_config(self) -> Dict:
        """Load agent configuration"""
        try:
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
            print(f"[MASTER] Loaded config: {len(config.get('agents', []))} agents")
            return config
        except FileNotFoundError:
            print(f"[MASTER] ERROR: Config not found at {CONFIG_PATH}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"[MASTER] ERROR: Invalid JSON in config: {e}")
            sys.exit(1)

    def initialize_agents(self, config: Dict):
        """Initialize all agents from config"""
        print("\n" + "=" * 60)
        print("ZYN EMPIRE - MASTER CONTROL INITIALIZING")
        print("=" * 60)

        agents_config = config.get('agents', [])
        execution_config = config.get('execution', {})
        integrations = config.get('integrations', {})

        for agent in agents_config:
            agent_id = agent['id']
            self.agents[agent_id] = {
                'id': agent_id,
                'name': agent['name'],
                'role': agent['role'],
                'status': agent.get('status', 'IDLE'),
                'active': agent.get('active', True),
                'tasks_completed': 0,
                'errors': 0,
                'last_heartbeat': None,
                'last_task': None
            }
            self.agent_status[agent_id] = {
                'name': agent['name'],
                'role': agent['role'],
                'status': 'INITIALIZED',
                'active': agent.get('active', True)
            }
            print(f"  ✓ {agent['name']:12} [{agent_id}] — {agent['role']}")

        print(f"\n  Execution Mode: {execution_config.get('mode', 'AUTONOMOUS')}")
        print(f"  Demo Mode: {execution_config.get('demo_mode', True)}")
        print(f"  Integrations: Discord={integrations.get('discord', {}).get('enabled', False)}, "
              f"GoogleSheets={integrations.get('google_sheets', {}).get('enabled', False)}, "
              f"SAM.gov={integrations.get('sam_gov', {}).get('enabled', False)}")

    def heartbeat(self):
        """Update all agent heartbeats"""
        now = datetime.now().isoformat()
        for agent_id, agent in self.agents.items():
            if agent['active']:
                agent['last_heartbeat'] = now
                self.agent_status[agent_id]['status'] = 'HEALTHY'

    def process_cycle(self, config: Dict):
        """Execute one processing cycle"""
        self.cycle_count += 1
        execution_config = config.get('execution', {})
        demo_mode = execution_config.get('demo_mode', True)

        # Simulate task processing for each active agent
        for agent_id, agent in self.agents.items():
            if not agent['active']:
                self.agent_status[agent_id]['status'] = 'INACTIVE'
                continue

            if demo_mode:
                # Demo task execution
                self.agents[agent_id]['tasks_completed'] += 1
                self.agents[agent_id]['last_task'] = datetime.now().isoformat()
                self.total_tasks_processed += 1
                self.agent_status[agent_id]['status'] = 'IDLE'

    def generate_report(self) -> Dict:
        """Generate master status report"""
        active_count = sum(1 for a in self.agents.values() if a['active'])
        healthy_count = sum(1 for a in self.agent_status.values() if a['status'] == 'HEALTHY')
        total_completed = sum(a['tasks_completed'] for a in self.agents.values())
        total_errors = sum(a['errors'] for a in self.agents.values())

        now = datetime.now().isoformat()
        uptime_seconds = (datetime.fromisoformat(now) - datetime.fromisoformat(self.start_time)).total_seconds()

        report = {
            'timestamp': now,
            'system': 'ZYN EMPIRE',
            'master_status': 'OPERATIONAL',
            'uptime_seconds': uptime_seconds,
            'cycle_count': self.cycle_count,
            'agents': {
                'total': len(self.agents),
                'active': active_count,
                'healthy': healthy_count,
                'inactive': len(self.agents) - active_count
            },
            'tasks': {
                'total_completed': total_completed,
                'current_cycle': self.total_tasks_processed,
                'errors': total_errors
            },
            'agent_details': {}
        }

        for agent_id, agent in self.agents.items():
            report['agent_details'][agent_id] = {
                'name': agent['name'],
                'role': agent['role'],
                'status': self.agent_status[agent_id]['status'],
                'active': agent['active'],
                'tasks_completed': agent['tasks_completed'],
                'errors': agent['errors'],
                'last_heartbeat': agent['last_heartbeat']
            }

        return report

    def save_state(self):
        """Save current state to file"""
        state = {
            'saved_at': datetime.now().isoformat(),
            'cycle_count': self.cycle_count,
            'total_tasks_processed': self.total_tasks_processed,
            'errors': self.errors,
            'agents': self.agents
        }
        try:
            with open(STATE_FILE, 'w') as f:
                json.dump(state, f, indent=2)
            print(f"[MASTER] State saved to {STATE_FILE}")
        except Exception as e:
            print(f"[MASTER] Failed to save state: {e}")

    def run(self, cycles: int = 1, interval: int = 60):
        """Main execution loop"""
        config = self.load_config()
        self.initialize_agents(config)

        demo_mode = config.get('execution', {}).get('demo_mode', True)
        mode_label = "DEMO" if demo_mode else "PRODUCTION"

        print(f"\n{'=' * 60}")
        print(f"MASTER CONTROL — {mode_label} MODE")
        print(f"Cycles: {cycles if cycles > 0 else 'INFINITE'} | Interval: {interval}s")
        print(f"{'=' * 60}\n")

        cycle = 0
        while self.running:
            if cycles > 0 and cycle >= cycles:
                break

            cycle += 1
            print(f"[MASTER] Cycle {cycle}/{cycles if cycles > 0 else '∞'} at {datetime.now().strftime('%H:%M:%S')}")

            self.heartbeat()
            self.process_cycle(config)

            report = self.generate_report()
            print(f"  Agents: {report['agents']['active']}/{report['agents']['total']} active, "
                  f"{report['agents']['healthy']} healthy")
            print(f"  Tasks: {report['tasks']['total_completed']} completed, "
                  f"{report['tasks']['errors']} errors")

            # Save state after each cycle
            if cycle % 5 == 0:
                self.save_state()

            # Wait for next cycle (unless single-shot)
            if cycles <= 0 or cycle < cycles:
                try:
                    time.sleep(interval)
                except KeyboardInterrupt:
                    break

        print(f"\n{'=' * 60}")
        print("MASTER CONTROL — FINAL REPORT")
        print("=" * 60)
        final_report = self.generate_report()
        print(json.dumps(final_report, indent=2))
        self.save_state()

        print(f"\n{'=' * 60}")
        print("✓ MASTER CONTROL SHUTDOWN COMPLETE")
        print(f"  Total Cycles: {self.cycle_count}")
        print(f"  Total Tasks: {self.total_tasks_processed}")
        print(f"  Total Errors: {self.errors}")
        print("=" * 60)

        return final_report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='ZYN Empire Master Controller')
    parser.add_argument('--cycles', type=int, default=1,
                        help='Number of cycles to run (0 for infinite)')
    parser.add_argument('--interval', type=int, default=60,
                        help='Seconds between cycles')

    args = parser.parse_args()

    master = MasterController()
    master.run(cycles=args.cycles, interval=args.interval)