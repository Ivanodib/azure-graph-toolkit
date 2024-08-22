<!--<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
     <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>-->

  <h1 align="center">azure-graph-toolkit</h1>


<div align="center">
  
[![Unit test](https://github.com/Ivanodib/azure-graph-toolkit/actions/workflows/unittest-pipeline.yml/badge.svg)](https://github.com/Ivanodib/azure-graph-toolkit/actions/workflows/unittest-pipeline.yml) [![Coverage Status](https://coveralls.io/repos/github/Ivanodib/azure-graph-toolkit/badge.svg?&kill_cache=1)](https://coveralls.io/github/Ivanodib/azure-graph-toolkit)  [![Maintainability](https://api.codeclimate.com/v1/badges/1936009e913846781090/maintainability)](https://codeclimate.com/github/Ivanodib/azure-graph-toolkit/maintainability)  [![Deployment](https://github.com/Ivanodib/azure-graph-toolkit/actions/workflows/deployment-pipeline.yml/badge.svg)](https://github.com/Ivanodib/azure-graph-toolkit/actions/workflows/deployment-pipeline.yml) ![PyPI - Version](https://img.shields.io/pypi/v/azure-graph-toolkit) 

</div>

<div align="center">
  
[![Downloads](https://static.pepy.tech/badge/azure-graph-toolkit)](https://pepy.tech/project/azure-graph-toolkit)
[![Downloads](https://static.pepy.tech/badge/azure-graph-toolkit/month)](https://pepy.tech/project/azure-graph-toolkit)

</div>


  <p align="center">
    Lightweight python library for easily managing Azure AD (Entra ID) users and groups through the Graph API.
    <br />
    <a href=https://github.com/Ivanodib/azure-graph-toolkit><strong>Explore the docs (work in progress)»</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/Ivanodib/azure-graph-toolkit/issues">Report Bug</a>
    ·
    <a href="https://github.com/Ivanodib/azure-graph-toolkit/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
There are many great Azure libraries available on GitHub; however, I didn't find one that really suited my needs, so I created this one to simplify and automate daily tasks.

Features:
* Add user to AAD group
* Remove user from AAD group
* Check if user is member of a group
* List all user membership groups
* Reset user password
* Disable/enable user
* Revoke user session tokens

<!-- Here's why:
* Automate Sysadmin daily task
* Get user and groups informations. -->

<br>
<br>


<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

1. Python >= 3.8
2. Azure AD App Registration with the following role assigned:


| Least privilege role | Delegation type | Description |
| --- | --- | --- |
| `GroupMember.ReadWrite.All` | Application | To manage user membership groups. |
| `GroupMember.Read.All` | Application | List all the groups available. |
| `User.ReadWrite.All`, `User Administrator role`  | Application | To change user password. |
| `User.ManageIdentities.All`, `User.EnableDisableAccount.All` | Application | To disable/enable user. |
| `User.RevokeSessions.All` | Application | To revoke user session tokens. |

<br>

### Installation

1. Install azure-graph-toolkit library from PyPi 
   ```sh
   pip install azure-graph-toolkit
    ```
2. Profit 😁

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
### Usage

Import library modules

```python
from azure_graph_toolkit import graph_auth, graph_utils
   ```

App authentication and authorization. Once get the access token is possible to interact with Azure AD Graph API.
```python

tenant_id = '<tenant Id>'
client_id = '<client (App) Id>'
client_secret = '<client secret>'

access_token = graph_auth.get_access_token(tenant_id, client_id, client_secret)
   ```

<br>


**Add user to AAD group:**
```python

result = graph_utils.add_user_to_group('mario.rossi@domain.com', 'block-usb-group', access_token)

print(result)

 ```

<br>

 **Remove user from AAD group:**
```python

result = graph_utils.remove_user_from_group('mario.rossi@domain.com', 'block-usb-group', access_token)

print(result)
 ```
 <br>

 **Disable user:**
```python

result = graph_utils.set_user_account_status('mario.rossi@domain.com', enable_account=False, access_token)

print(result)
 ```
 <br>

  **Revoke user sessions:**
```python

result = graph_utils.user_revoke_sessions('mario.rossi@domain.com', access_token)

print(result)
 ```
 <br>



  Example Output
 ```python
 {'status_code': 204, 'message': 'Success. User mario.rossi@domain.com added to AAD group block-usb-group.'}
 
 ```
 ```python
 {'status_code': 404, 'message': 'No AAD group with a name containing \'block-usb-group\' was found. Please try another group name.'}
 ```


<!--_For more examples, please refer to the [Documentation](https://example.com)_ -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] List user MFA status
- [ ] List user's owned devices
- [ ] List devices compliance status
- [ ] Add device to group
- [ ] Remove device from group
- [ ] Create and delete users
- [ ] Create and delete groups

<!-- See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues). -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact
Ivano Dibenedetto - [@Linkedin](https://www.linkedin.com/in/ivano-dibenedetto-b526ab188/) - ivano.dibenedetto7@gmail.com

Project Link: [https://github.com/Ivanodib/azure-graph-toolkit](https://github.com/Ivanodib/azure-graph-toolkit)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
