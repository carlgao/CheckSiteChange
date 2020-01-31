import os
from datetime import datetime
from urllib.request import Request, urlopen


SITE = "https://alumni.harvard.edu/reunions/accommodations"
EXPECTED = os.environ["EXPECTED"]

ACCOUNT_SID = os.environ["ACCOUNT_SID"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]

TO_PHONE = os.environ["TO_PHONE"]
FROM_PHONE = os.environ["FROM_PHONE"]

VOICE_TWIML_URL = os.environ["VOICE_TWIML_URL"]
TEXT_MESSAGE = os.environ["TEXT_MESSAGE"]


def validate(res):
    return EXPECTED in res


def lambda_handler(_event, _context):
    print("Checking {} at {}...".format(SITE, str(datetime.now())))
    ret = None
    try:
        req = Request(SITE, headers={"User-Agent": "AWS Lambda"})
        if validate(str(urlopen(req).read())):
            print("No change...")
        else:
            print("CHANGE DETECTED!")
            ret = "NEW"

            # Download the helper library from https://www.twilio.com/docs/python/install
            from twilio.rest import Client

            # Account Sid and Auth Token from twilio.com/console
            client = Client(ACCOUNT_SID, AUTH_TOKEN)

            call = client.calls.create(
                url=VOICE_TWIML_URL, to=TO_PHONE, from_=FROM_PHONE,
            )

            print("Call SID", call.sid)

            message = client.messages.create(
                body=TEXT_MESSAGE, from_=TO_PHONE, to=FROM_PHONE,
            )

            print("Message SID", message.sid)
    except OSError as err:
        print("OSError:", err)
    except:
        import sys

        print("Exception:", sys.exc_info()[0])
    finally:
        print("Check complete at {}".format(str(datetime.now())))

    return ret


if __name__ == "__main__":
    lambda_handler(None, None)
