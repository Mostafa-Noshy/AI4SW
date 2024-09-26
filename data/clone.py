import json
import os
import subprocess

#JSON file
json_file = 'results.json'
with open(json_file, 'r') as file:
    data = json.load(file)

# Directory for repositories
clone_directory = 'java_projects'
if not os.path.exists(clone_directory):
    os.makedirs(clone_directory)

for project in data['items']:
    # Check if the project is primarily written in Java
    if 'Java' in project['languages']:
        repo_name = project['name']
        repo_url = f"https://github.com/{repo_name}.git"
        repo_dir = os.path.join(clone_directory, repo_name.split('/')[1])

        # Clone the repository
        if not os.path.exists(repo_dir):
            print(f"Cloning {repo_name}...")
            try:
                subprocess.run(['git', 'clone', repo_url, repo_dir], check=True)
                print(f"Successfully cloned {repo_name}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to clone {repo_name}: {e}")
        else:
            print(f"{repo_name} already cloned.")

