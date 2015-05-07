[![Build Status](https://travis-ci.org/jkosir/insightful.svg?branch=master)](https://travis-ci.org/jkosir/insightful)

Insightful
==========

Insightful is an open source web analytics platform, built with Django and adapted to Heroku platform.
After the installation, you'll be given a small bit of javascript code which should be included on websites
 you wish to to track.

Installation
============

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

#### Notes
* When running on other platforms modify settings.py accordingly
* Using with database backends other than PostgreSQL doesn't provide full timezone support

Tracking content
================
If you wish to track specific content add `data-track-name="Some name"` to elements you'd like to track.
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