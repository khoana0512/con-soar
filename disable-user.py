"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


def on_start(container):
    phantom.debug('on_start() called')

    # call 'call_api_send_message_msteams' block
    call_api_send_message_msteams(container=container)
    # call 'auto_disable_user' block
    auto_disable_user(container=container)

    return

def call_api_send_message_msteams(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("call_api_send_message_msteams() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    headers_formatted_string = phantom.format(
        container=container,
        template="""{\n\"accept\": \"application/json\"\n}""",
        parameters=[])
    location_formatted_string = phantom.format(
        container=container,
        template="""/send-msteam/alert/{0}/{1}""",
        parameters=[
            "artifact:*.cef.ad_host",
            "artifact:*.cef.destinationUserName"
        ])

    parameters = []

    if location_formatted_string is not None:
        parameters.append({
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

    phantom.act("get data", parameters=parameters, name="call_api_send_message_msteams", assets=["notification-api"])

    return


def auto_disable_user(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("auto_disable_user() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    headers_formatted_string = phantom.format(
        container=container,
        template="""{\n\"accept\": \"application/json\"\n}""",
        parameters=[])
    location_formatted_string = phantom.format(
        container=container,
        template="""/auto-disable/{0}/{1}""",
        parameters=[
            "artifact:*.cef.ad_host",
            "artifact:*.cef.destinationUserName"
        ])

    parameters = []

    if location_formatted_string is not None:
        parameters.append({
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

    phantom.act("get data", parameters=parameters, name="auto_disable_user", assets=["notification-api"])

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