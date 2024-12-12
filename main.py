

def define_env(env):

    @env.macro
    def my_macro():
        return 'Hello, World!'