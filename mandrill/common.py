BASE_URL = "https://mandrillapp.com/api/1.0/"

DAY_RANGE = 30; # The range of days to import data from

metrics = [
    {
        "name":"messages",
        "path":"messages/search-time-series.json"
    },

    {
        "name":"tags",
        "path":"tags/all-time-series.json"
    },

    {
        "name":"senders",
        "path":"senders/time-series.json",
        "required":"address",
        "listpath":"senders/list.json"
    },

    {
        "name":"urls",
        "path":"urls/time-series.json",
        "required":"url",
        "listpath":"urls/list.json"
    },

    {
        "name":"templates",
        "path":"templates/time-series.json",
        "required":"name",
        "listpath":"templates/list.json"
    },

    {
        "name":"webhooks",
        "path":"webhooks/list.json"
    },

    {
        "name":"subaccounts",
        "path":"subaccounts/list.json"
    }
]
