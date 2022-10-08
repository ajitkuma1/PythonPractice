from json import dumps

from httplib2 import Http


def main():
    """Hangouts Chat incoming webhook quickstart."""

    
    url = "https://chat.googleapis.com/v1/spaces/AAAAZKAU1v4/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=u7Zp004b4SclHRxvTSBglVL5IcIhjInl5tlP_MSEH2Y%3D"

    bot_message = {
        'text': 'Hello from Cloud Vision!'}
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    print(response)


if __name__ == '__main__':
    main()
