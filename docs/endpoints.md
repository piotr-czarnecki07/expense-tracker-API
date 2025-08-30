# Endpoints

Each endpoint requires an HTTP POST request.\
Appropriate data should be sent to each endpoint.

In case of an error, the following respose is send

```json
{
    "error": "Reason why error occured"
}
```

## User-action based

- `/user/signup/` - creates an accoun and generates token for user.\
Email must be unique for each user.

**JSON example**

```json
{
    "username": "",
    "email": "",
    "password": ""
}
```

**Response**

```json
{
    "token": "A string of 50 characters"
}
```

- `/user/login/` - generates new token when user is not logged in

**JSON example**

```json
{
    "email": "",
    "password": ""
}
```

**Response**

```json
{
    "token": ""
}
```

- `/user/remind/` - sends token that is currently assigned to user

**JSON example**

```json
{
    "email": "",
    "password": ""
}
```

**Response**

```json
{
    "token": ""
}
```

- `/user/logout/` - sets token for user as "logged_out", makes previous token outdated.\
User must log in to create new token.

**JSON example**

```json
{
    "token": ""
}
```

**Response**

```json
{
    "message": "User logged out successfully"
}
```

### Operation based

- `/operation/add/` - creates new expense.\
See how **categories** work in [categories.md](categories.md).

**JSON example**

```json
{
    "title": "",
    "amount": 12.34,
    "categories": [
        1,
        2,
        3
    ],
    "token": ""
}
```

**Response**

Expense object

- `/operation/update/` - updates listed expenses with provided data.\
Within an object provide an ID number of the expense and fields with new value that you would like to update.

**JSON example**

```json
{
    "token": "",
    "expenses": [
        {
            "id": 1,
            "title": ""
        },
        {
            "id": 2,
            "amount": 123.45
        },
        {
            "id": 3,
            "title": "",
            "amount": 123.45
        },
        {
            "id": 4,
            "categoires": [
                1,
                2,
                3
            ]
        },
        {
            "id": 5
        }
    ]
}
```

**Response**

A list of updated expense objects

- `/operation/get/` - returns a list of expense objects, that was requested by their ID numbers

**JSON example**

```json
{
    "token": "",
    "expenses": [
        1,
        2,
        3
    ]
}
```

**Response**

A list of expense objects

- `/operation/delete/` - Changes task's status from "to-do" to "done"

**JSON example**

```json
{
    "token": "",
    "expenses": [
        1,
        2,
        3
    ]
}
```

**Response**

A list of deleted expense objects
