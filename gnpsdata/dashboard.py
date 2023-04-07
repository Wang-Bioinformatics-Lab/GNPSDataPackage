import urllib.parse

def get_dashboard_viewer_linkout(usi, 
    xic_mz=None,
    xic_rt=None,
    ms2_scan=None):

    params = {}
    params["usi"] = usi
    if xic_mz is not None:
        params["xic_mz"] = xic_mz
    if xic_rt is not None:
        params["xic_rt_window"] = xic_rt
    if xic_mz is not None:
        params["ms2_identifier"] = "MS2:" + str(ms2_scan)
    

    return "https://dashboard.gnps2.org/?{}".format(urllib.parse.urlencode(params))