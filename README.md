# Custom PMR PIN
  
Application that can receive PSTN calls (Webex Connect) with custom IVR, and direct the caller to a Webex PMR (by way of Webex Calling).  

This project was developed to provide a method for PSTN callers to join PMRs using a single static DID and a static 7 digit PIN, that can be customized by each user (per PMR).

[![Vidcast Overview](https://github.com/wxsd-sales/custom-pmr-pin/assets/19175490/4861e7cd-7478-49cf-bada-223b30810691)](https://app.vidcast.io/share/3f264756-563a-4294-82f7-193643932fb3)


## Overview

The PSTN Flow:
- Caller dials a Webex Connect number which triggers a Webex Connect Flow.
- Webex Connect Flow collects DTMF input, and sends an HTTP POST with the caller number and entered digits to our server
- Webex Connect Flow patches the call to Webex Calling Queue (empty)
- Our server monitors the Webex Calling Queue using XSI
- When a call enters the Queue that matches the POST we received from the Webex Connect Flow, we transfer the call to the Webex PMR

The Server:
- Our python server.py is listening for POST requests from Webex Connect
- Our python server.py is monitoring the Webex Calling Queue
- Retrieving/Storing configuration information from/to MongoDB


### Flow Diagram
![PSTN Flow](https://github.com/wxsd-sales/custom-pmr-pin/assets/19175490/bb4d0ed9-7d57-4306-ae99-74d37337a562)


## Setup

### Prerequisites & Dependencies:

- Developed on MacOS Ventura (13.2.1) & Ubuntu 22.04
- Developed on Python 3.8.1 & 3.8.3
-   Other OS and Python versions may work but have not been tested
- Mongo DB (i.e. Atlas)
- Webex Connect
- Webex Calling
- [Webex Integration](https://developer.webex.com/docs/integrations) with the following scopes:
```
meeting:preferences_write, meeting:preferences_read, spark:people_read
```

- [Service App](https://developer.webex.com/docs/service-app) with the following scopes:
```
spark:organizations_read, spark:people_read, spark:people_write, spark-admin:licenses_read, spark-admin:people_read, spark-admin:people_write, spark-admin:xsi
```

<!-- GETTING STARTED -->

### Installation Steps:
1. 
```
pip3 install aiohttp
pip3 install python-dotenv
pip3 install wxcadm
pip3 install motor
pip3 install cachetools
```
2.  Clone this repo, and create a file named ```.env``` in the repo's root directory.
3.  Populate the following environment variables to the .env file:
```
DEBUG_MODE=False
DEV_MODE=True

#For Handling User Web Portal
MY_APP_PORT=8080
MY_WEBEX_CLIENT_ID=
MY_WEBEX_SECRET=
MY_WEBEX_REDIRECT_URI="https://<yourserver>.<domain>/oauth"
MY_WEBEX_SCOPES="spark%3Akms%20spark%3Apeople_read%20meeting%3Apreferences_write%20meeting%3Apreferences_read"

#For Handling XSI Manager
#Scopes Required: 
MY_SERVICE_APP_CLIENT_ID=
MY_SERVICE_APP_SECRET=
MY_SERVICE_APP_REFRESH_TOKEN=

MY_CALL_QUEUE_TARGET="<identifier>@<subdomain>.cisco-bcld.com"
MY_MONGO_URI="mongodb+srv://<username>:<password>@<name>.<subdomain>.mongodb.net/customPMRPIN?authSource=admin&retryWrites=true&w=majority"
MY_MONGO_DB="customPMRPIN"
```
4. Run
```python3 server.py```
    
    
## Live Demo

<!-- Update your vidcast link -->
Check out our Vidcast recording, [here](https://app.vidcast.io/share/3f264756-563a-4294-82f7-193643932fb3)!

<!-- Keep the following statement -->
*For more demos & PoCs like this, check out our [Webex Labs site](https://collabtoolbox.cisco.com/webex-labs).

## License

All contents are licensed under the MIT license. Please see [license](LICENSE) for details.

## Disclaimer

<!-- Keep the following here -->  
Everything included is for demo and Proof of Concept purposes only. Use of the site is solely at your own risk. This site may contain links to third party content, which we do not warrant, endorse, or assume liability for. These demos are for Cisco Webex usecases, but are not Official Cisco Webex Branded demos.
 
 
## Support

Please contact the Webex SD team at [wxsd@external.cisco.com](mailto:wxsd@external.cisco.com?subject=CustomPMRPIN) for questions. Or for Cisco internal, reach out to us on Webex App via our bot globalexpert@webex.bot & choose "Engagement Type: API/SDK Proof of Concept Integration Development". 
