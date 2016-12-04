DAY_RANGE = 30 # The range of days to import data from

metrics = [

    # it is very important to leave the exports metric as the last metric
    # since it can take a long time for it to resolve
    {
        "name":"exports",
        "path": "activity",
        "includeTimeframe": True
    }
]
# add a default category which equals to the name if category was not specified
metrics = [dict(category=metric.pop('category', metric.get('name')), **metric) for metric in metrics]

