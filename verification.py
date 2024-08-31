import re


def verify_emails(emails):
    priority_patterns = {
        'high': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
        'medium': re.compile(r'^(?!.*(info|support|contact)).*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
        'low': re.compile(r'^(info|support|contact)@.*'),
    }

    verified_emails = []

    for email in emails:
        if priority_patterns['high'].match(email):
            print(f"High priority email: {email}")
            verified_emails.append({'query': email, 'status': 'RECEIVING', 'priority': 'high'})
        elif priority_patterns['medium'].match(email):
            print(f"Medium priority email: {email}")
            verified_emails.append({'query': email, 'status': 'RECEIVING', 'priority': 'medium'})
        elif priority_patterns['low'].match(email):
            print(f"Low priority email: {email}")
            verified_emails.append({'query': email, 'status': 'RECEIVING', 'priority': 'low'})
        else:
            print(f"Invalid or low priority email: {email}")
            verified_emails.append({'query': email, 'status': 'INVALID', 'priority': 'none'})

    return verified_emails
