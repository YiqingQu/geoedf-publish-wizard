# controller.py - App logic, rcampbel@purdue.edu, Oct 2023
import logging
import os
import sys
import traceback

from nb import model, view
from nb.log import log, log_handler
from nb.utils import get_resource_list, copy_directories, send_publish_request
from nb.view import external_update_trigger

ctrl = sys.modules[__name__]


def start(debug=False):
    """Begin running the app."""
    try:
        if debug:
            log_handler.setLevel(logging.DEBUG)
            log.setLevel(logging.DEBUG)

        # Build UI & data access objects
        view.start(debug)

        # Setup callbacks NOTE uploader's callback set by view
        view.stack.observe(when_stack_changes, 'selected_index', 'change')  # Tabs
        view.back_btn.on_click(when_back)
        view.next_btn.on_click(when_next)
        view.submit_btn.on_click(when_submit)
        view.refresh_btn.on_click(when_refresh)

        log.info('App running')
    except Exception:
        log.error('start:\n' + traceback.format_exc())
        raise


def when_next(_=None):
    """React to user pressing Next button."""

    if view.stack.selected_index < len(view.steps) - 1:
        view.stack.selected_index += 1
        log.info(f"view.stack.selected_index={view.stack.selected_index}")
        # log.info("view.progress")
        # log.info(view.progress)

        # this line below is commented to avoid one error
        # view.progress.value = view.stack.selected_index
        # view.progress.description = view.steps[view.stack.selected_index]


def when_back(_=None):
    """React to user pressing Back button."""

    if view.stack.selected_index > 0:
        view.stack.selected_index -= 1
        log.info(f"view.stack.selected_index={view.stack.selected_index}")
        log.info("view.progress")
        log.info(view.progress)

        # this line below is commented to avoid one error
        # view.progress.value = view.stack.selected_index
        # view.progress.description = view.steps[view.stack.selected_index]


def when_stack_changes(change):
    """React to user selecting new tab."""
    try:
        view.adjust_progress(change['new'])
        log.info(f'when_stack_changes, publication={model.publication.__repr__()}')
        if change['new'] == 2:
            log.info('when_stack_changes, REVIEW_PUBLISH_INFO change={change}:\n')

            when_refresh_preview()

        # elif change['new'] == view.steps.index(INTEGRITY):
        #     model.set_columns({i+1:ddn.value for i, ddn in enumerate(ctrl.col_ddns)})  # +1 to skip model
        #     model.analyze()

    except Exception:
        log.error('when_stack_changes, change={change}:\n' + traceback.format_exc())
        raise


def observe_activate(activate, widgets, callback):
    """Turn on/off value callbacks for widgets in given list."""
    for widget in widgets:

        if activate:
            widget.observe(callback, 'value')
        else:
            widget.unobserve(callback, 'value')


def when_refresh_preview(_=None):
    """Populate submission preview widgets w/data."""
    log.info(f'[when_refresh_preview], publication={model.publication.__repr__()}')
    external_update_trigger()
    # view.update_publishing_screen(model.publication)
    # view.temp()


def when_submit(_=None):
    """React to user pressing Submit button."""
    log.debug('Submit!')
    # source = "/home/jovyan/test-mount/folder1"
    target = "/home/jovyan/test-mount/staging"

    # Example usage
    # sources_json = [
    #     {'name': 'yaml', 'path': '/home/jovyan/test-mount/folder1/Untitled.ipynb'},
    #     {'name': 'input_files', 'path': '/home/jovyan/test-mount/folder2/'},
    #     {'name': 'output_files', 'path': '/home/jovyan/test-mount/folder3/'}
    # ]

    target = "/staging"
    target_path, response = copy_directories(model.publication, target)
    resp = send_publish_request(model.publication, target_path)
    log.debug(f'[when_submit] resp={resp}')


def when_refresh(_=None):
    # make request to portal
    user_id = os.getenv('JUPYTERHUB_USER')
    resources = get_resource_list()
    for i, resource in resources:
        view.resource_grid.children[i].value = resource
