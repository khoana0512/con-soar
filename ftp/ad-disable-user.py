"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


def on_start(container):
    phantom.debug('on_start() called')

    # call 'disable_account_1' block
    disable_account_1(container=container)

    return

def post_data_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("post_data_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    container_artifact_data_userName = phantom.collect2(container=container, datapath=["artifact:*.cef.destinationUserName","artifact:*.id"])
    container_artifact_data_host = phantom.collect2(container=container, datapath=["artifact:*.cef.deviceCustomString1","artifact:*.id"])
    
    body_formatted_string = phantom.format(
        container=container,
        template="""{\n  \"user\": \"%s\",\n  \"host\": \"%s\",\n  \"status\": 0,\n  \"description\": \"string\"\n}"""%(container_artifact_data_userName[0][0],container_artifact_data_host[0][0]),
        parameters=[])
    headers_formatted_string = phantom.format(
        container=container,
        template="""{\n\"Content-Type\": \"application/json\",\n\"accept\":\"application/json\"\n}""",
        parameters=[])
    location_formatted_string = phantom.format(
        container=container,
        template="""/alert""",
        parameters=[])

    parameters = []

    if body_formatted_string is not None and location_formatted_string is not None:
        parameters.append({
            "body": body_formatted_string,
            "headers": headers_formatted_string,
            "location": location_formatted_string,
            "verify_certificate": False,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("post data", parameters=parameters, name="post_data_1", assets=["notification-api"])

    return

def disable_account_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("disable_account_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.destinationUserName","artifact:*.id"])

    parameters = []

    # build parameters list for 'disable_account_1' call
    for container_artifact_item in container_artifact_data:
        if container_artifact_item[0] is not None:
            parameters.append({
                "user": container_artifact_item[0],
                "use_samaccountname": True,
                "context": {'artifact_id': container_artifact_item[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("disable account", parameters=parameters, name="disable_account_1", assets=["adldap-defenders"], callback=decision_1)

    return


def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["disable_account_1:action_result.status", "==", False]
        ])

    # call connected blocks if condition 1 matched
    if found_match_1:
        post_data_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    post_data_2(action=action, success=success, container=container, results=results, handle=handle)

    return


def post_data_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("post_data_2() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    container_artifact_data_userName = phantom.collect2(container=container, datapath=["artifact:*.cef.destinationUserName","artifact:*.id"])
    container_artifact_data_host = phantom.collect2(container=container, datapath=["artifact:*.cef.deviceCustomString1","artifact:*.id"])
    body_formatted_string = phantom.format(
        container=container,
        template="""{\n  \"user\": \"False\",\n  \"host\": \"%s\",\n  \"status\": 0,\n  \"description\": \"string\"\n}"""%(container_artifact_data_host[0][0]),
        parameters=[])
    headers_formatted_string = phantom.format(
        container=container,
        template="""{\n\"Content-Type\": \"application/json\",\n\"accept\":\"application/json\"\n}""",
        parameters=[])
    location_formatted_string = phantom.format(
        container=container,
        template="""/alert""",
        parameters=[])

    parameters = []

    if body_formatted_string is not None and location_formatted_string is not None:
        parameters.append({
            "body": body_formatted_string,
            "headers": headers_formatted_string,
            "location": location_formatted_string,
            "verify_certificate": False,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("post data", parameters=parameters, name="post_data_2", assets=["notification-api"])

    return

def on_finish(container, summary):
    phantom.debug("on_finish() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # This function is called after all actions are completed.
    # summary of all the action and/or all details of actions
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    ################################################################################
    ## Custom Code End
    ################################################################################

    return