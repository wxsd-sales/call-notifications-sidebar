# Call Notifications Sidebar
  
Embedded Sidebar application that reacts to inbound calls on Webex Calling.  Perhaps the signed in Webex User is an Agent receiving calls from customers.  This app can do data dips into MockAPI or Salesforce, to look up information about the customer based on the customer's caller ID, and display the customer information to the Agent.

[![Vidcast Overview](https://github.com/wxsd-sales/custom-pmr-pin/assets/19175490/4861e7cd-7478-49cf-bada-223b30810691)](https://app.vidcast.io/share/3f264756-563a-4294-82f7-193643932fb3)


## Overview

The PSTN Flow:
- Caller dials a PSTN number that routes to a Webex Agent (Call Queue).
- The Sidebar App passes the information to its webserver, which does an API call to MockAPI or Salesforce in an effort to match the inbound callerID.
- The Sidebar App displays additional information to the Agent about the caller, if the API request was successful.


### Flow Diagram
![PSTN Flow](https://github.com/wxsd-sales/custom-pmr-pin/assets/19175490/bb4d0ed9-7d57-4306-ae99-74d37337a562)


## Setup

### Prerequisites & Dependencies:

- Developed on MacOS Ventura (13.2.1) & Ubuntu 22.04
- Developed on Python 3.8.1 & 3.8.3
-   Other OS and Python versions may work but have not been tested
- MockAPI (optional)
- Salesforce (optional)
- Webex Calling
- [Sidebar App](https://developer.webex.com/docs/embedded-apps-framework-sidebar-api-quick-start)

<!-- GETTING STARTED -->

### Installation Steps:
1. 
```
pip3 install aiohttp
pip3 install python-dotenv
```
2.  Clone this repo, and create a file named ```.env``` in the repo's root directory.
3.  Populate the following environment variables to the .env file:
```
MY_APP_PORT=10031

MY_SALESFORCE_CLIENT_ID=""
MY_SALESFORCE_CLIENT_SECRET=""
MY_SALESFORCE_USERNAME=""
MY_SALESFORCE_PASSWORD=""

MY_MOCKAPI_URL=""
```
Note: the MockAPI and Salesforce variables should be removed, or the quotes left empty, if you are not using mockapi or salesforce respectively.  
4. Run
```python3 server.py```

### Sidebar App Setup
1. Create a new app while signed in [here](https://developer.webex.com/my-apps), and choose Embedded App.  
2. Select Sidebar and give it a name. You will need to request admin approval once created.  

3. Supply the domain and URL of the publicly accessible webserver where you plan to deploy this.

    
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
