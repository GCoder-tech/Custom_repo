import os
import requests

def get_login_by_email(email):
    token = os.environ['GITHUB_TOKEN']
    headers = { "Authorization": f"Bearer {token}" }
    query = """
    query($email: String!) {
        search(query: $email, type: USER, first: 1) {
            nodes {
                ... on User {
                login
                }
            }
        }
    }
    """

    response = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': {'email': email}}, headers=headers)
    if response.status_code == 200:
        result = response.json()
        nodes = result['data']['search']['nodes']
        if nodes:
            github_login = nodes[0]['login']
            print(f"Found user {github_login} - with email {email}")

            with open('github_login.txt', 'w') as output_file:
                output_file.write(github_login)
        else:
            print("No user found")
    else:
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {response.text}")

if __name__ == "__main__":
    email = os.environ['INPUT_EMAIL']
    get_login_by_email(email)
