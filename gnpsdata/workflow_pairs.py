from gnpsdata import taskresult


def get_unfiltered_pairs_dataframe(task):
    view_name = "view_results"

    df = taskresult.download_task_resultview(task, view_name)

    return df