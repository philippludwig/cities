# Cities backend
This is the backed for the List of Cities web app as described in the task.

## Live installation
The application is currently available on [https://citylist.ml](https://citylist.ml), but
the access is password-protected. The backend runs in a docker container, for which the
Dockerfile can be found in this repository. Access control and CORS is handled by a proxy
Apache server.

## API
* The list of cities can be retrieved via the API endpoint `/cities`
* Cities can be accessed individually via a GET request to `/cities/<Name or ID of City`
* Cities and be added by issuing a PUT request with the name of the city to add, e.g. `PUT /cities/London`.

## Caching
Due to the limitation of the free plan of the openweathermap API, the `WeatherProvider` defined in
`cities/weather.py` caches the temperature of every City for 15 Minutes.

## Storage
All cities are stored in an in-memory dict; saving the list to a file or a database is not implemented (yet).

## Known problems
* There is hardly any error handling at this point, so if the weather API breaks down, the end user will not get a useful error message.
* Deleting cities is implemented, but untested: `DELETE /cities/London`
* If the user adds a lot of cities, this will most likely lead to problems with the openweathermap API limit.
* For some cities, need to use a different name. For example, for the city of თბილისი no temperature inforamation can be requested. The alias "Tbilisi" should be used in this case.

## Ideas / possible extensions
* Since we get more details about the weather in each city with the API requests to the openweathermap anyway, we could make more of this information available.
* A reset function could be implemented to restore the original state of the application (before any cities were added).
* Websockets or a similar technology could be used to push weather updates to the client (thereby avoiding the need of polling).
