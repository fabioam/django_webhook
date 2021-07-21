import hashlib
import hmac
import sys
import os
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

def validate_signature(payload, secret):
    # Get the signature from the payload
    signature_header = payload.headers.get('X-Hub-Signature')
    sha_name, github_signature = signature_header.split('=')
    if sha_name != 'sha1':
        print('ERROR: X-Hub-Signature in payload headers was not sha1=****')
        return False

    # Create our own signature
    body = payload.body
    local_signature = hmac.new(secret.encode('utf-8'), msg=body, digestmod=hashlib.sha1)

    # See if they match
    return hmac.compare_digest(local_signature.hexdigest(), github_signature)

@csrf_exempt
def webhook_post(request):
    if request.method == "POST":
        if validate_signature(request, settings.GITHUB_REPOS_SIGNATURE):
            data = json.loads(request.body.decode('utf-8'))

            if data.get('repository').get('full_name') == settings.GITHUB_REPOS_NAME\
                    and data.get('ref').replace('refs/heads/', '') == settings.GITHUB_REPOS_BRANCH:

                os.chdir(settings.LOCAL_REPOS_PATH)

                popen_output = 'Webhook starting from %s:' % os.popen('pwd').read()

                for command in settings.COMMAND_LIST:
                    popen_output += os.popen(command).read()

                return HttpResponse(popen_output)
        else:
            return HttpResponse("invalide signature")
    else:
        return HttpResponse('method not allowed')


@csrf_exempt
def webhook_post_test(request):

    # os.system('git pull origin %s' % settings.GITHUB_REPOS_BRANCH)

    os.chdir(settings.LOCAL_REPOS_PATH)
    popen_output = 'Webhook starting from %s:\n' % os.popen('pwd').read()

    for command in settings.COMMAND_LIST:
        popen_output += os.popen(command).read()

    # popen_output += os.popen('git pull origin %s' % settings.GITHUB_REPOS_BRANCH).read()
    # popen_output += os.popen('yarn install').read()

    # os.system('yarn build')
    # os.system('pm2 stop %s' % settings.PM2_PROCESS_NAME)
    # os.system('pm2 start %s' % settings.PM2_PROCESS_NAME)
    # os.system('pm2 reload %s' % settings.PM2_PROCESS_NAME)

    return HttpResponse(popen_output)
