import shutil
import os
import inspect

import hololinked.serializers
import hololinked.core

def define_env(env):

    @env.macro
    def thing_id_docstring():
        return hololinked.core.Thing.id.doc

    @env.macro
    def sub_things_docstring(): # does not work, dont know why
        return inspect.getdoc(hololinked.core.thing.Thing.sub_things)
    
    @env.macro
    def thing_logger_doc():
        return hololinked.core.thing.Thing.logger.doc
    
    @env.macro
    def thing_FSM_state_doc():
        return hololinked.core.thing.Thing.state.doc


# uncomment these while running the first time, then recomment them:
# otherwise mkdocs will reload in an infinite loop.

# source_path = os.path.join(os.path.dirname(hololinked.core.__file__), 'protocols', 'zmq', 'request_message_header_schema.json')
# destination_path = os.path.join('docs', 'api-reference', 'protocols', 'zmq', 'request-message-header-schema.json')
# os.makedirs(os.path.dirname(destination_path), exist_ok=True)
# shutil.copyfile(source_path, destination_path)

# source_path = os.path.join(os.path.dirname(hololinked.core.__file__), 'protocols', 'zmq', 'response_message_header_schema.json')
# destination_path = os.path.join('docs', 'api-reference', 'protocols', 'zmq', 'response-message-header-schema.json.json')
# os.makedirs(os.path.dirname(destination_path), exist_ok=True)
# shutil.copyfile(source_path, destination_path)
