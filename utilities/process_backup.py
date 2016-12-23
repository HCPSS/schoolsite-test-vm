#!/usr/bin/env python
import os, time
from lib import BackupOptionResolver, SchoolMover
from multiprocessing.pool import Pool
from multiprocessing import cpu_count

options = BackupOptionResolver()

def process_school(school):
    """A wrapper so we can process this with a pool."""
    if school.code == "school":
        return False

    school.move()

    return True

if __name__ == '__main__':
    start = time.time()

    # Open a pool of worker, one worker per CPU.
    pool = Pool(processes=cpu_count())
    for subdir, dirs, files in os.walk(options.backup_location()):
        for filename in files:
            path        = os.path.join(subdir, filename)
            school_code = filename.split("-")[0].split("_", 2)[-1];

            school = SchoolMover(path, school_code, options.destination())
            pool.apply_async(process_school, [school])

    # Wait for our asynchronous operations.
    pool.close()
    pool.join()

    print("Done")
