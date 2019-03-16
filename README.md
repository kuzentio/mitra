# Mitra

### How to run it locally

Requirements:
*    Docker = 2.0.0
*    docker-compose = 1.23.2 

#### For install project make sure that ports

(8000, 5432, 5672, [7000-7500]) are not allocated.

then run

``make init``
``make start``

#### For install project make sure that ports
(8000, 5432, 5672, [7000-7500]) are not allocated.

Here is list of Make command tasted on OSX:
*    init - initing project 
*    start - start docker-compose
*    stop - down all containers from docker-compose
*    restart - alias for run down/up command. 
*    destroy - removes all docker stuf from host machine
*    test - run ``manage.py tests`` inside container  
*    codestyle - runs codestyles checks
*    shell_plus - alias for ``manage.py shell_plus``

It could be an issue if try to run tests before container were provisioned,
then try to wait until provision would be done, then run ``make test``
