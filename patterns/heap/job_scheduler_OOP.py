"""
Problem: Job Scheduler
Pattern: Python OOP + heap / scheduled work

Prompt:
    Implement a simple job scheduler.

    Each job has:
        - job_id
        - run_at timestamp

    Support:
        - schedule(job_id, run_at)
        - pop_ready(current_time)

    pop_ready(current_time) returns all job IDs whose run_at <= current_time.

Implementation:
    Use a heap so the earliest scheduled job is always available first.

Distributed-systems idea:
    Scheduled background work, delayed jobs, retry queues, task orchestration.

Python idea:
    heapq is a min-heap.
    For tuples (run_at, job_id), the earliest run_at is at heap[0].
"""

import heapq


class JobScheduler:
    def __init__(self):
        self.heap = []

    def schedule(self, job_id: str, run_at: int) -> None:
        heapq.heappush(self.heap, (run_at, job_id))

    def pop_ready(self, current_time: int) -> list[str]:
        ready = []

        while self.heap and self.heap[0][0] <= current_time:
            run_at, job_id = heapq.heappop(self.heap)
            ready.append(job_id)

        return ready


def main():
    scheduler = JobScheduler()

    scheduler.schedule("job-b", 110)
    scheduler.schedule("job-a", 100)
    scheduler.schedule("job-c", 105)

    assert scheduler.pop_ready(99) == []
    assert scheduler.pop_ready(100) == ["job-a"]
    assert scheduler.pop_ready(106) == ["job-c"]
    assert scheduler.pop_ready(120) == ["job-b"]

    scheduler2 = JobScheduler()
    scheduler2.schedule("job-b", 100)
    scheduler2.schedule("job-a", 100)

    assert scheduler2.pop_ready(100) == ["job-a", "job-b"]

    print("All tests passed.")


if __name__ == "__main__":
    main()
