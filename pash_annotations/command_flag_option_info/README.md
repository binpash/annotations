## JSON Format
```
{
    "flag": [ <list of flags> ],
    "option": [ <list of [ <option_flag> , <option_arg> ] values ]
}
```

## Script

#### How To Use
Run `./manpage-to-json.sh [command_name]` to print a JSON file containing the tags and options for [command_name] from its man page.

This script calls args-to-json.py.

#### Example
```
./manpage-to-json.sh cat
```
