# OpenPanel Python SDK

The OpenPanel Python SDK allows you to track user behavior in your Python applications. This guide provides instructions for installing and using the Python SDK in your project.

## Installation

> ⚠️ This package is not yet published. So you cannot install it with `pip`

You can install the OpenPanel Python SDK using pip:

```bash
pip install openpanel
```

## Usage

### Initialization

First, import the SDK and initialize it with your client ID:

```python
from openpanel import OpenPanel

op = OpenPanel(client_id="YOUR_CLIENT_ID", client_secret="YOUR_CLIENT_SECRET")
```

### Options

When initializing the SDK, you can provide several options:

- `client_id` (required): Your OpenPanel client ID.
- `client_secret` (optional): Your OpenPanel client secret.
- `api_url` (optional): Custom API URL if you're not using the default OpenPanel API.
- `filter` (optional): A function to filter events before sending.
- `disabled` (optional): Set to `True` to disable event sending.

### Tracking Events

To track an event:

```python
op.track("button_clicked", {"button_id": "submit_form"})
```

### Identifying Users

To identify a user:

```python
op.identify("user123", {
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "customAttribute": "value"
})
```

### Setting Global Properties

To set properties that will be sent with every event:

```python
op.set_global_properties({
    "app_version": "1.0.2",
    "environment": "production"
})
```

### Creating Aliases

To create an alias for a user:

```python
op.alias("user123", "john_doe")
```

### Incrementing Properties

To increment a numeric property on a user profile:

```python
op.increment("user123", "login_count", 1)
```

### Decrementing Properties

To decrement a numeric property on a user profile:

```python
op.decrement("user123", "credits", 5)
```

### Clearing User Data

To clear the current user's data:

```python
op.clear()
```

## Advanced Usage

### Custom Event Filtering

You can set up custom event filtering:

```python
def my_filter(payload):
    # Your custom filtering logic here
    return True  # or False to filter out the event

op = OpenPanel(client_id="YOUR_CLIENT_ID", filter=my_filter)
```

### Disabling Tracking

You can temporarily disable tracking:

```python
op = OpenPanel(client_id="YOUR_CLIENT_ID", disabled=True)
```

## Thread Safety

The OpenPanel SDK is designed to be thread-safe. You can call its methods from any thread without additional synchronization.

## Support

For any issues or feature requests, please file an issue on our [GitHub repository](https://github.com/Openpanel-dev/python-sdk/issues).