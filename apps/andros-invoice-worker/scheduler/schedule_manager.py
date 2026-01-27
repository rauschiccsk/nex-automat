"""
Temporal Schedule Manager for ANDROS Invoice Worker.

Manages scheduled workflows for automatic invoice fetching from suppliers.
"""

import logging
from datetime import timedelta
from typing import Optional

from temporalio.client import Client, ScheduleAlreadyRunningError
from temporalio.client import (
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleIntervalSpec,
    ScheduleSpec,
    ScheduleState,
    SchedulePolicy,
    ScheduleOverlapPolicy,
)

logger = logging.getLogger(__name__)


class ScheduleManager:
    """Manages Temporal Schedules for supplier invoice workflows."""

    def __init__(self, client: Client, task_queue: str = "andros-invoice-queue"):
        """
        Initialize schedule manager.

        Args:
            client: Temporal client
            task_queue: Task queue for workflows
        """
        self.client = client
        self.task_queue = task_queue

    async def create_marso_schedule(
        self,
        schedule_id: str = "andros-marso-daily",
        cron_expression: str = "0 6 * * *",
        lookback_days: int = 7,
        customer_code: str = "ANDROS",
        paused: bool = False,
    ) -> str:
        """
        Create or update MARSO invoice fetch schedule.

        Args:
            schedule_id: Unique schedule identifier
            cron_expression: Cron expression (default: daily at 6:00)
            lookback_days: Number of days to look back for invoices
            customer_code: Customer code for multi-tenant support
            paused: Whether to create schedule in paused state

        Returns:
            Schedule ID
        """
        from datetime import date, timedelta

        # Calculate date range
        today = date.today()
        date_from = (today - timedelta(days=lookback_days)).isoformat()
        date_to = today.isoformat()

        schedule = Schedule(
            action=ScheduleActionStartWorkflow(
                "ANDROSInvoiceWorkflow",
                args=[
                    "marso",           # supplier_id
                    date_from,         # date_from
                    date_to,           # date_to
                    customer_code,     # customer_code
                    True,              # skip_pipeline
                ],
                id=f"{schedule_id}-{{{{.ScheduledTime.Format \"2006-01-02\"}}}}",
                task_queue=self.task_queue,
            ),
            spec=ScheduleSpec(
                cron_expressions=[cron_expression],
            ),
            state=ScheduleState(
                paused=paused,
                note=f"MARSO invoice fetch for {customer_code}",
            ),
            policy=SchedulePolicy(
                overlap=ScheduleOverlapPolicy.SKIP,
                catchup_window=timedelta(hours=1),
            ),
        )

        try:
            handle = await self.client.create_schedule(
                schedule_id,
                schedule,
            )
            logger.info(f"Created schedule: {schedule_id}")
            return schedule_id
        except ScheduleAlreadyRunningError:
            # Update existing schedule
            handle = self.client.get_schedule_handle(schedule_id)
            await handle.update(lambda _: schedule)
            logger.info(f"Updated existing schedule: {schedule_id}")
            return schedule_id

    async def create_supplier_schedule(
        self,
        supplier_id: str,
        schedule_id: Optional[str] = None,
        cron_expression: str = "0 6 * * *",
        lookback_days: int = 7,
        customer_code: str = "ANDROS",
        paused: bool = False,
    ) -> str:
        """
        Create schedule for any supplier.

        Args:
            supplier_id: Supplier identifier (marso, continental, etc.)
            schedule_id: Schedule ID (auto-generated if not provided)
            cron_expression: Cron expression
            lookback_days: Days to look back
            customer_code: Customer code
            paused: Start paused

        Returns:
            Schedule ID
        """
        if schedule_id is None:
            schedule_id = f"andros-{supplier_id}-daily"

        from datetime import date, timedelta

        today = date.today()
        date_from = (today - timedelta(days=lookback_days)).isoformat()
        date_to = today.isoformat()

        schedule = Schedule(
            action=ScheduleActionStartWorkflow(
                "ANDROSInvoiceWorkflow",
                args=[supplier_id, date_from, date_to, customer_code, False],
                id=f"{schedule_id}-{{{{.ScheduledTime.Format \"2006-01-02\"}}}}",
                task_queue=self.task_queue,
            ),
            spec=ScheduleSpec(
                cron_expressions=[cron_expression],
            ),
            state=ScheduleState(
                paused=paused,
                note=f"{supplier_id.upper()} invoice fetch for {customer_code}",
            ),
            policy=SchedulePolicy(
                overlap=ScheduleOverlapPolicy.SKIP,
                catchup_window=timedelta(hours=1),
            ),
        )

        try:
            await self.client.create_schedule(schedule_id, schedule)
            logger.info(f"Created schedule: {schedule_id}")
        except ScheduleAlreadyRunningError:
            handle = self.client.get_schedule_handle(schedule_id)
            await handle.update(lambda _: schedule)
            logger.info(f"Updated schedule: {schedule_id}")

        return schedule_id

    async def pause_schedule(self, schedule_id: str) -> None:
        """Pause a schedule."""
        handle = self.client.get_schedule_handle(schedule_id)
        await handle.pause(note="Paused by ScheduleManager")
        logger.info(f"Paused schedule: {schedule_id}")

    async def unpause_schedule(self, schedule_id: str) -> None:
        """Unpause a schedule."""
        handle = self.client.get_schedule_handle(schedule_id)
        await handle.unpause(note="Unpaused by ScheduleManager")
        logger.info(f"Unpaused schedule: {schedule_id}")

    async def trigger_now(self, schedule_id: str) -> None:
        """Trigger a schedule to run immediately."""
        handle = self.client.get_schedule_handle(schedule_id)
        await handle.trigger()
        logger.info(f"Triggered schedule: {schedule_id}")

    async def delete_schedule(self, schedule_id: str) -> None:
        """Delete a schedule."""
        handle = self.client.get_schedule_handle(schedule_id)
        await handle.delete()
        logger.info(f"Deleted schedule: {schedule_id}")

    async def list_schedules(self) -> list:
        """List all ANDROS schedules."""
        schedules = []
        async for schedule in self.client.list_schedules():
            if schedule.id.startswith("andros-"):
                schedules.append({
                    "id": schedule.id,
                    "paused": schedule.info.paused if schedule.info else False,
                })
        return schedules

    async def get_schedule_info(self, schedule_id: str) -> dict:
        """Get detailed schedule information."""
        handle = self.client.get_schedule_handle(schedule_id)
        desc = await handle.describe()

        return {
            "id": schedule_id,
            "paused": desc.schedule.state.paused if desc.schedule.state else False,
            "note": desc.schedule.state.note if desc.schedule.state else "",
            "recent_actions": len(desc.info.recent_actions) if desc.info else 0,
            "next_action_times": [
                t.isoformat() for t in (desc.info.next_action_times or [])[:3]
            ] if desc.info else [],
        }
