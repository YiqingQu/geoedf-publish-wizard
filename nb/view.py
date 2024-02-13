# view.py - User interface, rcampbel@purdue.edu, Oct 2023
import os
import sys

import matplotlib.pyplot as plt
from IPython.core.display import clear_output
from IPython.display import display
from ipywidgets import Accordion, Dropdown, HBox, Label, \
    Layout, HTML, Text, VBox, Button, Stack, Textarea, Checkbox, RadioButtons, \
    widgets

from nb.config import YRS, VAL, SELECT_FILES, EXTRACT_METADATA, \
    REVIEW_PUBLISH_INFO, PUBLISH, TAB_TITLES, \
    TASK_LIST_TITLE, TASK_LIST_TEXT
from nb.log import log, log_handler

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


def start(show_log, when_upload_completed, user_projects):
    """Build the user interface."""
    display(HTML(filename='nb/custom.html'))  # Send CSS code down to browser    
    app_title = HTML('GeoEDF Publishing Wizard')
    app_title = HTML(
        '<h2 style="margin-bottom: 5px; font-weight: bold; text-align: center;">GeoEDF Publish Wizard</h2>')
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
    view.steps = [SELECT_FILES, EXTRACT_METADATA, REVIEW_PUBLISH_INFO, PUBLISH]

    # Create stack - NOTE Maintain corresponding order of IDs & children!
    view.stack = Stack([
        select_files_screen(),
        extract_metadata_screen(),
        review_publish_info_screen(),
        publish_screen(),
        # view_publish_status_screen()
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
    '''Create widgets for introductory tab content'''
    content = []
    content.append(section(TASK_LIST_TITLE, [HTML(value=TASK_LIST_TEXT)]))

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


from ipyfilechooser import FileChooser


def select_files_screen():
    # Code for 'Select Files' screen
    # This will be similar to the old 'first_screen' and 'upload_screen'
    # File type selection
    file_type_ddn = RadioButtons(description='File Type:', options=['Geospatial Files', 'Workflow', 'Other Files'])

    # File uploader
    geospatial_chooser = FileChooser('/Users/')
    geospatial_chooser.title = 'Select Geospatial Files:'
    geospatial_chooser.filter_pattern = '*'
    geospatial_chooser.use_dir_icons = True
    geospatial_chooser.allow_multiple = True

    # File chooser for workflow file (single file selection)
    workflow_chooser = FileChooser('/Users/')
    workflow_chooser.title = 'Select Workflow YAML:'
    workflow_chooser.filter_pattern = '*.yml'
    workflow_chooser.use_dir_icons = True
    workflow_chooser.allow_multiple = False

    # File chooser for input files (allowing multiple selection)
    input_chooser = FileChooser('/Users/')
    input_chooser.title = 'Select Input Files (Optional):'
    input_chooser.filter_pattern = '*'
    input_chooser.use_dir_icons = True
    input_chooser.allow_multiple = True

    # Output folder selection (single directory selection)
    output_folder_chooser = FileChooser('/Users/', show_only_dirs=True)
    output_folder_chooser.title = 'Select Output Folder:'
    output_folder_chooser.use_dir_icons = True

    # File chooser for other files (allowing multiple selection)
    other_files_chooser = FileChooser('/Users/')
    other_files_chooser.title = 'Select Other Files:'
    other_files_chooser.filter_pattern = '*'
    other_files_chooser.use_dir_icons = True
    other_files_chooser.allow_multiple = True

    # geospatial_uploader = FileUpload(accept='', multiple=True, description='Geospatial Files')
    # workflow_uploader = FileUpload(accept='.yml', multiple=False, description='Workflow YAML')
    # input_uploader = FileUpload(accept='', multiple=True, description='Input Files (Optional)')
    # output_folder_text = Text(description='Output Folder:')
    # other_files_uploader = FileUpload(accept='', multiple=True, description='Other Files')

    # Display based on selection
    def on_file_type_change(change):
        if change['new'] == 'Geospatial Files':
            uploader_box.children = [geospatial_chooser]
        elif change['new'] == 'Workflow':
            uploader_box.children = [workflow_chooser, input_chooser, output_folder_chooser]
        else:  # Other Files
            uploader_box.children = [other_files_chooser]

    file_type_ddn.observe(on_file_type_change, names='value')
    uploader_box = VBox([])
    on_file_type_change({'new': file_type_ddn.value})  # Initialize with the default selection

    # Create and display a FileChooser widget
    # fc = FileChooser('/Users')
    # display(fc)

    content = [file_type_ddn, uploader_box, ]
    # content.append(view.new_section(CRITERIA_TITLE, section_list))
    return VBox([section("File Selection", content)])


def extract_metadata_screen():
    # Code for 'Extract Metadata' screen
    # This can be derived from the old 'submission_screen'
    import os
    username = os.getenv('JUPYTERHUB_USER')
    title_entry_area = Text(description='Title:')
    metadata_entry_area = Textarea(description='Description:', layout=Layout(width='90%', height='100px'))

    # Obtain username from Jupyter environment or allow manual entry
    username_text = Text(description='Creator:',
                         value=username)
    keyword_area = Textarea(description='Keyword:', layout=Layout(width='90%', height='50px'))

    content = [title_entry_area, username_text, metadata_entry_area, keyword_area]
    return VBox([section("Metadata Specification", content)])


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
    file_metadata_section = section("File Metadata Summary", [HTML(value=file_metadata_html)])

    # Construct HTML formatted summary for Publishing Information
    publishing_info_html = "<h4>Metadata:</h4><ul>"
    metadata_info['Creator'] = os.getenv('JUPYTERHUB_USER')
    for key, value in metadata_info.items():
        publishing_info_html += f"<li><b>{key}:</b> {value}</li>"
    publishing_info_html += "</ul>"
    publishing_info_section = section("Publishing Information", [HTML(value=publishing_info_html)])

    # # Action buttons to go back or proceed
    # back_button = Button(description='Back', button_style='warning')
    # proceed_button = Button(description='Proceed to Publish', button_style='success', disabled=True)
    #
    # # Enable proceed button only if the confirmation checkbox is checked
    # def on_checkbox_change(change):
    #     proceed_button.disabled = not change['new']
    #
    # confirmation_checkbox.observe(on_checkbox_change, names='value')
    #
    # # Action buttons section
    # action_buttons_section = HBox([back_button, proceed_button])

    # Assembling all sections into the final layout
    content = VBox([publishing_info_section, file_metadata_section])

    return content


def publish_screen():
    # Confirmation checkbox
    confirmation_checkbox = Checkbox(value=False,
                                     description='Confirm checkbox content')

    view.submit_btn = Button(description='Submit')
    content = [section('Confirm submission', [VBox([confirmation_checkbox, view.submit_btn])],
                       'Press the button below to submit the publishing task.')]
    # view.activity_out = Output()
    # content += [
    #     section('b) Review submission activity', [view.activity_out], 'Completed submissions are listed below.')]

    return VBox(content)


def view_publish_status_screen():
    # Code for 'View Publish Status' screen
    # This is a new step, so you'll need to create this screen based on your requirements
    content = []
    content.append(section('[Track Publishing Status]', [HBox([])]))
    return VBox(content)


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


def display_plot(data):
    """Ask data to plot itself then show that plot."""
    with view.plot_area:
        clear_output(wait=True)

        if type(data) is str:
            display(Label(data))
        else:  # data is a pandas dataframe
            _, ax = plt.subplots()
            data.plot(title='Value Trends', xlabel=YRS, ylabel=VAL, legend=True, grid=True, figsize=(10, 5))
            ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))  # Move legend outside plot area
            plt.show()


def adjust_progress(selected_index):
    """Change progress widget to reflect selected step."""
    log.debug("adjust.progress")
    for i, widget in enumerate(view.progress):
        # log.debug(f'i = {i}, selected_index = {selected_index}')

        if i == selected_index:
            widget.value = '<b><u>' + view.steps[i] + '</u></b>'
        else:
            widget.value = view.steps[i]
