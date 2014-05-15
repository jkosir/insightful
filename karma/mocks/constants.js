var constants = {
    staticUrl: /static/,
    website: {"url": "http://www.google.com/", "id": 1, "name": "Test website", "user": 1},
    series: [
        ["page_views", "Page views"],
        ["visits", "Visits"],
        ["avg_duration", "Average view duration"],
        ["avg_active_duration", "Average engagement time"]
    ],
    // urls for json views
    urls: {
        overview: '/api/1/overview/',
        engagement: '/api/1/engagement/',
        monthlychart: '/api/1/monthlychart/'
    }
};