import shutil
import os

import hololinked.serializers
import hololinked.server

def define_env(env):

    @env.macro
    def thing_id():
        return hololinked.server.Thing.id.doc
    
    


# uncomment these while running the first time, then recomment them:
# otherwise mkdocs will reload in an infinite loop.

# source_path = os.path.join(os.path.dirname(hololinked.server.__file__), 'protocols', 'zmq', 'request_message_header_schema.json')
# destination_path = os.path.join('docs', 'api-reference', 'protocols', 'zmq', 'request-message-header-schema.json')
# os.makedirs(os.path.dirname(destination_path), exist_ok=True)
# shutil.copyfile(source_path, destination_path)

# source_path = os.path.join(os.path.dirname(hololinked.server.__file__), 'protocols', 'zmq', 'response_message_header_schema.json')
# destination_path = os.path.join('docs', 'api-reference', 'protocols', 'zmq', 'response-message-header-schema.json.json')
# os.makedirs(os.path.dirname(destination_path), exist_ok=True)
# shutil.copyfile(source_path, destination_path)
