Flask
=====

To use the *app factory* function outside of the main dashboard, import the factory and call it to create an instance of the Flask app. For example:

.. code-block:: python

    from sigmas import create_app

    app = create_app()

This approach allows you to create multiple instances of your app with different configurations, which is useful for testing and deployment.