DAY_RANGE = 30 # The range of days to import data from

metrics = [
    {
        "name":"messages",
        "path":"search_time_series",
        "includeTimeframe": True
    },

    {
        "name":"tags",
        "path":"all_time_series"
    },

    {
        "name":"senders",
        "path":"time_series",
        "required":"address",
    },

    {
        "name":"urls",
        "path":"time_series",
        "required":"url",
    },

    {
        "name":"templates",
        "path":"time_series",
        "required":"name",
    },

    {
        "name":"webhooks",
        "path":"list"
    },

    {
        "name":"subaccounts",
        "path":"list"
    },
    # it is very important to leave the exports metric as the last metric
    # since it can take a long time for it to resolve
    {
        "name":"exports",
        "path": "activity"
    }
]
# add a default category which equals to the name if category was not specified
metrics = [dict(category=metric.pop('category', metric.get('name')), **metric) for metric in metrics]

