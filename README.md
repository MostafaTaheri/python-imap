# IMAP

Easily ingest messages from POP3, IMAP, or local mailboxes.

This app allows you to either ingest e-mail content from common e-mail services (as long as the service provides POP3 or IMAP support)

## Requirements

```
    pip install -r requirements.txt
```

## Configuration

Edit config.yml for handlers information.

```
    handlers:
      - name: imap
		username: '<Username>'
		password: '<Password>'
		hostname: '<Email address>'
		timeout: 30
		port: '<Port>'
		search: 'SINCE'
		flag: 'ALL'
		select: 'inbox'
```

## How to use

```
    python read_email.py
```
