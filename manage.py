#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    from dotenv import load_dotenv
    from pathlib import Path  # python3 only

    env_path = Path('.') / '.env.local'
    # load_dotenv(dotenv_path=env_path)
    load_dotenv(dotenv_path=str(env_path.absolute()))

    if os.environ.get('ENV') is not None:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.{}'.format(os.environ.get('ENV')))
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    # This allows easy placement of apps within the interior
    # arena directory.
    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(current_path, 'mitra'))

    execute_from_command_line(sys.argv)
