import os
import sys

from nb.config import MAP_PUBLICATION_TO_FILE_TYPE

model = sys.modules[__name__]
model.publication = None


class Publication:
    def __init__(self, publication_type=None, title='', creator='', description='', keywords=''):
        self.publication_type = publication_type
        self.title = title
        self.creator = creator
        self.description = description
        self.keywords = keywords
        self.files = {}
        self.status = 'Draft'

        # Only initialize file structure if a valid publication type is provided
        if publication_type in MAP_PUBLICATION_TO_FILE_TYPE:
            file_types = MAP_PUBLICATION_TO_FILE_TYPE[publication_type]
            for file_type in file_types:
                self.files[file_type] = []

    def set_type(self, publication_type):
        self.files = {}
        if publication_type in MAP_PUBLICATION_TO_FILE_TYPE:
            file_types = MAP_PUBLICATION_TO_FILE_TYPE[publication_type]
            for file_type in file_types:
                self.files[file_type] = []

    def add_file(self, file_path, file_type):
        """
        Adds a file to the publication under the appropriate file type,
        only if the file type is valid for the publication's type.

        :param file_path: Path to the file
        :param file_type: Type of the file, must be valid for the publication's type
        """
        if file_type in self.files:
            self.files[file_type].append({
                'path': file_path,
                'filename': os.path.basename(file_path),
            })

        else:
            print(
                f"File type: {file_type} is not valid for this publication type: {self.publication_type}. File not added.")
        # log.debug(f"[CLASS add_file] files: {self.files}")

    def update_metadata(self, publication_type=None, title=None, creator=None, description=None, keywords=None):
        """
        Updates the metadata for the publication.

        :param publication_type: The type of the publication
        :param title: The title of the publication
        :param creator: The creator of the publication
        :param description: The description of the publication
        :param keywords: The keywords associated with the publication
        """
        if publication_type:
            self.publication_type = publication_type
        if title:
            self.title = title
        if creator:
            self.creator = creator
        if description:
            self.description = description
        if keywords:
            self.keywords = keywords

    def publish(self):
        """
        Changes the status of the publication to 'Published'.
        """
        self.status = 'Published'
        # Additional logic to handle the publication process

    def __repr__(self):
        return f"Publication(type={self.publication_type}, title={self.title}, creator={self.creator}, status={self.status})"


# # Example of using the updated Publication class
# pub_workflow = Publication(publication_type=PUBLICATION_TYPE_WORKFLOW,
#                            title='Workflow Publication',
#                            creator='Alice',
#                            description='A detailed workflow publication.',
#                            keywords='workflow, example')
#
# pub_workflow.add_file('/path/to/workflow/process.yml', FILE_TYPE_YAML)
# pub_workflow.add_file('/path/to/data/input.csv', FILE_TYPE_INPUT)
# pub_workflow.add_file('/path/to/results/output.csv', FILE_TYPE_OUTPUT)
#
# # Trying to add a file type that is not valid for the publication type
# pub_workflow.add_file('/path/to/image/map.png', FILE_TYPE_GEOSPATIAL)
#
# print(pub_workflow)
#

def start():
    """Prep model."""
    model.publication = Publication()
