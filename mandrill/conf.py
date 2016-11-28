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
        "path":"urls/time_series",
        "required":"url",
    },

    {
        "name":"templates",
        "path":"templates/time_series",
        "required":"name",
    },

    {
        "name":"webhooks",
        "path":"webhooks/list"
    },

    {
        "name":"subaccounts",
        "path":"subaccounts/list"
    }
]
# add a default category which equals to the name if category was not specified
metrics = [dict(category=x.pop('category', x.get('name')), **x) for x in metrics]
