

import heroku3
import requests
from heroku3.api import Heroku

from apps.profile_app.models import HerokuCredentials

API_KEY = '9b90fb1c-5b9b-4942-8502-c17e9df9ac37'

heroku_connection = heroku3.from_key(API_KEY)


class HerokuClient(Heroku):

    def create_application(self, user_id):
        try:
            credentials = HerokuCredentials.objects.get(user_id=user_id)
        except (HerokuCredentials.DoesNotExist, HerokuCredentials.MultipleObjectsReturned):
            return 'Could not find heroku credentials for this user.'

        url = 'https://api.heroku.com/app-setups'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.heroku+json; version=3',
            'Authorization': 'Bearer {}'.format(credentials.api_key)
        }
        data = {
            "source_blob": {
                "url": "https://github.com/kuzentio/gbot-trader/tarball/master/"
            }
        }
        response = requests.post(
            url,
            data=data,
            headers=headers
        )
        print(response.json)
        if not response.status_code == 202:  # TODO: review!
            return 'Failed!'

