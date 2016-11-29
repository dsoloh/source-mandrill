BASE_URL = "https://mandrillapp.com/api/1.0/"

DAY_RANGE = 30 # The range of days to import data from

metrics = [
    {
        "name":"messages",
        "path":"search_time_series"
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
    }
]
# add a default category which equals to the name if category was not specified
metrics = [dict(category=metric.pop('category', metric.get('name')), **metric) for metric in metrics]

