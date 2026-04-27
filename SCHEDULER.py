#!/usr/bin/env python3
"""
SCHEDULER.py - ZYN Empire Autonomous Task Scheduler
Automatic scheduling and orchestration of agent tasks
Version: 1.0
"""

import os
import sys
import json
import time
import logging
import threading
import io
from datetime import datetime, timedelta
from queue import Queue, PriorityQueue
import random

# Fix Windows console encoding
if sys.platform == 'win32':
      sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
      sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logging.basicConfig(
      level=logging.INFO,
      format='[%(asctime)s] [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

class TaskScheduler:
      """Manages task scheduling and execution timing"""

    def __init__(self):
              self.task_queue = PriorityQueue()
              self.scheduled_tasks = []
              self.execution_log = []
              logger.info("✓ TaskScheduler initialized")

    def schedule_task(self, task_name, execute_time, agent_id, task_data):
              """Schedule a task for specific execution time"""
              priority = self._calculate_priority(task_data)
              task = {
                  "id": f"TASK_{int(time.time()*1000)}",
                  "name": task_name,
                  "agent_id": agent_id,
                  "execute_time": execute_time,
                  "priority": priority,
                  "data": task_data,
                  "status": "SCHEDULED"
              }
              self.scheduled_tasks.append(task)
              logger.info(f"✓ Scheduled: {task_name} for agent {agent_id} at {execute_time}")
              return task["id"]

    def _calculate_priority(self, task_data):
              """Calculate task priority based on value and type"""
              value = task_data.get("value", 0)
              task_type = task_data.get("type", "general")

        priority_map = {
                      "closing": 1,
                      "proposal": 2,
                      "qualification": 3,
                      "outreach": 4,
                      "general": 5
        }
        return priority_map.get(task_type, 5) * (1 + value / 100000)

    def get_pending_tasks(self):
              """Get all tasks ready for execution"""
              now = datetime.now()
              pending = [t for t in self.scheduled_tasks 
                        if t["execute_time"] <= now and t["status"] == "SCHEDULED"]
              return pending

    def execute_scheduled_tasks(self):
              """Execute all pending tasks"""
              pending = self.get_pending_tasks()
              for task in pending:
                            task["status"] = "EXECUTED"
                            self.execution_log.append({
                                "task_id": task["id"],
                                "executed_at": datetime.now().isoformat(),
                                "agent_id": task["agent_id"]
                            })
                            logger.info(f"✓ Executed: {task['name']} (Agent {task['agent_id']})")
                        return len(pending)

    def generate_daily_schedule(self):
              """Generate automatic daily schedule for all agents"""
        agent_names = [
                      "Noah", "Sara", "Malik", "Elijah", "Adam", "Ruth", "Lea", "Zara", 
                      "Ezekiel", "Samson", "Cyrus", "Asher", "Rebecca", "Zuri", "Mariam",
                      "Enoch", "Juda", "Miro Fish", "Caleb"
        ]

        task_count = 0
        now = datetime.now()

        for hour in range(8, 18):  # 8am to 6pm
                      for i, agent_name in enumerate(agent_names):
                                        execute_time = now.replace(hour=hour, minute=random.randint(0, 59))

                task_types = ["outreach", "qualification", "proposal", "closing"]
                task_type = task_types[i % len(task_types)]

                task_data = {
                                      "type": task_type,
                                      "value": random.randint(5000, 500000),
                                      "agent": agent_name
                }

                self.schedule_task(
                                      f"{agent_name} - {task_type}",
                                      execute_time,
                                      i + 1,
                                      task_data
                )
                task_count += 1

        logger.info(f"✓ Generated {task_count} daily scheduled tasks")
        return task_count

class ExecutionMonitor:
      """Monitors task execution and performance"""

    def __init__(self):
              self.metrics = {
                            "total_executed": 0,
                            "total_failed": 0,
                            "avg_execution_time": 0,
                            "success_rate": 0.0
              }
              logger.info("✓ ExecutionMonitor initialized")

    def record_execution(self, task_id, status, duration):
              """Record task execution metrics"""
              if status == "success":
                            self.metrics["total_executed"] += 1
else:
            self.metrics["total_failed"] += 1

        self._update_metrics()

    def _update_metrics(self):
              """Update performance metrics"""
              total = self.metrics["total_executed"] + self.metrics["total_failed"]
              if total > 0:
                            self.metrics["success_rate"] = self.metrics["total_executed"] / total
                        logger.info(f"✓ Metrics updated: {total} tasks, {self.metrics['success_rate']:.1%} success")

    def get_report(self):
              """Get execution report"""
        return self.metrics

def main():
      """Main scheduler execution"""
    logger.info("\n" + "="*60)
    logger.info("ZYN EMPIRE - TASK SCHEDULER STARTED")
    logger.info("="*60)

    scheduler = TaskScheduler()
    monitor = ExecutionMonitor()

    # Generate daily schedule
    task_count = scheduler.generate_daily_schedule()

    # Execute pending tasks
    logger.info("\n" + "="*60)
    logger.info("EXECUTING SCHEDULED TASKS")
    logger.info("="*60)
    executed = scheduler.execute_scheduled_tasks()

    logger.info(f"\n✓ Scheduler complete: {executed}/{task_count} tasks executed")
    logger.info(f"Report: {monitor.get_report()}")
    logger.info("="*60 + "\n")

    return 0

if __name__ == "__main__":
      exit_code = main()
      sys.exit(exit_code)
