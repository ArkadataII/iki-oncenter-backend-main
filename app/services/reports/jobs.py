import asyncio
import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ProcessPoolExecutor


class SchedulerService:

    async def task(self, **kwargs):
        print(kwargs.get('message'))
        res = httpx.get('http://127.0.0.1:5000/api/v1/sync/report/today', timeout=120)
        return res

    async def sync_report_today(self, **kwargs):
        tasks = []
        task = asyncio.create_task(self.task(**kwargs))
        tasks.append(task)
        await self.queue.join()

        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

    def start(self):
        self.queue = asyncio.Queue()
        self.sch = AsyncIOScheduler(job_defaults={'coalesce': False, 'max_instances': 2, 'replace_existing': True},
                                    executors={'default': {'type': 'threadpool', 'max_workers': 2},
                                               'processpool': ProcessPoolExecutor(max_workers=2)},
                                    timezone='Asia/Ho_Chi_Minh')
        self.sch.add_job(self.sync_report_today, 'interval', minutes=1, kwargs={"message": "Starting Job ..."})
        self.sch.start()


if __name__ == '__main__':
    sch_srv = SchedulerService()
    sch_srv.start()
