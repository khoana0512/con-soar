"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


def on_start(container):
    phantom.debug('on_start() called')

    # call 'scan_url' block
    scan_url(container=container)

    return

def scan_url(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("scan_url() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.requestURL","artifact:*.id"])

    parameters = []

    # build parameters list for 'scan_url' call
    for container_artifact_item in container_artifact_data:
        if container_artifact_item[0] is not None:
            parameters.append({
                "url": container_artifact_item[0],
                "context": {'artifact_id': container_artifact_item[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("detonate url", parameters=parameters, name="scan_url", assets=["scan url"], callback=decision_1)

    return


def post_data_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("post_data_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    receiver = phantom.collect2(container=container, datapath=["artifact:*.cef.destinationUserName","artifact:*.id"])
    sender = phantom.collect2(container=container, datapath=["artifact:*.cef.sourceUserName","artifact:*.id"])
    url = phantom.collect2(container=container, datapath=["artifact:*.cef.requestURL","artifact:*.id"])
    body_formatted_string = phantom.format(
        container=container,
        template="""{\n  \"sender\": \"%s\",\n  \"receiver\": \"%s\",\n  \"url\": \"%s\"\n}"""%(sender[0][0],receiver[0][0],url[0][0]),
        parameters=[])
    headers_formatted_string = phantom.format(
        container=container,
        template="""{\n\"accept\": \"application/json\"\n}""",
        parameters=[])
    location_formatted_string = phantom.format(
        container=container,
        template="""/send-msteam/email-alert/fail-scan""",
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

def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["scan_url:action_result.status", "==", "success"]
        ])

    # call connected blocks if condition 1 matched
    if found_match_1:
        get_report_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    post_data_1(action=action, success=success, container=container, results=results, handle=handle)

    return


def get_report_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_report_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    scan_url_result_data = phantom.collect2(container=container, datapath=["scan_url:action_result.data.*.scan_id","scan_url:action_result.parameter.context.artifact_id"], action_results=results)

    parameters = []

    # build parameters list for 'get_report_1' call
    for scan_url_result_item in scan_url_result_data:
        if scan_url_result_item[0] is not None:
            parameters.append({
                "report_type": "url",
                "scan_id": scan_url_result_item[0],
                "context": {'artifact_id': scan_url_result_item[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get report", parameters=parameters, name="get_report_1", assets=["scan url"], callback=post_data_2)

    return


def post_data_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("post_data_2() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    body_formatted_string = phantom.format(
        container=container,
        template="""{\n  \"scanId\": \"string\",\n  \"sender\": \"string\",\n  \"receiver\": \"string\",\n  \"url\": \"string\",\n  \"totalScan\": 0,\n  \"positive\": 0\n}""",
        parameters=[])
    headers_formatted_string = phantom.format(
        container=container,
        template="""{\n\"accept\": \"application/json\"\n}""",
        parameters=[])
    location_formatted_string = phantom.format(
        container=container,
        template="""/send-msteam/email-alert/success-scan""",
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