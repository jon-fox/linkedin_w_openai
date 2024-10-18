from linkedin_api import Linkedin
from requests.cookies import RequestsCookieJar, create_cookie
from linkedin_api.cookie_repository import CookieRepository
import json
import os

# username, etc are set as username::user
with open('credentials.txt') as f:
    for line in f:
        key, value = line.strip().split('::')
        os.environ[key] = value

# verify the environment variables are set
print(os.environ['username'])
print(os.environ['password'])
print(os.environ['profile'])

# linkedin has an annoying challenge thing, so grabbed cookies using get cookies.txt chrome extension
# used this solution from linkedin_api github issue
cookies = json.load(open('./cookies.json'))

cookie_jar = RequestsCookieJar()

for cookie_data in cookies:
    cookie = create_cookie(
        domain=cookie_data["domain"],
        name=cookie_data["name"],
        value=cookie_data["value"],
        path=cookie_data["path"],
        secure=cookie_data["secure"],
        expires=cookie_data.get("expirationDate", None),
        rest={
            "HttpOnly": cookie_data.get("httpOnly", False),
            "SameSite": cookie_data.get("sameSite", "unspecified"),
            "HostOnly": cookie_data.get("hostOnly", False),
        }
    )
    cookie_jar.set_cookie(cookie)


new_repo = CookieRepository()
new_repo.save(cookie_jar, os.environ['username'])

# create a new linkedin object
api = Linkedin(os.environ['username'], os.environ['password'])

conversations = api.get_conversations()
print(conversations)

profile = api.get_profile(os.environ['profile'])

print(f"Name: {profile['firstName']} {profile['lastName']}")

# GET a profiles contact info
contact_info = api.get_profile_contact_info(os.environ['profile'])
print(f"Contact info: {contact_info}")

# connections = api.get_profile_connections('1234asc12304')
# print(f"Connections: {connections}")
