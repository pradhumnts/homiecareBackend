# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

account_sid = 'AC62d3d2229ae0ae99adac644e1c1c3012'
auth_token = '63dc14d2f0acd0d3ea7fe422a9897893'
client = Client(account_sid, auth_token)

def send_verification(phone):
    verification = client.verify \
                        .v2 \
                        .services('VAe15177029932eae73960dedd799695aa') \
                        .verifications \
                        .create(to=phone, channel='sms')

    print(verification.status)
    return verification.status

def check_verification(phone, code):
    verification_check = client.verify \
                           .v2 \
                           .services('VAe15177029932eae73960dedd799695aa') \
                           .verification_checks \
                           .create(to=phone, code=code)
    print(verification_check.status)
    return verification_check.status
