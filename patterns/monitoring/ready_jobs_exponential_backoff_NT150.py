"""
Problem: Ready Jobs with Exponential Backoff
Rapid Pattern Drill Problem 5
Pattern: Retry queue / exponential backoff / scheduled retry
Status: Green review item

Prompt:
    You are given failed jobs. Each job has:
        (job_id, failed_at_time, retry_count)

    A job should be retried after:
        delay = base_delay * (2 ** retry_count)

    Return the job IDs that are ready to retry at current_time.

A job is ready if:
    failed_at_time + base_delay * (2 ** retry_count) <= current_time

Core idea:
    Iterate over jobs.
    Unpack each tuple.
    Compute delay.
    Compute next retry time.
    Compare to current_time.

Main traps:
    - `**` is exponentiation in Python.
    - `^` is not exponentiation in Python.
    - retry_count = 0 gives 2 ** 0 = 1, so the first retry waits one base delay.
    - Equality counts as ready here.
"""


def ready_jobs(
    failed_jobs: list[tuple[str, int, int]],
    current_time: int,
    base_delay: int
) -> list[str]:
    ready = []

    for job_id, failed_at_time, retry_count in failed_jobs:
        delay = base_delay * (2 ** retry_count)
        next_retry_time = failed_at_time + delay

        if next_retry_time <= current_time:
            ready.append(job_id)

    return ready


def main():
    failed_jobs = [
        ("job-a", 100, 0),
        ("job-b", 100, 1),
        ("job-c", 100, 2),
    ]

    assert ready_jobs(failed_jobs, current_time=103, base_delay=2) == ["job-a"]
    assert ready_jobs(failed_jobs, current_time=104, base_delay=2) == ["job-a", "job-b"]
    assert ready_jobs(failed_jobs, current_time=108, base_delay=2) == [
        "job-a", "job-b", "job-c"
    ]

    assert ready_jobs([], current_time=100, base_delay=2) == []

    print("All tests passed.")


if __name__ == "__main__":
    main()
