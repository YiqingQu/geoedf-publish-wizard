import os
import sys

from IPython.display import display
from ipyfilechooser import FileChooser
from ipywidgets import Accordion, Dropdown, HBox, Label, \
    Layout, HTML, Text, VBox, Button, Stack, Textarea, Checkbox, RadioButtons, \
    widgets

from nb.config import SELECT_FILES, EXTRACT_METADATA, \
    REVIEW_PUBLISH_INFO, PUBLISH, TAB_TITLES, \
    TASK_LIST_TITLE, APP_TITLE, PUBLICATION_TYPE_GEOSPATIAL, PUBLICATION_TYPE_WORKFLOW, PUBLICATION_TYPE_OTHER, \
    FILE_TYPE_YAML, FILE_TYPE_INPUT, FILE_TYPE_OUTPUT, FILE_TYPE_GEOSPATIAL
from nb.log import log, log_handler
from nb.utils import get_resource_list

view = sys.modules[__name__]


def new_section(title, contents):
    '''Utility method that create a collapsible widget container'''

    if type(contents) == str:
        contents = [widgets.HTML(value=contents)]
    if type(contents) == VBox:
        contents = [contents]

    ret = widgets.Accordion(children=tuple([widgets.VBox(contents)]), layout=Layout(width='100%'))
    ret.set_title(0, title)
    ret.selected_index = 0
    return ret


def start(show_log, ):
    """Build the user interface."""
    display(HTML(filename='nb/custom.html'))  # Send CSS code down to browser    
    app_title = HTML(
        f'<h2 style="margin-bottom: 5px; font-weight: bold; text-align: center;">{APP_TITLE}</h2>')
    # app_title.add_class('app_title')

    # with open('nb/logo.png', "rb") as logo_file:
    #     logo = Image(value=logo_file.read(), format='png', layout={'max_height': '32px'})

    # Create tabs and fill with UI content (widgets)

    tabs = widgets.Tab()

    # Build conent (widgets) for each tab
    tab_content = []
    tab_content.append(view.build_publish_tab())
    tab_content.append(view.build_publish_status_tab())

    tabs.children = tuple(tab_content)  # Fill tabs with content

    # Add title text for each tab
    for i, tab_title in enumerate(TAB_TITLES):
        tabs.set_title(i, tab_title)

    header = widgets.HBox([app_title, ])  # todo add logo here
    header.layout.justify_content = 'space-between'  # Example of custom widget layout
    display(widgets.VBox([header, tabs]))
    log.info('UI build completed')

    if show_log:  # Duplicate log lines in log widget (will always show in Jupyter Lab log)
        display(log_handler.log_output_widget)


def build_publish_tab():
    '''Create widgets for introductory tab content'''
    # view.steps = ["first", UPLOAD, SUBMISSION, INTEGRITY, PLAUSIBILITY, FINISH]
    view.steps = [SELECT_FILES, EXTRACT_METADATA, REVIEW_PUBLISH_INFO]

    # Create stack - NOTE Maintain corresponding order of IDs & children!
    view.stack = Stack([
        select_files_screen(),
        extract_metadata_screen(),
        review_publish_info_screen(),
    ], selected_index=0)

    view.back_btn = Button(description='Back', layout=Layout(margin='15px'))
    view.next_btn = Button(description='Next', layout=Layout(margin='15px'))
    # if view.stack.selected_index == 0:
    #     view.back_btn.disabled = True
    #     # view.back_btn = Label(layout=Layout(width='90px'))
    # if view.stack.selected_index == len(view.steps)-1:
    #     view.next_btn.disabled = True
    #     # view.next_btn = Label(layout=Layout(width='90px'))

    view.progress = [HTML(text, layout=Layout(width='auto', margin='15px')) for text in view.steps]
    view.adjust_progress(0)

    # NOTE Header & footer use blank labels as spacers
    # header = standard(HBox([app_title, Label(layout=Layout(width='700px')), ]))  # add logo here
    footer = standard(HBox([view.back_btn, Label(layout=Layout(width='645px')), view.next_btn]))

    return VBox([HBox(view.progress), view.stack, footer])  # Show app


def build_publish_status_tab():
    content = []
    view.refresh_btn = Button(description='Refresh')
    # content.append(view.refresh_btn)

    user_id = os.getenv('JUPYTERHUB_USER')  # id is the same as username
    resources = get_resource_list()
    labels = [Label(layout=Layout(border='1px solid lightgray', padding='0px', margin='0px')) for _ in range(2)]

    header = [
        HTML('<strong>Resource Name</strong>'),
        HTML('<strong>Status</strong>'),
    ]

    # Create a list of widgets for each row in the grid
    rows = []
    for resource in resources:
        name_widget = widgets.Label(resource['title'])
        status_widget = widgets.Label(resource['status'])
        rows.append(name_widget)
        rows.append(status_widget)

    # Combine the header and rows
    grid_items = header + rows

    # Calculate the number of columns (fixed at 2 for 'Resource Name' and 'Status')
    num_columns = 2

    # Create the GridBox with the specified children and layout
    grid = widgets.GridBox(grid_items, layout=widgets.Layout(grid_template_columns="repeat(2, auto)"))

    # view.out_grid = GridBox(children=labels, layout=Layout(grid_template_columns=f'repeat({len(HDR)}, 1fr)', grid_gap='0px'))

    # todo display resources
    content.append(section(TASK_LIST_TITLE, [grid, view.refresh_btn]))
    # content.append(section(TASK_LIST_TITLE, [HTML(value=TASK_LIST_TEXT), view.refresh_btn]))

    task_id_entry_area = Text(description='Task ID:')
    submit_btn = Button(description='Submit')
    track_content = VBox([task_id_entry_area, submit_btn])

    # content.append(view.new_section(TRACK_TITLE, track_content))
    return widgets.VBox(content)


def section(title, contents, desc=None):
    '''Create collapsible container with title, optional desc.'''
    if desc is not None:
        contents = [HTML(value=desc)] + contents

    ret = Accordion(children=tuple([VBox(contents)]),
                    layout=Layout(width='1000px'))  # TODO , layout=Layout(width='1000px')
    ret.set_title(0, title)
    ret.selected_index = 0
    return standard(ret)


def standard(widget):
    widget.layout.min_width = '1000px'
    return widget


def set_width(widgets, width='auto', desc=False):
    """Set width for widgets' layouts or descriptions."""
    for widget in widgets:

        if desc:
            widget.style.description_width = width
        else:
            widget.layout = Layout(width=width)


def select_files_screen():
    """Code for 'Select Files' screen"""
    sources_json = []

    def update_sources_json(chooser):
        # Clear previous selections to avoid duplications
        log.debug(f"Before Updated sources_json:{sources_json}")  # For demonstration

        # Update sources_json with selected file paths
        selected_files = chooser.selected
        if selected_files:
            # todo multiple selection
            if isinstance(selected_files, list):
                for file_path in selected_files:
                    sources_json.append({"name": chooser.title, "path": file_path, "filename": os.path.basename(file_path)})
            else:  # Single file selected
                sources_json.append({"name": chooser.title, "path": selected_files, "filename": os.path.basename(selected_files),})
        log.debug(f"Updated sources_json:{sources_json}")  # For demonstration

    file_type_btn = RadioButtons(description='File Type:',
                                 options=[PUBLICATION_TYPE_GEOSPATIAL, PUBLICATION_TYPE_WORKFLOW,
                                          PUBLICATION_TYPE_OTHER])

    base_dir = '/Users/'  # todo change this
    # todo use map to display UI texts different from field name

    chooser_map = {}
    # chooser_map[PUBLICATION_TYPE_GEOSPATIAL] = geospatial_chooser
    geospatial_chooser = FileChooser(base_dir, title=FILE_TYPE_GEOSPATIAL, filter_pattern='*', use_dir_icons=True,
                                     allow_multiple=True)
    workflow_chooser = FileChooser(base_dir, title=FILE_TYPE_YAML, filter_pattern='*.yml', use_dir_icons=True,
                                   allow_multiple=False)
    input_chooser = FileChooser(base_dir, title=FILE_TYPE_INPUT, filter_pattern='*',
                                use_dir_icons=True, allow_multiple=True)
    other_files_chooser = FileChooser(base_dir, title=FILE_TYPE_OUTPUT, filter_pattern='*', use_dir_icons=True,
                                      allow_multiple=True)
    output_folder_chooser = FileChooser(base_dir, title=PUBLICATION_TYPE_OTHER, use_dir_icons=True,
                                        show_only_dirs=True)

    for chooser in [geospatial_chooser, workflow_chooser, input_chooser, other_files_chooser, output_folder_chooser]:
        chooser.register_callback(update_sources_json)

    # Display based on selection
    def on_file_type_change(change):
        if change['new'] == PUBLICATION_TYPE_GEOSPATIAL:
            uploader_box.children = [geospatial_chooser]
        elif change['new'] == PUBLICATION_TYPE_WORKFLOW:
            uploader_box.children = [workflow_chooser, input_chooser, output_folder_chooser]
        else:  # Other Files
            uploader_box.children = [other_files_chooser]

    file_type_btn.observe(on_file_type_change, names='value')
    uploader_box = VBox([])
    on_file_type_change({'new': file_type_btn.value})  # Initialize with the default selection

    content = [file_type_btn, uploader_box, ]
    # content.append(view.new_section(CRITERIA_TITLE, section_list))
    return VBox([section("File(s) selection", content)])


def extract_metadata_screen():
    # Code for 'Extract Metadata' screen
    # This can be derived from the old 'submission_screen'
    import os
    username = os.getenv('JUPYTERHUB_USER')
    title_entry_area = Text(description='Title:')
    metadata_entry_area = Textarea(description='Description:', layout=Layout(width='90%', height='100px'))

    # Obtain username from Jupyter environment or allow manual entry
    # username_text = VBox([Label(value='Creator:'), Label(value=username)])
    username_text = Text(description='Creator:',
                         value=username, disabled=True)
    keyword_area = Textarea(description='Keyword:', layout=Layout(width='90%', height='50px'))

    content = [title_entry_area, username_text, metadata_entry_area, keyword_area]
    return VBox([section("Metadata", content)])


file_info = {
    'Geospatial Files': ['map1.nc', 'map2.nc'],
    # 'Workflow': ['process.yml'],
    # 'Other Files': ['additional_doc.pdf']
}

metadata_info = {
    'Title': 'Resource title',
    'Creator': 'Username',
    'Description': 'A short description of the resource.',
    'Keywords': 'geospatial, temperature'
}


def review_publish_info_screen():
    """
    Creates a screen for reviewing publishing information with two sections:
    - File Metadata
    - Publishing Information
    """

    # Construct HTML formatted summary for File Metadata
    file_metadata_html = "<h4>Selected Files:</h4><ul>"
    for file_type, files in file_info.items():
        files_list = ''.join([f"<li>{file}</li>" for file in files])
        file_metadata_html += f"<li><b>{file_type}:</b><ul>{files_list}</ul></li>"
    file_metadata_html += "</ul>"
    file_metadata_section = section("Resource Summary", [HTML(value=file_metadata_html)])

    # Construct HTML formatted summary for Publishing Information
    publishing_info_html = "<ul>"
    metadata_info['Creator'] = os.getenv('JUPYTERHUB_USER')
    for key, value in metadata_info.items():
        publishing_info_html += f"<li><b>{key}:</b> {value}</li>"
    publishing_info_html += "</ul>"
    publishing_info_section = section("Metadata", [HTML(value=publishing_info_html)])

    confirmation_checkbox = Checkbox(value=False,
                                     description='Confirm publication information',
                                     layout=Layout(width='100%', padding='2px', margin='0px'))

    view.submit_btn = Button(description='Submit Publication')
    submit_section = section('Confirm submission', [VBox([confirmation_checkbox, view.submit_btn])])

    content = VBox([publishing_info_section, file_metadata_section, submit_section])

    return content


def cell(text):
    """Create label for use within grid."""
    return Label(value=text, layout=Layout(border='1px solid lightgray', padding='2px', margin='0px'))


def cell_ddn(selected, choices):
    """Create dropdown menu for use within grid."""
    return Dropdown(value=selected, options=choices,
                    layout=Layout(border='1px solid lightgray', padding='2px', margin='0px'))


def title(text):
    """Create header text for use within grid."""
    return Label(value=text)


def adjust_progress(selected_index):
    """Change progress widget to reflect selected step."""
    log.debug("adjust.progress")
    for i, widget in enumerate(view.progress):
        # log.debug(f'i = {i}, selected_index = {selected_index}')

        if i == selected_index:
            widget.value = '<b><u>' + view.steps[i] + '</u></b>'
        else:
            widget.value = view.steps[i]
