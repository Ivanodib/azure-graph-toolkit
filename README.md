

<a id="readme-top"></a>



<!-- PROJECT LOGO -->
<br />
<!--<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
     <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>-->

  <h1 align="center">azure-graph-toolkit</h1>

  <p align="center">
    A Python library to manage Azure AD (Entra ID) user groups easily through Graph API.
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
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
There are many great Azure libraries available on GitHub; however, I didn't find one that really suited my needs, so I created this one to simplify and automate daily sysadmin tasks.

<!-- Here's why:
* Automate Sysadmin daily task
* Get user and groups informations. -->

<br>
<br>


<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

1. Python >= 3.4
2. Azure AD App Registration with the following role assigned *(App delegation)*:


| Least privilege role | Type | Description |
| --- | --- | --- |
| `GroupMember.ReadWrite.All` | Application | To manage user membership groups. |
| `GroupMember.Read.All` | Application | List all the groups available, excluding dynamic distribution groups. |
| `User.Read.All` | Application | To get user informations. |

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

 **Error handling**<br>
 This library handles exceptions for you. Just verify the presence of the 'error' key in the JSON response: 
```python

result = graph_utils.remove_user_from_group('mario.rossi@domain.com', 'block-usb-group', access_token)

if 'error' in result:
  doSomething()
   
 ```
<br>

  Example Output
 ```python
 {'status_code': 204, 'message': 'Success. User mario.rossi@domain.com added to AAD group block-usb-group.'}
 
 ```
 ```python
 {'status_code': 200, 'error': 'No AAD group name that contains block-usb-group found. Try another name.'}
 ```


<!--_For more examples, please refer to the [Documentation](https://example.com)_ -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Add orchestrator to change user membership temporarily
- [ ] Add module to manage user credentials
- [ ] Add module to manage Entra ID registered devices
- [ ] Add module to manage Intune MDM joined devices

<!-- See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues). -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing
Any contributions you make are **greatly appreciated**.

<br>



<!-- CONTACT -->
## Contact
Ivano Dibenedetto - [@Linkedin](https://www.linkedin.com/in/ivano-dibenedetto-b526ab188/) - ivano.dibenedetto7@gmail.com

Project Link: [https://github.com/Ivanodib/azure-graph-helper](https://github.com/Ivanodib/azure-graph-helper)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
