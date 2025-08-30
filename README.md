# expense-tracker-API

RESTful API for managing a list of expenses.\
Uses JWT for authenticating users.\
Passwords and tokens are hashed before being stored in the database.

## Table of Contents

- [Local Setup](#local-setup)
- [Needed Files](#needed-files)
- [How to Use](#how-to-use)
- [License](#license)
- [Credits](#credits)

## Local Setup

1. Have Python 3.13+ installed.
2. Clone the repository.
3. Create local enviroment, for example by running `py -m venv venv` on Windows.
4. Install requirements from [requirements.txt](requirements.txt).
5. Create files from [Needed Files](#needed-files).

## Needed Files

You need `.env` file, that can be created based on [.env.example](expenseTrackerAPI/.env.example) file.\
Also you need `hashes.py` file, that contains tables to hash strings and place it in `expenseTrackerAPI/expenseTrackerAPIViews/` directory.

## How to Use

1. Create an account using `user/signup/` endpoint.
2. Save token that was sent as a response.
3. Send requests to any endpoints and provide this token.
4. After finishing using, send request to `user/logout/`.
5. If you want to login again, send request to `user/login/` and save new token.

For a full list of endpoints see [endpoints.md](docs/endpoints.md).

## License

See [License](License)

## Credits

Project idea: [roadmap.sh](https://roadmap.sh/projects/expense-tracker-api)
