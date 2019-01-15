# sdub

sdub is python utility to generate `.properties` files using Jinja2 templates from environment variables.
Inpired by `dub` created by [confluent inc](https://github.com/confluentinc/confluent-docker-utils).

Unlike original `dub` allows to have properties containing underscores `_`.
`sdub template` commands transforms `jinja2` template 
(which typically reads environment variables and transforms them into key-value pair)
written as 'MY_SUPER_PROP' so that resulting file will contain `prop=value`.

For instance Jinja2 template in `sample.properties.template` file:
```jinja
{% set connect_props = env_to_props('MY_SUPER_') -%}
{% for(name, value) in connect_props.items() -%}
{{name}}={{value}}
{% endfor -%}
```

Usage:

```bash
export MY_SUPER_DEVOPS_PROP=5
export MY_SUPER_DEVOPS_PROP~WITH~UNDERSCORE=10

sdub sample.properties.template sample.properties
```

Resulting file will look like:

```
devops.prop=5
devops.prop_with_underscore=10
```

There are also a [Dockerfile](./Dockerfile) based on `debian/jessie` image with this script installed.

You may also ensure some environment variables set using `sdub ensure`:

```bash
sdub ensure PATH # obviously works
sdub ensure PATH0 # throw an error if you haven't exported PATH0
```
