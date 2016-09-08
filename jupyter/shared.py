import numpy as np
import sys
import os

wk_dir = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(
        os.path.abspath(os.path.join(wk_dir, '..')))


from source.helpers.db import fetch

# indexes that make accessing values in X and Y more verbose

OPEN_ISSUES_COUNT = 0
SIZE = 1
DEPENDENCIES_COUNT = 2
MAINTAINERS_COUNT = 3
CONTRIBUTORS_COUNT = 4
HAS_TESTS = 5
HAS_README = 6

STARS = 0
FORKS = 1
SUBSCRIBERS = 2
TOTAL_DOWNLOADS = 3
AVERAGE_PER_MONTH_DOWNLOADS = 4
LAST_MONTH_DOWNLOADS = 5
LAST_WEEK_DOWNLOADS = 6


def fetch_data():
    result = fetch((
    "SELECT stargazers_count, forks_count,"
            "open_issues_count, size, subscribers_count,"
            "dependencies_count, mainteiners_count,"
            "contributors_count, has_tests, has_readme,"
            "total_downloads.downloads, m_average_downloads.avg,"
            "last_month_downloads.downloads,"
            "last_week_downloads.downloads "
    "FROM repos AS r "
    "INNER JOIN m_average_downloads ON r.id = m_average_downloads.repo_id "
    "INNER JOIN total_downloads ON r.id = total_downloads.repo_id "
    "INNER JOIN last_month_downloads ON r.id = last_month_downloads.repo_id "
    "INNER JOIN last_week_downloads ON r.id = last_week_downloads.repo_id "
    "WHERE has_readme is not Null "
    "ORDER BY RANDOM();"
    ))

    X_tmp = []
    Y_tmp = []
    for r in result:
        y = [r[0], r[1], r[4], r[10], r[11], r[12], r[13]]
        x = [r[2], r[3], r[5], r[6], r[7], int(r[8]), int(r[9])]
        X_tmp.append(x)
        Y_tmp.append(y)

    # X_labels and Y_labels correspond with what is in X and Y, they mark  what columns represent what values
    X_labels = ["open_issues_count", "size", "dependencies_count",
                "mainteiners_count", "contributors_count", "has_tests", "has_readme"]
    Y_labels = ["stars", "forks", "subscribers", "downloads",
                "avg_per_month", "last_month_downloads", "last_week_downloads"]
    X = np.array(X_tmp, dtype=np.float64)
    Y = np.array(Y_tmp, dtype=np.float64)
    return (X, Y, X_labels, Y_labels)
