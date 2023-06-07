import os
import sys
from tkinter import Tk, messagebox
from tkinter.filedialog import askdirectory

import requests
import yaml

CONFIG_FILE = "config.yaml"

# Define the config.yaml structure
CONFIG_TEMPLATE = {
    "branches": [],
    "org": "REPLACE WITH ORGANIZATION NAME",
    "team_slug": "REPLACE WITH TEAM NAME",
    "token": "REPLACE WITH GITHUB PERSONAL ACCESS TOKEN"
}

# ANSI escape sequences for text color
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[96m"
RESET = "\033[0m"

def update_config_file():
    messagebox.showinfo("Config File Update", "The config file is missing or incomplete. Please update the config file.")

    # Load the existing config if it exists
    existing_config = {}
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as config_file:
            existing_config = yaml.safe_load(config_file)
    
    if not existing_config:
        existing_config = {}

    # Fill in missing fields from the existing config or set defaults from the template
    updated_config = {}
    for field, value in CONFIG_TEMPLATE.items():
        if field in existing_config:
            updated_config[field] = existing_config[field]
        else:
            updated_config[field] = value

    # Write the updated config to the config file
    with open(CONFIG_FILE, "w") as config_file:
        yaml.dump(updated_config, config_file)

    os.system("notepad.exe config.yaml")

    messagebox.showinfo("Config File Update", "Please save and close the config file after making the necessary updates.")

    response = messagebox.askyesno("Config File Update", "Restart the application?")
    if response:
        # Restart the app
        python_executable = sys.executable
        script_path = os.path.abspath(sys.argv[0])
        os.execl(python_executable, python_executable, script_path)
    else:
        sys.exit(0)

# Check if config.yaml exists
if not os.path.isfile(CONFIG_FILE):
    update_config_file()

# Load configuration from config.yaml
with open(CONFIG_FILE, "r") as config_file:
    config = yaml.safe_load(config_file)

if not config:
    update_config_file()

# Check if required fields are populated in config.yaml
required_fields = ["org", "branches", "token"]
missing_fields = [field for field in required_fields if field not in config or not config[field]]

# Exclude 'branches' field when it's an empty array
if "branches" in config and isinstance(config["branches"], list) and not config["branches"]:
    missing_fields.remove("branches")

if missing_fields:
    update_config_file()

# Extract configuration variables
branches = config["branches"]
org = config["org"]
token = config["token"]
team_slug = None
if "team_slug" in config:
    team_slug = config["team_slug"]

# Select parent directory
Tk().withdraw()  # Hide the Tkinter main window
clone_directory = askdirectory(title="Select Clone Directory")

if not clone_directory:
    print(f"{YELLOW}Clone directory selection canceled. Exiting the script.{RESET}")
    input("Press any key to exit...")
    sys.exit(0)

# Create the clone directory if it doesn't exist
os.makedirs(clone_directory, exist_ok=True)

# Get the repositories in the team
if team_slug:
    team_repos_url = "https://api.github.com/orgs/{org}/teams/{team_slug}/repos"
    print(f"{BLUE}Cloning all repositories in {team_slug} in {org} organization{RESET}")
else:
    team_repos_url = "https://api.github.com/orgs/{org}/repos"
    print(f"{BLUE}Cloning all repositories in {org} organization{RESET}")
headers = {"Authorization": f"token {token}"}
repos_response = requests.get(team_repos_url.format(org=org, team_slug=team_slug), headers=headers)
repos = repos_response.json()

try:
    # Track cloning status
    success_count = 0
    failure_count = 0

    # Clone each repository for the specified branches or default branch
    for repo in repos:
        repo_name = repo["name"]
        default_branch = repo["default_branch"]
        clone_url = repo["clone_url"]
        cloned = False

        if branches:
            for branch in branches:
                clone_path = os.path.join(clone_directory, f"{repo_name}_{branch}")
                clone_command = f"git clone --branch {branch} {clone_url} {clone_path}"
                exit_code = os.system(clone_command)

                if exit_code == 0:
                    print(f"{GREEN}Cloned repository '{repo_name}' on branch '{branch}' to '{clone_path}'{RESET}")
                    success_count += 1
                    cloned = True
                    break

        if not cloned:
            clone_path = os.path.join(clone_directory, f"{repo_name}_{default_branch}")
            clone_command = f"git clone --branch {default_branch} {clone_url} {clone_path}"
            exit_code = os.system(clone_command)

            if exit_code == 0:
                print(f"{GREEN}Cloned repository '{repo_name}' on default branch '{default_branch}' to '{clone_path}'{RESET}")
                success_count += 1
            else:
                print(f"{RED}Failed to clone repository '{repo_name}' on default branch '{default_branch}'{RESET}")
                failure_count += 1

    # Summary
    total_repos = len(repos)
    print(f"\nCloning completed:")
    print(f"{BLUE}Total repositories found: {total_repos}{RESET}")
    print(f"{GREEN}Successful clones: {success_count}{RESET}")
    print(f"{RED}Failed clones: {failure_count}{RESET}")
except:    
    print(f"{RED}An error occured. Some values in config.yaml may not be properly set.{RESET}")
    
input("Press any key to exit...")
