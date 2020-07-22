Testing
=======

The root directory is also a working Django project. The login credentials are: admin/admin

When a model is sortable, a tool-area link will be added that says "Change Order". Click this link, and you will be taken to the custom view where you can drag-and-drop the records into order.

Inlines may be drag-and-dropped into any order directly from the change form.

Unit and functional tests may be found in the ``app/tests.py`` file and run via:

    $ python manage.py test app
