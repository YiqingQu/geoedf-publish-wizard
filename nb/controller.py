# controller.py - App logic, rcampbel@purdue.edu, Oct 2023
import logging
import os
import sys
import traceback

from fuzzywuzzy import fuzz, process

from nb import model, view
from nb.config import cfg, HDR, NUM_PREVIEW_ROWS, COL_DDN_WIDTH
from nb.log import log, log_handler
from nb.utils import get_resource_list, copy_directories, send_publish_request

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
        log.error('start:\n'+traceback.format_exc())
        raise


def when_next(_=None):
    """React to user pressing Next button."""

    if view.stack.selected_index < len(view.steps)-1:
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
            # if change['new'] == view.steps.index(VIEW_PUBLISH_STATUS):
            #
            #     when_refresh_preview()

            # elif change['new'] == view.steps.index(INTEGRITY):
            #     model.set_columns({i+1:ddn.value for i, ddn in enumerate(ctrl.col_ddns)})  # +1 to skip model
            #     model.analyze()

    except Exception:
        log.error('when_stack_changes, change={change}:\n'+traceback.format_exc())
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

    # Clear sample view widgets
    for i in range(NUM_PREVIEW_ROWS*len(HDR)):
        
        if i < len(HDR):
            view.out_grid.children[i].value = HDR[i]  
            view.out_grid.children[i].style.font_weight = 'bold'
        else:
            view.out_grid.children[i].value = ' '  

    if model.df is not None:

        # Data rows
        for r in range(1, NUM_PREVIEW_ROWS):  # 1 to skip header
            view.out_grid.children[r*len(HDR)+0].value = str(view.model_ddn.value)  # Model

            for c in range(len(HDR[1:])):  # +1 to skip model  
                view.out_grid.children[r*len(HDR)+c+1].value = str(model.df.iloc[r, c+1])  


def when_submit(_=None):
    """React to user pressing Submit button."""
    log.debug('Submit!')
    # source = "/home/jovyan/test-mount/folder1"
    target = "/home/jovyan/test-mount/staging"

    # Example usage
    sources_json = [
        {'name': 'yaml', 'path': '/home/jovyan/test-mount/folder1/Untitled.ipynb'},
        {'name': 'input_files', 'path': '/home/jovyan/test-mount/folder2/'},
        {'name': 'output_files', 'path': '/home/jovyan/test-mount/folder3/'}
    ]
    publication_type = ""

    target = "/staging"
    target_path, response = copy_directories(sources_json, target)
    send_publish_request(publication_type, target_path)
    # log.debug(f'[when_submit] resp={resp}')


def when_refresh(_=None):
    # make request to portal
    user_id = os.getenv('JUPYTERHUB_USER')
    resources = get_resource_list()
    for i, resource in resources:
        view.resource_grid.children[i].value = resource

