from gnpsdata import taskresult


# This gets us the results as a data frame
def get_results_dataframe(task):
    view_name = "query_results"

    df = taskresult.get_task_resultview_dataframe(task, view_name)

    return df

def get_extractionresults_dataframe(task):
    view_name = "extract_results"

    df = taskresult.get_task_resultview_dataframe(task, view_name)

    return df