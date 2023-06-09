# **GitBatchClone**

## **What is this?**

This is a tool that automates the cloning of specific branches of all repositories within a GitHub organization or team.

## **Generate PAT**

Generate a personal access token (classic) with the necessary permissions to the organization. The `read:org` scope should be enough.

## **Update config file**

First time running the tool, a `config.yaml` file will be generated. Update the fields in the file:

- `branches`: List of branches to be cloned. If just the main branch is required from each repo, leave as an empty array. Only the first branch of the repository if present will be cloned. If no branches in the repository match any specified in this field, the main branch will be cloned
- `org`: Organization name
- `token`: GitHub personal access token
- `team_slug`: Team name. If no team is provided, then all repositories of the organization will be cloned. This is the only optional field

## **Running the tool**

Create a parent folder for the repositories to be cloned to and run the tool. A file dialogue window will appear. Select the newly created folder and click OK. All the repositories will be cloned to the selected folder.

### **From the binary or executable**

Download the latest [release](https://github.com/viruj96/GitBatchClone/releases/latest) for the target platform and run it.

### **From the terminal**

Download and install [python](https://www.python.org/downloads/)

> [Optional] Create a virtual environment:
>
> *Linux*:
>
> ```bash
> python -m venv venv
> source ./venv/bin/activate
> ```
>
> *Windows*:
>
> ```cmd
> python -m venv venv
> .\venv\Scripts\activate
> ```
>
> ---

Install all the required modules in the requirements.txt file and run the script

```bash
pip install -r ./requirements.txt
python ./main.py
```

## **Troubleshoot**

If the script fails due to an SSL certificate error, add the GitHub SSL certificate to the trusted certificate store:

- Navigate to [GitHub](https://github.com)
- Click on the padlock icon in the address bar and view the certificate (this will vary depending on the browser used)
- Download or export the certificate (again this will depend on the browser). A `.cer` or `.pem` file should be saved
- Add the file to the trusted store:
  - *Linux* (the trusted certificate store is usually managed by the OpenSSL library and are stored in `/etc/ssl/certs/`):
    - Copy the GitHub SSL certificate to `/usr/local/share/ca-certificates/`

	```bash
	sudo cp github.cer /usr/local/share/ca-certificates/
	```

    - Update the trusted certificate store

	```bash
	sudo update-ca-certificates
	```

  - *Windows*:
    - Search for `certmgr.msc` to open the Certificate Manager

	![Certificate Manager Window](https://adamtheautomator.com/wp-content/uploads/2020/06/Untitled-57.png)

    - Right click on the `Trusted Root Certification Authorities` folder and choose `All Tasks` > `Import`
    - Follow the import wizard to select the SSL certificate downloaded earlier
