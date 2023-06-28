import aiohttp
import asyncio
import json
import traceback
import urllib.parse

from aiohttp import web
from lib.settings import Settings


class Salesforce:
    access_token = None
    instance_url = None
    browser_url = ""

async def simple_get(use_url, headers={}):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(use_url) as resp:
            res = await resp.json()
            if resp.status > 299:
                print("resp.status:{0}".format(resp.status))
                print("resp:{0}".format(resp))
                print("res:{0}".format(res))
            return resp.status, res

async def simple_post(use_url, data={}):
    async with aiohttp.ClientSession() as session:
        async with session.post(use_url, json=data) as resp:
            res = await resp.json()
            if resp.status > 299:
                print(resp, res)
            return res

async def salesforce_get(url, attempts=0):
    headers = {"Accept":"application/json",
            "Authorization":"Bearer {0}".format(Salesforce.access_token)}
    status, res = await simple_get(url, headers)
    if status > 299:
        if attempts == 0:
            print('salesforce_get failed.  Generating a new token and retrying.')
            await get_salesforce_token()
            res = await salesforce_get(url, attempts+1)
        else:
            print('salesforce_get failed a second time.  Not retrying again.')
    return res

def get_salesforce_browser_url(instance_url):
    browser_url_template = instance_url.replace(".my.salesforce.",".lightning.force.")
    browser_url_template += "/lightning/r/Contact/{0}/view"
    return browser_url_template

async def get_salesforce_token():
    url = "https://login.salesforce.com/services/oauth2/token?"
    url += "client_id={0}&".format(Settings.sf_client_id)
    url += "client_secret={0}&".format(Settings.sf_client_secret)
    url += "username={0}&".format(Settings.sf_username)
    url += "password={0}&grant_type=password".format(Settings.sf_password)
    print('get_salesforce_token url:{0}'.format(url))
    res = await simple_post(url)
    print('get_salesforce_token res:{0}'.format(res))
    Salesforce.access_token = res.get('access_token')
    Salesforce.instance_url = res.get('instance_url')
    Salesforce.browser_url = get_salesforce_browser_url(res.get('instance_url'))
    return res

async def salesforce_query(select_items, phone_number):
    url_path = "/services/data/v53.0/query?"
    url_template = Salesforce.instance_url + url_path + "q=SELECT+{0}+FROM+Contact+WHERE+phone='{1}'"
    url = url_template.format(select_items, phone_number)
    print("Querying Salesforce for: {0}".format(url))
    data = await salesforce_get(url)
    return data

async def get_salesforce_contact(select_items, caller_id, secondary_caller_id):
    data = {}
    browser_url = ""
    if secondary_caller_id:
        data = await salesforce_query(select_items, urllib.parse.quote_plus(secondary_caller_id))
    if data == {} or len(data.get('records', [])) == 0:
        data = await salesforce_query(select_items, caller_id)
    print("Salesforce API resp:{0}".format(data))
    if len(data.get('records', [])) > 0:
        data = data['records'][0]
        data =  {k.lower(): v for k, v in data.items()}
        browser_url = Salesforce.browser_url.format(data["id"])
    return data, browser_url


async def page_handle(request):
    print('serving index.html')
    return web.FileResponse('./static/index.html')

async def api(request):
    """
    POST requests from the UI 
    """
    body = await request.json()
    default_error_msg = "A unknown error occurred."
    response = {}
    try:
        integration = body.get('integration')
        caller_id = body.get('caller_id')
        secondary_caller_id = body.get('secondary_caller_id')
        print("integration:{0}".format(integration))
        print("caller_id:{0}".format(caller_id))
        print("secondary_caller_id:{0}".format(secondary_caller_id))
        if integration == "mockapi":
            use_url = Settings.mockapi_url + caller_id
            status, data = await simple_get(use_url)
            if type(data) == list and len(data) > 0:
                data = data[0]
            response = {'url': use_url, 'data': data}
        else:#salesforce
            select_items = "Id,name,AccountId,phone,email"
            data, browser_url = await get_salesforce_contact(select_items, caller_id, secondary_caller_id)
            response = {'url': browser_url, 'data': data}
    except Exception as e:
        response = {"error": default_error_msg}
        traceback.print_exc()
    print(response)
    return web.Response(text=json.dumps(response))

async def url(request):
    """
    POST requests from the UI 
    """
    body = await request.json()
    default_error_msg = "A unknown error occurred."
    response = {}
    try:
        integration = body.get('integration')
        caller_id = body.get('caller_id')
        secondary_caller_id = body.get('secondary_caller_id')
        print(integration)
        print(caller_id)
        print("secondary_caller_id:{0}".format(secondary_caller_id))
        if integration == "mockapi":
            use_url = Settings.mockapi_url + caller_id
            response['url'] = use_url
        else:
            select_items = "Id"
            data, browser_url = await get_salesforce_contact(select_items, caller_id, secondary_caller_id)
            response['url'] = browser_url
    except Exception as e:
        response = {"error": default_error_msg}
        traceback.print_exc()
    print(response)
    return web.Response(text=json.dumps(response))

async def options(request):
    """
    POST requests from the UI 
    """
    default_error_msg = "A unknown error occurred."
    response = {"mockapi":False, "salesforce":False}
    try:
        if Settings.sf_client_id and Settings.sf_client_secret:
            response["salesforce"] = True
        if Settings.mockapi_url:
            response["mockapi"] = True
    except Exception as e:
        response = {"error": default_error_msg}
        traceback.print_exc()
    #print(response)
    return web.Response(text=json.dumps(response))

app = web.Application()
app.add_routes([web.get('/', page_handle),
                web.post('/api', api),
                web.post('/url', url),
                web.post('/options', options),
               ])

if __name__ == '__main__':
    if Settings.sf_client_id and Settings.sf_client_secret:
        asyncio.run(get_salesforce_token())
        print("Salesforce.access_token: {0}".format(Salesforce.access_token))
    else:
        print("No Salesforce Client App configured.  Salesforce will not be an option as a result.")
    web.run_app(app, port=Settings.port)