# Call Notifications Sidebar
  
Embedded Sidebar application that reacts to inbound calls on Webex Calling.  Perhaps the signed in Webex User is an Agent receiving calls from customers.  This app can do data dips into MockAPI, Salesforce, or Hubspot, to look up information about the customer based on the customer's caller ID, and display the customer information to the Agent.

[![Vidcast Overview](https://github-production-user-asset-6210df.s3.amazonaws.com/19175490/249649420-980de741-1a2c-4aea-883e-4da629bc8701.png)](https://app.vidcast.io/share/677cc9bc-b0bb-4419-9338-5f4bbe0100a3)

## Overview

The PSTN Flow:
- Caller dials a PSTN number that routes to a Webex Agent (Call Queue).
- The Sidebar App passes the information to its webserver, which does an API call to MockAPI, Salesforce, or Hubspot in an effort to match the inbound callerID.
- The Sidebar App displays additional information to the Agent about the caller, if the API request was successful.


## Setup

### Prerequisites & Dependencies:

- Developed on MacOS Ventura (13.2.1) & Ubuntu 22.04
- Developed on Python 3.8.1 & 3.8.3
    - Other OS and Python versions may work but have not been tested
- [MockAPI](mockapi.io) (optional)
- Salesforce (optional)
- Hubspot (optional)
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

HUBSPOT_ACCESS_TOKEN=""
HUBSPOT_ORG_ID=""
```
Note: the MockAPI, Salesforce, or Hubspot variables should be removed, or the quotes left empty, if you are not using them.  
4. Run
```python3 server.py```

### Sidebar App Setup
1. Create a new app while signed in [here](https://developer.webex.com/my-apps), and choose Embedded App.  
2. Select Sidebar and give it a name. You will need to request admin approval once created.  
![Screenshot 2023-06-28 at 12 43 25 PM](https://github.com/wxsd-sales/call-notifications-sidebar/assets/19175490/70491bae-260b-47dc-a882-9eb80ffe55ae)

4. Supply the domain and URL of the publicly accessible webserver where you plan to deploy this.  
![Screenshot 2023-06-28 at 12 43 11 PM](https://github.com/wxsd-sales/call-notifications-sidebar/assets/19175490/9b308946-8a21-482a-a1a8-7b6e0dd03126)

### MockAPI Setup
1. Navigate to [mockapi.io](https://mockapi.io) and either create a new project, or add a resource to an existing project.
2. The project can have any name, but take note of what you name the resource added - in my example it is called **SideBarContacts**  
![Screenshot 2023-06-28 at 1 12 53 PM](https://github.com/wxsd-sales/call-notifications-sidebar/assets/19175490/68f5b944-d5f5-47d6-9ad9-6b6ed75f67ce)  
3. It is recommended to populate the DB with MockAPI's fake data generator, but you will need to replace at least one entry with a real number you expect to receive as an agent while testing.  
4. The phone numbers must not include any dashes (MockAPI will add dashes by default, but since these are fake numbers, they won't match regardless until you add some real ones).  
![Screenshot 2023-06-28 at 1 02 52 PM](https://github.com/wxsd-sales/call-notifications-sidebar/assets/19175490/5ca7628b-db41-4266-b843-f9ed6984e6cf)  
5. Your data should then look something like this:  
![Screenshot 2023-06-28 at 1 00 07 PM](https://github.com/wxsd-sales/call-notifications-sidebar/assets/19175490/02e7b3bf-9191-4fa0-b9b6-3df96cfe8be0)  
6. Your ```MY_MOCKAPI_URL``` in your .env file should then look like this: ```MY_MOCKAPI_URL="https://1234abcd.mockapi.io/SideBarContacts?number="```, where **1234abcd** is replaced with the unique alphanumeric value your project shows.  If you named your resource something other than **SideBarContacts**, replace that in the URL as well.

    
## Live Demo

<!-- Update your vidcast link -->
Check out our Vidcast recording, [here](https://app.vidcast.io/share/677cc9bc-b0bb-4419-9338-5f4bbe0100a3)!

<!-- Keep the following statement -->
*For more demos & PoCs like this, check out our [Webex Labs site](https://collabtoolbox.cisco.com/webex-labs).

## License

All contents are licensed under the MIT license. Please see [license](LICENSE) for details.

## Disclaimer

<!-- Keep the following here -->  
Everything included is for demo and Proof of Concept purposes only. Use of the site is solely at your own risk. This site may contain links to third party content, which we do not warrant, endorse, or assume liability for. These demos are for Cisco Webex usecases, but are not Official Cisco Webex Branded demos.
 
 
## Support

Please contact the Webex SD team at [wxsd@external.cisco.com](mailto:wxsd@external.cisco.com?subject=CallNotificationsSidebar) for questions. Or for Cisco internal, reach out to us on Webex App via our bot globalexpert@webex.bot & choose "Engagement Type: API/SDK Proof of Concept Integration Development". 
