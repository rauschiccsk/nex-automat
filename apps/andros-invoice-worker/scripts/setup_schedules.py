#!/usr/bin/env python
"""
Setup Temporal Schedules for ANDROS Invoice Worker.

Creates schedules for automatic invoice fetching from suppliers.

Usage:
    python setup_schedules.py [--temporal-host HOST] [--temporal-port PORT]
    python setup_schedules.py --list
    python setup_schedules.py --trigger marso
    python setup_schedules.py --pause marso
    python setup_schedules.py --unpause marso
"""

import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scheduler.schedule_manager import ScheduleManager
from temporalio.client import Client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def setup_all_schedules(manager: ScheduleManager) -> None:
    """Create all supplier schedules."""
    logger.info("Setting up ANDROS invoice schedules...")

    # MARSO - daily at 6:00, lookback 7 days
    await manager.create_marso_schedule(
        schedule_id="andros-marso-daily",
        cron_expression="0 6 * * *",
        lookback_days=7,
        customer_code="ANDROS",
    )
    logger.info("✓ MARSO schedule created: andros-marso-daily (6:00 daily)")

    # Future suppliers can be added here:
    # await manager.create_supplier_schedule(
    #     supplier_id="continental",
    #     cron_expression="0 7 * * *",
    #     lookback_days=7,
    # )

    logger.info("All schedules configured successfully!")


async def list_schedules(manager: ScheduleManager) -> None:
    """List all ANDROS schedules."""
    schedules = await manager.list_schedules()

    if not schedules:
        print("No ANDROS schedules found.")
        return

    print("\nANDROS Invoice Schedules:")
    print("-" * 50)
    for s in schedules:
        status = "PAUSED" if s["paused"] else "ACTIVE"
        print(f"  {s['id']}: {status}")

        # Get detailed info
        try:
            info = await manager.get_schedule_info(s["id"])
            if info["next_action_times"]:
                print(f"    Next run: {info['next_action_times'][0]}")
        except Exception:
            pass
    print("-" * 50)


async def trigger_schedule(manager: ScheduleManager, supplier: str) -> None:
    """Trigger a schedule immediately."""
    schedule_id = f"andros-{supplier}-daily"
    await manager.trigger_now(schedule_id)
    print(f"Triggered schedule: {schedule_id}")


async def pause_schedule(manager: ScheduleManager, supplier: str) -> None:
    """Pause a schedule."""
    schedule_id = f"andros-{supplier}-daily"
    await manager.pause_schedule(schedule_id)
    print(f"Paused schedule: {schedule_id}")


async def unpause_schedule(manager: ScheduleManager, supplier: str) -> None:
    """Unpause a schedule."""
    schedule_id = f"andros-{supplier}-daily"
    await manager.unpause_schedule(schedule_id)
    print(f"Unpaused schedule: {schedule_id}")


async def main():
    parser = argparse.ArgumentParser(
        description="Setup and manage ANDROS invoice schedules"
    )
    parser.add_argument(
        "--temporal-host",
        default=os.environ.get("TEMPORAL_HOST", "localhost"),
        help="Temporal server host",
    )
    parser.add_argument(
        "--temporal-port",
        type=int,
        default=int(os.environ.get("TEMPORAL_PORT", "7233")),
        help="Temporal server port",
    )
    parser.add_argument(
        "--task-queue",
        default=os.environ.get("TEMPORAL_TASK_QUEUE", "andros-invoice-queue"),
        help="Temporal task queue",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all schedules",
    )
    parser.add_argument(
        "--trigger",
        metavar="SUPPLIER",
        help="Trigger schedule for supplier (e.g., marso)",
    )
    parser.add_argument(
        "--pause",
        metavar="SUPPLIER",
        help="Pause schedule for supplier",
    )
    parser.add_argument(
        "--unpause",
        metavar="SUPPLIER",
        help="Unpause schedule for supplier",
    )

    args = parser.parse_args()

    # Connect to Temporal
    temporal_address = f"{args.temporal_host}:{args.temporal_port}"
    logger.info(f"Connecting to Temporal at {temporal_address}")

    try:
        client = await Client.connect(temporal_address)
    except Exception as e:
        logger.error(f"Failed to connect to Temporal: {e}")
        sys.exit(1)

    manager = ScheduleManager(client, task_queue=args.task_queue)

    # Execute requested action
    if args.list:
        await list_schedules(manager)
    elif args.trigger:
        await trigger_schedule(manager, args.trigger)
    elif args.pause:
        await pause_schedule(manager, args.pause)
    elif args.unpause:
        await unpause_schedule(manager, args.unpause)
    else:
        # Default: setup all schedules
        await setup_all_schedules(manager)


if __name__ == "__main__":
    asyncio.run(main())
