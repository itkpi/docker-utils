from jinja2 import Environment, FileSystemLoader
import os
import sys
import argparse


def env_to_props(env_prefix, exclude=[]):
    def escape_prop(key):
        without_prefix = key.replace(env_prefix, '')
        replace_underscore = without_prefix.replace('_', '.')
        replace_placeholders = replace_underscore.replace('~', '_') if '~' in replace_underscore else replace_underscore
        return replace_placeholders.lower()

    props = {escape_prop(env_name): value for (env_name, value) in os.environ.items() if env_name not in exclude and env_name.startswith(env_prefix)}
    return props


def exit_if_absent(env_var):
    """Check if an environment variable is absent.
    Args:
        env_var: Name of environment variable.
    Returns:
        Returns True if env variable exists, False otherwise.
    """
    if not os.environ.get(env_var):
        print("%s is required." % (env_var,), file=sys.stderr)
        return False
    return True


def fill_and_write_template(template_file, output_file, context=os.environ):
    """Uses Jinja2 template and environment variables to create configuration
       files.
       Adds parse_log4j_loggers as a custom function for log4j.property parsing.
    Args:
        template_file: template file path.
        output_file: output file path.
        context: the data for the filling in the template, defaults to environment variables.
    Returns:
        Returns False if an Exception occurs, True otherwise.
    """
    try:
        j2_env = Environment(
            loader=FileSystemLoader(searchpath="/"),
            trim_blocks=True)
        j2_env.globals['env_to_props'] = env_to_props
        with open(output_file, 'w') as f:
            template = j2_env.get_template(template_file)
            f.write(template.render(env=context))

        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    root = argparse.ArgumentParser(description='Docker Utility Belt.')

    actions = root.add_subparsers(help='Actions', dest='action')

    template = actions.add_parser('template', description='Generate template from env vars.')
    template.add_argument('input', help='Path to template file.')
    template.add_argument('output', help='Path of output file.')

    check_env = actions.add_parser('ensure', description='Check if env var exists.')
    check_env.add_argument('name', help='Name of env var.')

    check_env = actions.add_parser('ensure-atleast-one', description='Check if env var exists.')
    check_env.add_argument('names', nargs='*', help='Names of env var.')

    check_env = actions.add_parser('wait', description='Wait for network service to appear.')
    check_env.add_argument('host', help='Host.')
    check_env.add_argument('port', help='Port.', type=int)
    check_env.add_argument('timeout', help='timeout in secs.', type=float)

    check_env = actions.add_parser('http-ready', description='Wait for an HTTP/HTTPS URL to be retrievable.')
    check_env.add_argument('url', help='URL to retrieve. Expected HTTP status code: 2xx.')
    check_env.add_argument('timeout', help='Time in secs to wait for the URL to be retrievable.', type=float)

    check_env = actions.add_parser('path', description='Check for path permissions and existence.')
    check_env.add_argument('path', help='Full path.')
    check_env.add_argument('mode', help='One of [writable, readable, executable, exists].',
                           choices=['writable', 'readable', 'executable', 'exists'])

    check_env = actions.add_parser('path-wait', description='Wait for a path to exist')
    check_env.add_argument('path', help='Full path.')
    check_env.add_argument('timeout', help='Time in secs to wait for the path to exist.', type=float)

    if len(sys.argv) < 2:
        root.print_help()
        sys.exit(1)

    args = root.parse_args()

    success = False

    if args.action == "template":
        success = fill_and_write_template(args.input, args.output)
    elif args.action == "ensure":
        success = exit_if_absent(args.name)

    if success:
        sys.exit(0)
    else:
        command = " ".join(sys.argv)
        print("Command [%s] FAILED !" % command, file=sys.stderr)
        sys.exit(1)

