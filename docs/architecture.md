![architecture](https://raw.githubusercontent.com/dusan-pilot/slack-integration/master/docs/arch.jpeg)

## layers:

- router
- controller
- view


## technical summary

- a user issues slack command to create request for specified url
- the router matches the url to a predefined route
- the controller action associated with the route is called
- the controller retrieves all of the necessary data, places the data in an array, and loads a view, passing along the data structure.
- the view accesses the structure of data and uses it to render the requested page i.e. to embed frame terminal