def select(inputlist, list_a, dep_dict, kpi):
    for item in inputlist:
        if item.r_value:
            list_a[item.month.strftime('%Y-%m-%d')] = item.r_value
        else:
            list_a[item.month.strftime('%Y-%m-%d')] = 'NA'
        list_sort = sorted(list_a.items(), key=lambda x: x[0])
        dep_dict[kpi] = {"t_value": item.groupkpi.t_value,
                         "l_limit": item.groupkpi.l_limit,
                         "r_value": dict(list_sort)}