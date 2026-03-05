"""
Temporal Schedule Manager for invoice workers.

Manages scheduled workflows for automatic invoice fetching from suppliers.
Tenant-aware: schedule IDs and workflow names adapt to current tenant.
"""

import logging
from datetime import timedelta

from nex_invoice_worker.config.tenant import WorkerTenant, get_tenant
from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleAlreadyRunningError,
    ScheduleOverlapPolicy,
    SchedulePolicy,
    ScheduleSpec,
    ScheduleState,
)

logger = logging.getLogger(__name__)

# Tenant-specific schedule prefix
_SCHEDULE_PREFIX = {
    WorkerTenant.SUPPLIER: "supplier",
    WorkerTenant.ANDROS: "andros",
}


class ScheduleManager:
    """Manages Temporal Schedules for supplier invoice workflows."""

    def __init__(self, client: Client, task_queue: str = ""):
        """
        Initialize schedule manager.

        Args:
            client: Temporal client
            task_queue: Task queue for workflows (auto-detected if empty)
        """
        self.client = client
        self.tenant = get_tenant()
        if not task_queue:
            from nex_invoice_worker.config.settings import get_settings

            task_queue = get_settings().temporal_task_queue
        self.task_queue = task_queue
        self._prefix = _SCHEDULE_PREFIX[self.tenant]

    async def create_supplier_schedule(
        self,
        supplier_id: str,
        schedule_id: str | None = None,
        cron_expression: str = "0 6 * * *",
        lookback_days: int = 7,
        customer_code: str = "",
        paused: bool = False,
        skip_pipeline: bool = False,
    ) -> str:
        """
        Create schedule for a supplier.

        Args:
            supplier_id: Supplier identifier (marso, continental, etc.)
            schedule_id: Schedule ID (auto-generated if not provided)
            cron_expression: Cron expression
            lookback_days: Days to look back
            customer_code: Customer code (auto-detected from tenant if empty)
            paused: Start paused
            skip_pipeline: Skip posting to pipeline

        Returns:
            Schedule ID
        """
        if schedule_id is None:
            schedule_id = f"{self._prefix}-{supplier_id}-daily"

        if not customer_code:
            customer_code = "ANDROS" if self.tenant == WorkerTenant.ANDROS else "ICC"

        from datetime import date

        today = date.today()
        date_from = (today - timedelta(days=lookback_days)).isoformat()
        date_to = today.isoformat()

        schedule = Schedule(
            action=ScheduleActionStartWorkflow(
                "InvoiceAPIWorkflow",
                args=[supplier_id, date_from, date_to, customer_code, skip_pipeline],
                id=f'{schedule_id}-{{{{.ScheduledTime.Format "2006-01-02"}}}}',
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

    async def create_marso_schedule(
        self,
        schedule_id: str | None = None,
        cron_expression: str = "0 6 * * *",
        lookback_days: int = 7,
        customer_code: str = "",
        paused: bool = False,
    ) -> str:
        """Create MARSO-specific schedule (convenience method)."""
        if schedule_id is None:
            schedule_id = f"{self._prefix}-marso-daily"

        skip_pipeline = self.tenant == WorkerTenant.ANDROS

        return await self.create_supplier_schedule(
            supplier_id="marso",
            schedule_id=schedule_id,
            cron_expression=cron_expression,
            lookback_days=lookback_days,
            customer_code=customer_code,
            paused=paused,
            skip_pipeline=skip_pipeline,
        )

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
        """List schedules for current tenant."""
        schedules = []
        async for schedule in self.client.list_schedules():
            if schedule.id.startswith(f"{self._prefix}-"):
                schedules.append(
                    {
                        "id": schedule.id,
                        "paused": schedule.info.paused if schedule.info else False,
                    }
                )
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
            ]
            if desc.info
            else [],
        }
