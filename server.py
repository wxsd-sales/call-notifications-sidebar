import aiohttp
import asyncio
import json
import logging
import traceback
import urllib.parse

from aiohttp import web
from lib.settings import Settings, LogRecord, CustomFormatter

logging.setLogRecordFactory(LogRecord)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

class Salesforce:
    access_token = None
    instance_url = None
    browser_url = ""

async def simple_get(use_url, headers={}):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(use_url) as resp:
            res = await resp.json()
            if resp.status > 299:
                logger.debug("resp:{0}".format(resp))
                logger.debug("res:{0}".format(res))
            return resp.status, res

async def simple_post(use_url, data={}):
    async with aiohttp.ClientSession() as session:
        async with session.post(use_url, json=data) as resp:
            res = await resp.json()
            if resp.status > 299:
                logger.debug(resp, res)
            return res

async def salesforce_get(url, attempts=0):
    headers = {"Accept":"application/json",
               "Authorization":"Bearer {0}".format(Salesforce.access_token)}
    status, res = await simple_get(url, headers)
    if status > 299:
        if attempts == 0:
            logger.debug('salesforce_get failed.  Generating a new token and retrying.')
            await get_salesforce_token()
            res = await salesforce_get(url, attempts+1)
        else:
            logger.debug('salesforce_get failed a second time.  Not retrying again.')
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
    logger.debug('get_salesforce_token url:{0}'.format(url))
    res = await simple_post(url)
    logger.debug('get_salesforce_token res:{0}'.format(res))
    Salesforce.access_token = res.get('access_token')
    Salesforce.instance_url = res.get('instance_url')
    Salesforce.browser_url = get_salesforce_browser_url(res.get('instance_url'))
    return res

async def salesforce_query(select_items, phone_number):
    url_path = "/services/data/v53.0/query?"
    url_template = Salesforce.instance_url + url_path + "q=SELECT+{0}+FROM+Contact+WHERE+phone='{1}'"
    url = url_template.format(select_items, phone_number)
    logger.info("Querying Salesforce for: {0}".format(url))
    data = await salesforce_get(url)
    return data

async def get_salesforce_contact(select_items, caller_id, secondary_caller_id):
    data = {}
    browser_url = ""
    if secondary_caller_id:
        data = await salesforce_query(select_items, urllib.parse.quote_plus(secondary_caller_id))
    if data == {} or len(data.get('records', [])) == 0:
        data = await salesforce_query(select_items, urllib.parse.quote_plus(caller_id))
    logger.info("Salesforce API resp:{0}".format(data))
    if len(data.get('records', [])) > 0:
        data = data['records'][0]
        data =  {k.lower(): v for k, v in data.items()}
        browser_url = Salesforce.browser_url.format(data["id"])
    return data, browser_url


async def page_handle(request):
    logger.debug('serving index.html')
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
        logger.debug("integration:{0}".format(integration))
        logger.debug("caller_id:{0}".format(caller_id))
        logger.debug("secondary_caller_id:{0}".format(secondary_caller_id))
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
    logger.info("/api response:{0}".format(response))
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
        logger.debug(integration)
        logger.debug(caller_id)
        logger.debug("secondary_caller_id:{0}".format(secondary_caller_id))
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
    logger.info("/url response:{0}".format(response))
    return web.Response(text=json.dumps(response))

async def options(request):
    """
    POST requests from the UI 
    """
    default_error_msg = "A unknown error occurred."
    response = {"mockapi":False, "salesforce":False, "developer":Settings.dev_mode}
    try:
        if Settings.sf_client_id and Settings.sf_client_secret:
            response["salesforce"] = True
        if Settings.mockapi_url:
            response["mockapi"] = True
    except Exception as e:
        response = {"error": default_error_msg}
        traceback.print_exc()
    logger.info("/options response:{0}".format(response))
    return web.Response(text=json.dumps(response))

app = web.Application()
app.add_routes([web.get('/', page_handle),
                web.post('/api', api),
                web.post('/url', url),
                web.post('/options', options),
                web.static('/static', 'static')
               ])

if __name__ == '__main__':
    if Settings.sf_client_id and Settings.sf_client_secret:
        asyncio.run(get_salesforce_token())
        logger.debug("Salesforce.access_token: {0}".format(Salesforce.access_token))
    else:
        logger.warning("No Salesforce Client App configured.  Salesforce will not be an option as a result.")
    logger.info("Running on port {0}".format(Settings.port))
    web.run_app(app, port=Settings.port)