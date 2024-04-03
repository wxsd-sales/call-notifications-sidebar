const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const title = urlParams.get('title');
const titleTextColor = urlParams.get('title-text-color');
const titleBGColor = urlParams.get('title-bg-color');
const background = urlParams.get('background');
const logo = urlParams.get('logo');

var integrationNameHash = {'mockapi': "MockAPI", "salesforce": "Salesforce", "hubspot": "Hubspot"};
var embedded_app;

function getActiveIntegration(){
    activeLis = $('#integration-tab li.is-active');
    if(activeLis.length > 0){
        return activeLis[0].id;
    } else {
        return undefined;
    }
}

function updateMainMessage(integration, callAction){
    let integrationName = integrationNameHash[integration];
    console.log(integrationName);
    let msg = "When you receive an incoming call, ";
    if(integrationName){
        if(callAction == "call-action-api"){
            msg += `an API request will be made to ${integrationName} to retrieve information about the caller.`
        } else if(callAction == "call-action-spop"){
            msg += `a new ${integrationName} window will be opened that shows information about the caller.`
        } else if(callAction == "call-action-both"){
            msg += `a new ${integrationName} window will be opened and an API request will be made to retrieve information about the caller.`
        }
    } else {
        msg += "information about the caller will be displayed below."
    }
    
    $('#call-behavior-message').text(msg);
}

$('#settings').on('click', function(e){
    if($('#configuration').is(":visible")){
        $('#configuration').hide();
    } else {
        $('#configuration').show();
    }
})

$('#integration-tab').on('click', function(e){
    let name = e.target.name;
    console.log(name);
    $('#integration-tab li.is-active').removeClass('is-active');
    $(`#${name}`).addClass('is-active');
    updateMainMessage(name, $('#call-action-tab li.is-active')[0].id);
})

$('#call-action-tab').on('click', function(e){
    let name = $(e.target).attr('name');
    console.log(name);
    $('#call-action-tab li.is-active').removeClass('is-active');
    $(`#${name}`).addClass('is-active');
    updateMainMessage(getActiveIntegration(), $('#call-action-tab li.is-active')[0].id);
})

$('#api-link').on('click', function(e){
    window.open($('#api-link-text').attr('href'));
})

$('#caller-info-button').on('click', function(e){
    if($('#call-behavior-message').is(":visible")){
        $('#call-behavior-message').hide();
    } else {
        $('#call-behavior-message').show();
    }
})

$('#dev-details-button').on('click', function(e){
    if($('#user-info-div').is(":visible")){
        $('#user-info-div').hide();
    } else {
        console.log(embedded_app.about);
        console.log(embedded_app.language);
        console.log(embedded_app.application.states.user);
        $('#user-info-div').show();
    }
})

function clearCallerInfo(){
    $('#caller-message').empty();
    $('#caller-info').hide();
}

$('#delete-api-info').on('click', function(e){
    $('#api-info-div').hide();
})

$('#delete-caller-info').on('click', function(e){
    clearCallerInfo();
})


function handleBadge(embedded_app, callCount) {
    embedded_app.context.getSidebar().then((s) => {
        sidebar = s;
        console.log("Show a badge on the sidebar...");
        // Make sure the sidebar is available..
        if (!sidebar) {
            console.log("Sidebar info is not available. Error: ", webex.Application.ErrorCodes[4]);
            return;
        }
        // Initialize a badge object...
        const badge = {
            badgeType: 'count',
            count: callCount,
        };
        console.log(`sidebar badge: ${JSON.stringify(badge)}`);
        // Show the badge...
        sidebar.showBadge(badge).then((success) => {
            console.log("sidebar.showBadge() successful.", success);
        }).catch((error) => {
            console.log("sidebar.showBadge() failed. Error: ", webex.Application.ErrorCodes[error]);
        });
    }).catch((error) => {
        console.log("getSidebar() failed. Error: ", webex.Application.ErrorCodes[error]);
    });
}


async function handleCallStateChange(embedded_app, call) {
    $('#call-state').text(call.state);
    if(call.state == "Started") {
        console.log("A call has come in...");
        //console.log(embedded_app);
        if(embedded_app.application.states.viewState != "IN_FOCUS"){
            handleBadge(embedded_app, call.remoteParticipants.length);
        }
        // For all calls, log the information...
        console.log(call);
        let callerId;
        let callerName;
        if(call.remoteParticipants.length > 0){
            callerId = call.remoteParticipants[0].callerID;
            callerName = call.remoteParticipants[0].name;
            //$('#caller-id').text(callerId.substring(0,6) + "XXXX");
            $('#caller-id').text(callerId);
        }
        console.log(`call.id:${call.id}`)
        if(!callerId && callerName){
            console.log(`No callerId (${callerId}), but callerName was found, assigning callerName value (${callerName}) to callerId.`)
            callerId = callerName;
        }
        //$('#caller-json').text(JSON.stringify(call.localParticipant));
        $('#call-id').text(call.id);
        $('#call-type').text(call.callType);
        console.log(`call.type:${call.callType}`)
        let callAction = $('#call-action-tab li.is-active')[0].id;
        let integration = getActiveIntegration();
        console.log(`callAction: ${callAction}`);

        $('#caller-info').show();

        if(integration){
            if(callAction == "call-action-api" || callAction == "call-action-both"){
                if(callerId){
                    $.post("/api", JSON.stringify({"integration":integration, "caller_id":callerId, "secondary_caller_id":callerName}), function(result){
                        let resp = JSON.parse(result);
                        console.log(resp);
                        let data = resp.data;

                        if(data.name){
                            $('#api-name-text').text(data.name);
                        } else {
                            $('#api-name-text').text("?");
                        }

                        if(data.address){
                            $('#api-address').show();
                            $('#api-address-text').text(data.address);
                        } else {
                            $('#api-address').hide();
                            $('#api-address-text').text("?");
                        }

                        if(data.email){
                            $('#api-email').show();
                            $('#api-email-text').text(data.email);
                        } else {
                            $('#api-email').hide();
                            $('#api-email-text').text("?");
                        }

                        if(data.dob){
                            $('#api-dob').show();
                            $('#api-dob-text').text(data.dob);
                        } else {
                            $('#api-dob').hide();
                            $('#api-dob-text').text("?");
                        }

                        if(data.primaryPhys){
                            $('#api-primary-phys').show();
                            $('#api-primary-phys-text').text(data.primaryPhys);
                        } else {
                            $('#api-primary-phys').hide();
                            $('#api-primary-phys-text').text("?");
                        }

                        if(data.hospital){
                            $('#api-hospital').show();
                            $('#api-hospital-text').text(data.hospital);
                        } else {
                            $('#api-hospital').hide();
                            $('#api-hospital-text').text("?");
                        }

                        if(resp.url){
                            $('#api-link-text').attr('href', resp.url);
                            $('#api-link-text').text(`View ${integrationNameHash[integration]} Page`);
                            $('#api-link').show();
                        } else {
                            $('#api-link').hide();
                        }

                        if(resp.error){
                            console.log(`/api response ERROR: ${resp.error}`);
                        } else {
                            $('#api-title').text( integrationNameHash[integration] + " Information");
                            $('#api-info-div').show();

                            if(callAction == "call-action-both"){
                                if(resp.url){
                                    window.open(resp.url);
                                } else {
                                    console.log("NO WINDOW URL!")
                                }
                            }
                        }
                    });
                }
            } else {
                $('#api-info-div').hide();
            }

            if(callAction == "call-action-spop"){
                if(callerId){
                    $.post("/url", JSON.stringify({"integration":integration, "caller_id":callerId}), function(result){
                        let resp = JSON.parse(result);
                        console.log(resp);
                        if(resp.url){
                            window.open(resp.url);
                        } else {
                            console.log("NO WINDOW URL!")
                        }

                        if(resp.error){
                            console.log(`/url response ERROR: ${resp.error}`);
                        }
                    });
                }
            }
        }
    } else if(call.state == "Connected"){
        console.log("Call is connected.");
    } else if(call.state == "Ended"){
        console.log("Call is ended.");
    } else {
        console.log("Other call.state:" + call.state);
    }
}


window.addEventListener('load', function () {
    updateMainMessage(getActiveIntegration(), $('#call-action-tab li.is-active')[0].id);
    console.log("Hello, app.");

    $.post("/options", function(result){
        let resp = JSON.parse(result);
        console.log(resp);
        if(!resp.mockapi){
            $('#mockapi').removeClass('is-active');
            $('#salesforce').addClass('is-active');
        } else {
            $('#mockapi').show();
        }
        if(!resp.salesforce){
            $('#salesforce').removeClass('is-active');
        } else {
            $('#salesforce').show();
        }
        if(!resp.hubspot){
            $('#hubspot').removeClass('is-active');
        } else {
            $('#hubspot').show();
        }

        console.log(resp.developer);
        if(resp.developer){
            $('#dev-details-button-div').show();
        }

        if(resp.error){
            console.log(`/url response ERROR: ${resp.error}`);
        }
        let activeIntegration = getActiveIntegration();
        if(activeIntegration){
            $('#call-action-tab').show();
        }
        updateMainMessage(activeIntegration, $('#call-action-tab li.is-active')[0].id);
    });
    $('body').css({'background-image':`url(${background})`});
    if(logo){
        $('#logo').attr('src', logo);
    }
    if(title){
        $('#main-title').text(title);
    }
    if(titleTextColor){
        $('#main-title').css({"color":`#${titleTextColor}`});
    }
    if(titleBGColor){
        $('#header-box').removeClass("is-info");
        $('#header-box').removeClass("has-background-info");
        $('#header-box').css({"background-color":`#${titleBGColor}`});
    }
    
    //console.log(window.webex);
    embedded_app = new window.webex.Application({logs: { logLevel: 1 }});
    embedded_app.onReady().then(() => {
        console.log("onReady()", { message: "EA is ready." });
        console.log(embedded_app.application.states.user);
        console.log(embedded_app.application.states.user.token);
        embedded_app.listen().then(() => {
            embedded_app.on("sidebar:callStateChanged", (call) => {
                console.log("Call state changed. New call object:", call);
                handleCallStateChange(embedded_app, call);
            });

            embedded_app.on("application:viewStateChanged", (viewState) => {
                console.log("View state changed. Current view:", viewState);
                switch (viewState) {
                    case "IN_FOCUS":
                        // User has noticed the badge and has responded, so we can remove it...
                        handleBadge(embedded_app, 0);
                        break;
                }
            });
        });
    });
});