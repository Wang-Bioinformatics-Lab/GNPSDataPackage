from gnpsdata import taskresult


def get_unfiltered_pairs_dataframe(task):
    view_name = "view_results"

    df = taskresult.get_task_resultview_dataframe(task, view_name)

    return df