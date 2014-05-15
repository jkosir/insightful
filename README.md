[![Build Status](https://travis-ci.org/dasf/insightful.svg?branch=master)](https://travis-ci.org/dasf/insightful)

Insightful
==========

Insightful is an open source web analytics platform, built with Django and adapted to Heroku platform.
After the installation, you'll be given a small bit of javascript code which should be included on websites
 you wish to to track.

Installation
============
#### Heroku

1. Install [heroku toolbelt](https://devcenter.heroku.com/articles/quickstart)
2. Clone this repository `git clone repo url`
3. Create heroku app `heroku create`
4. Add heroku remote url to repository `heroku git:remote -a "your application name"`
5. Push to heroku `git push heroku master`
6. Run syncdb `heroku run python manage.py syncdb --noinput`

#### Optional
* Install memcachier addon for better performance `heroku addons:add memcachier`

#### Notes
* When running on other platforms modify settings.py accordingly
* Using with database backends other than PostgreSQL doesn't provide full timezone support

Tracking content
================
If you wish to track specific content add `data-track-name="Some name"` to elements you wish to track.
Works best on bigger block elements such as paragraphs or container div's.

License
=======
Released under MIT license.


Roadmap
=======
* More coverage
* Actual jasmine tests
* Remove tracking code's jQuery dependency

Demo
====
Demo is available at [http://insightful-demo.herokuapp.com/](http://insightful-demo.herokuapp.com/)