# DATA EXTRACT COMMAND LINE INTERFACE (CLI)

## Requirements
[AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) 

## Installation
`./install`

If you choose to skip the configuration, you will have to configure environment variables in `$HOME/.airvantage-etl/.env` yourself.  

## Usage
`airvantage-etl --help`

Copy the extract request json:  
`cp extract-request.json.example extract-request.json`  
Remember to make sure the file is a valid json - there are some helpful comments in there.

### Run your first extract
`airvantage-etl extract --help`  
`airvantage-etl extract --input-json-path ./extract-request.json`

### Signed
Henk van Zyl (Symbyte) [henk@symbyte.tech](mailto:henk@symbyte.tech)  
Alexander Glöss (Symbyte) [alexander@symbyte.tech](mailto:alexander@symbyte.tech)
