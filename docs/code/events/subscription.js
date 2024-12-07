const statistics_event = new EventSource(
    'https://example.com/gentec-meter/statistics-event'
);
statistics_event.onmessage = (event_data) => {
    console.log(JSON.parse(event_data));
};
statistics_event.onerror = (error) => {
    console.error(error);
};
statistics_event.onopen = () => {
    console.log('subscribed to statistics event');
}