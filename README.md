# Craftsperson Environment

# What is it?
**craftsperson_env** reads configuration files in **yaml**, **env**, **toml**, **xml**, and **json** formats and adds them to the **'os.environ'** system. It formats the keys according to **naming-case-type**, **upper** or **lower**, and arranges them with a **specific join type in the upper-lower section**. Additionally, it specifies the data type when retrieving data from 'os.environ' to access data of that type.

# Where to get it
You can access the <a href="https://github.com/celalakcelikk/craftsperson-env">Github</a> repository from here.

Pip installers for the latest released version are available at the <a href="https://pypi.org/project/craftsperson-env">Python Package Index (PyPI)</a>

# Installation

```
python setup.py install
```
```
pip install craftsperson-env
```

# Import Library
```python
from craftsperson_env import CraftsEnvConfig
```

# Create Config Variable
```python
config = CraftsEnvConfig()
```

# Load File
**Description**
```
Help on method load_config_file in module craftsperson_env.main:

load_config_file(file_path: str, root_full_path: str = './', naming_case_type: str = None, naming_case_join_type: str = '', is_change_config_env_format: bool = False, config_env_replace_first_value: str = None, is_remove_xml_first_level: bool = False, extra_config_file_params: dict = {}) method of craftsperson_env.main.CraftsEnvConfig instance
    This function processes and uses a config file.
    
    Parameters
    ----------
    file_path : str
        This parameter specifies the file location path.
    root_full_path : str, optional
        This parameter retrieves the full path from the file. The default is './'.
    naming_case_type : str, optional
        This parameter specifies naming case types for env, yaml, json, xml, or toml. The default is None.
    naming_case_join_type : str, optional.
        This parameter specifies the join type, allowing values such as "", "-", or "_". The default is "".
    is_change_config_env_format: bool, optional.
        This parameter specifies whether the format of the env config file has been changed.
            The default value is False.
    config_env_replace_first_value: str, optional.
        This parameter specifies the replacement value for the first occurrence. The default is None.
    is_remove_xml_first_level : bool, optional
        This parameter determines whether to remove the first level. The default value is False.
    extra_config_file_params : dict, optional
        This parameter retrieves additional XML or TOML configuration parameters. The default value is {}.
    
    Returns
    -------
    None.
```

## Yaml File Use Case
```
version: 2.0
application:
  name: MyWebApp
  version: 1.2.3
  environment: production
  base_url: "https://mywebapp.example.com"
  allowed_hosts:
    - mywebapp.example.com
    - api.mywebapp.example.com
  options:
    use_ssl: true
    ssl_cert: "/path/to/cert"
json_format: "{'test': 1}"
```

```python
config.load_config_file(
    file_path="examples/yaml_config_file.yaml",
    root_full_path="examples/",
    naming_case_type="upper",
    naming_case_join_type=".",
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['VERSION',
     'APPLICATION.NAME',
     'APPLICATION.VERSION',
     'APPLICATION.ENVIRONMENT',
     'APPLICATION.BASE_URL',
     'APPLICATION.ALLOWED_HOSTS',
     'APPLICATION.OPTIONS.USE_SSL',
     'APPLICATION.OPTIONS.SSL_CERT',
     'JSON_FORMAT']

## Xml File Use Case
```
<config>
  <version>2.0</version>
  <application>
    <name>MyWebApp</name>
    <version>1.2.3</version>
    <environment>production</environment>
    <base_url>https://mywebapp.example.com</base_url>
    <allowed_hosts>
      <host>mywebapp.example.com</host>
      <host>api.mywebapp.example.com</host>
    </allowed_hosts>
    <options>
      <use_ssl>true</use_ssl>
      <ssl_cert>/path/to/cert</ssl_cert>
    </options>
  </application>
  <json_format>
    {'test': 1}
  </json_format>
</config>
```
The **is_remove_xml_first_level** default value is **False**.
```python
config.load_config_file(
    file_path="xml_config_file.xml",
    root_full_path = "./",
    naming_case_type="upper",
    naming_case_join_type = ".",
    is_remove_xml_first_level=False,
    extra_config_file_params={}
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['CONFIG.VERSION',
     'CONFIG.APPLICATION.NAME',
     'CONFIG.APPLICATION.VERSION',
     'CONFIG.APPLICATION.ENVIRONMENT',
     'CONFIG.APPLICATION.BASE_URL',
     'CONFIG.APPLICATION.ALLOWED_HOSTS.HOST',
     'CONFIG.APPLICATION.OPTIONS.USE_SSL',
     'CONFIG.APPLICATION.OPTIONS.SSL_CERT',
     'CONFIG.JSON_FORMAT']
The **is_remove_xml_first_level** is **True**, which removes the first level.
```python
config.load_config_file(
    file_path="xml_config_file.xml",
    root_full_path = "./",
    naming_case_type="upper",
    naming_case_join_type = ".",
    is_remove_xml_first_level=True,
    extra_config_file_params={}
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['CONFIG.APPLICATION.NAME',
     'CONFIG.APPLICATION.VERSION',
     'CONFIG.APPLICATION.ENVIRONMENT',
     'CONFIG.APPLICATION.BASE_URL',
     'CONFIG.APPLICATION.ALLOWED_HOSTS.HOST',
     'CONFIG.APPLICATION.OPTIONS.USE_SSL',
     'CONFIG.APPLICATION.OPTIONS.SSL_CERT',
     'CONFIG.JSON_FORMAT',
     'APPLICATION.ALLOWED_HOSTS.HOST']

## Toml File Use Case
```
version = "2.0"
json_format = "{'test': 1}"

[application]
name = "MyWebApp"
version = "1.2.3"
environment = "production"
base_url = "https://mywebapp.example.com"
allowed_hosts = ["mywebapp.example.com", "api.mywebapp.example.com"]

[application.options]
use_ssl = true
ssl_cert = "/path/to/cert"
```
```python
config.load_config_file(
    file_path="toml_config_file.toml",
    root_full_path = "./",
    naming_case_type="upper",
    naming_case_join_type = ".",
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['VERSION',
     'JSON_FORMAT',
     'APPLICATION.NAME',
     'APPLICATION.VERSION',
     'APPLICATION.ENVIRONMENT',
     'APPLICATION.BASE_URL',
     'APPLICATION.ALLOWED_HOSTS',
     'APPLICATION.OPTIONS.USE_SSL',
     'APPLICATION.OPTIONS.SSL_CERT']

## Json File Use Case
```
{
    "version": "2.0",
    "application": {
      "name": "MyWebApp",
      "version": "1.2.3",
      "environment": "production",
      "base_url": "https://mywebapp.example.com",
      "allowed_hosts": ["mywebapp.example.com", "api.mywebapp.example.com"],
      "options": {
        "use_ssl": true,
        "ssl_cert": "/path/to/cert"
      }
    },
    "json_format": "{'test': 1}"
}
```
```python
config.load_config_file(
    file_path="json_config_file.json",
    root_full_path = "./",
    naming_case_type="upper",
    naming_case_join_type = ".",
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['VERSION',
     'APPLICATION.NAME',
     'APPLICATION.VERSION',
     'APPLICATION.ENVIRONMENT',
     'APPLICATION.BASE_URL',
     'APPLICATION.ALLOWED_HOSTS',
     'APPLICATION.OPTIONS.USE_SSL',
     'APPLICATION.OPTIONS.SSL_CERT',
     'JSON_FORMAT']

## Env File Use Case
```
VERSION=2.0
APPLICATION_NAME=MyWebApp
APPLICATION_VERSION=1.2.3
APPLICATION_ENVIRONMENT=production
APPLICATION_BASE_URL=https://mywebapp.example.com
APPLICATION_ALLOWED_HOSTS=mywebapp.example.com,api.mywebapp.example.com
APPLICATION_OPTIONS_USE_SSL=true
APPLICATION_OPTIONS_SSL_CERT=/path/to/cert
JSON_FORMAT="{'test': 1}"
```
The **is_change_config_env_format** default value is **False**.

```python
config.load_config_file(
    file_path="env_config_file.env",
    root_full_path = "./",
    naming_case_type="upper",
    is_change_config_env_format=False,
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['VERSION',
     'APPLICATION_NAME',
     'APPLICATION_VERSION',
     'APPLICATION_ENVIRONMENT',
     'APPLICATION_BASE_URL',
     'APPLICATION_ALLOWED_HOSTS',
     'APPLICATION_OPTIONS_USE_SSL',
     'APPLICATION_OPTIONS_SSL_CERT',
     'JSON_FORMAT']

The **is_change_config_env_format** is **True**, which changes env format.

The **config_env_replace_first_value** is **"_"**, which replacement value for the first occurrence. 

```python
config.load_config_file(
    file_path="env_config_file.env",
    root_full_path = "./",
    naming_case_type="upper",
    naming_case_join_type=".",
    is_change_config_env_format=True,
    config_env_replace_first_value="_"
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['VERSION',
     'APPLICATION.NAME',
     'APPLICATION.VERSION',
     'APPLICATION.ENVIRONMENT',
     'APPLICATION.BASE.URL',
     'APPLICATION.ALLOWED.HOSTS',
     'APPLICATION.OPTIONS.USE.SSL',
     'APPLICATION.OPTIONS.SSL.CERT',
     'JSON.FORMAT']

## Naming Case Type Use Case

### Pascal Case

```python
config.load_config_file(
    file_path="json_config_file.json",
    root_full_path = "./",
    naming_case_type="pascal"
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['Version',
     'ApplicationName',
     'ApplicationVersion',
     'ApplicationEnvironment',
     'ApplicationBase_url',
     'ApplicationAllowed_hosts',
     'ApplicationOptionsUse_ssl',
     'ApplicationOptionsSsl_cert',
     'Json_format']

### Camel Case
```python
config.load_config_file(
    file_path="json_config_file.json",
    root_full_path = "./",
    naming_case_type="camel"
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['version',
     'applicationName',
     'applicationVersion',
     'applicationEnvironment',
     'applicationBase_url',
     'applicationAllowed_hosts',
     'applicationOptionsUse_ssl',
     'applicationOptionsSsl_cert',
     'json_format']

### Snake Case
```python
config.load_config_file(
    file_path="json_config_file.json",
    root_full_path = "./",
    naming_case_type="snake"
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['applicationOptionsSsl_cert',
     'json_format',
     'application_name',
     'application_version',
     'application_environment',
     'application_base_url',
     'application_allowed_hosts',
     'application_options_use_ssl',
     'application_options_ssl_cert']

### Kebab Case
```python
config.load_config_file(
    file_path="json_config_file.json",
    root_full_path = "./",
    naming_case_type="kebab"
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['version',
     'application-name',
     'application-version',
     'application-environment',
     'application-base_url',
     'application-allowed_hosts',
     'application-options-use_ssl',
     'application-options-ssl_cert',
     'json_format']

### Flat Case
```python
config.load_config_file(
    file_path="json_config_file.json",
    root_full_path = "./",
    naming_case_type="flat"
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['version',
     'applicationname',
     'applicationversion',
     'applicationenvironment',
     'applicationbase_url',
     'applicationallowed_hosts',
     'applicationoptionsuse_ssl',
     'applicationoptionsssl_cert',
     'json_format']

### Upper-Flat Case
```python
config.load_config_file(
    file_path="json_config_file.json",
    root_full_path = "./",
    naming_case_type="upper-flat"
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['VERSION',
     'APPLICATIONNAME',
     'APPLICATIONVERSION',
     'APPLICATIONENVIRONMENT',
     'APPLICATIONBASE_URL',
     'APPLICATIONALLOWED_HOSTS',
     'APPLICATIONOPTIONSUSE_SSL',
     'APPLICATIONOPTIONSSSL_CERT',
     'JSON_FORMAT']

### Pascal-Snake Case
```python
config.load_config_file(
    file_path="json_config_file.json",
    root_full_path = "./",
    naming_case_type="pascal-snake"
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['Version',
     'Application_Name',
     'Application_Version',
     'Application_Environment',
     'Application_Base_url',
     'Application_Allowed_hosts',
     'Application_Options_Use_ssl',
     'Application_Options_Ssl_cert',
     'Json_format']

### Camel-Snake Case
```python
config.load_config_file(
    file_path="json_config_file.json",
    root_full_path = "./",
    naming_case_type="camel-snake"
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['version',
     'application_Name',
     'application_Version',
     'application_Environment',
     'application_Base_url',
     'application_Allowed_hosts',
     'application_Options_Use_ssl',
     'application_Options_Ssl_cert',
     'json_format']

### Screaming-Snake Case
```python
config.load_config_file(
    file_path="json_config_file.json",
    root_full_path = "./",
    naming_case_type="screaming-snake"
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['VERSION',
     'APPLICATION_NAME',
     'APPLICATION_VERSION',
     'APPLICATION_ENVIRONMENT',
     'APPLICATION_BASE_URL',
     'APPLICATION_ALLOWED_HOSTS',
     'APPLICATION_OPTIONS_USE_SSL',
     'APPLICATION_OPTIONS_SSL_CERT',
     'JSON_FORMAT']

### Train Case
```python
config.load_config_file(
    file_path="json_config_file.json",
    root_full_path = "./",
    naming_case_type="train"
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['Version',
     'Application-Name',
     'Application-Version',
     'Application-Environment',
     'Application-Base_url',
     'Application-Allowed_hosts',
     'Application-Options-Use_ssl',
     'Application-Options-Ssl_cert',
     'Json_format']

### Cobol Case
```python
config.load_config_file(
    file_path="json_config_file.json",
    root_full_path = "./",
    naming_case_type="cobol"
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['VERSION',
     'APPLICATION-NAME',
     'APPLICATION-VERSION',
     'APPLICATION-ENVIRONMENT',
     'APPLICATION-BASE_URL',
     'APPLICATION-ALLOWED_HOSTS',
     'APPLICATION-OPTIONS-USE_SSL',
     'APPLICATION-OPTIONS-SSL_CERT',
     'JSON_FORMAT']

### Other Case: Upper
```python
config.load_config_file(
    file_path="json_config_file.json",
    root_full_path = "./",
    naming_case_type="upper",
    naming_case_join_type = "."
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['VERSION',
     'APPLICATION.NAME',
     'APPLICATION.VERSION',
     'APPLICATION.ENVIRONMENT',
     'APPLICATION.BASE_URL',
     'APPLICATION.ALLOWED_HOSTS',
     'APPLICATION.OPTIONS.USE_SSL',
     'APPLICATION.OPTIONS.SSL_CERT',
     'JSON_FORMAT']

### Other Case: Lower
```python
config.load_config_file(
    file_path="json_config_file.json",
    root_full_path = "./",
    naming_case_type="lower",
    naming_case_join_type = "."
)
```
```python
import os
key_list = list(os.environ.keys())[-9:]
key_list
```
    ['version',
     'application.name',
     'application.version',
     'application.environment',
     'application.base_url',
     'application.allowed_hosts',
     'application.options.use_ssl',
     'application.options.ssl_cert',
     'json_format']

# Get the Value From the 'os.environ' System

**Description**
```
Help on function get in module craftsperson_env.__main__:

get(key: str, value_type: Any = <class 'str'>, default: Any = None) -> str
    This function retrieves the value associated with the key from the 'os.environ' system.
    
    Parameters
    ----------
    key: str
        This parameter retrieves the key from the 'os.environ' system.
    value_type: str, optional.
        This parameter accepts value types such as int, str, list, dict, and others. The default value is str.
    default: Any, optional.
        This parameter retrieves the default value if the key is not found in any environment variables.
            The default is None.
    
    Returns
    -------
    value:
        This returns the value of the given environment variable key.
```

Additionally, it specifies the data type when retrieving data from 'os.environ' to access data of that type. For example, value_type gets int, float, str, dict and other types.

```python
print("boolean:", config.get(key="application.options.use_ssl", value_type=bool, default=None))
print("float:", config.get(key="version", value_type=float, default=None))
print("str:", config.get(key="application.name", value_type=str, default=None))
print("json:", config.get(key="json_format", value_type=dict, default=None))
```
    boolean: True
    float: 2.0
    str: MyWebApp
    json: {'test': 1}


# Set and Update the Value in the 'os.environ' System.

**Description**
```
Help on function set in module craftsperson_env.__main__:

set(key: str, value: str) -> None
    This function sets a key-value pair in the 'os.environ' system.
    
    Parameters
    ----------
    key: str
        This parameter specifies the key to be set as an environment variable.
    value: str
        This parameter specifies the value that will be stored in
            the environment variable identified by the given key.
    
    Returns
    -------
    None.
```

```python
config.set(key="int_value", value="1923")
```
```python
print("int:", config.get(key="int_value", value_type=int, default=None))
```
    int: 1923


# Author's Social Media

* Gmail: celalakcelikk@gmail.com
* Linkedin: https://www.linkedin.com/in/celalakcelik/
* Github: https://github.com/celalakcelikk
* Kaggle: https://www.kaggle.com/celalakcelik

