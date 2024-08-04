
<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!--[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
     <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h1 align="center">azure-graph-helper</h1>

  <p align="center">
    A Python library to manage Azure AD (Entra ID) user groups easily through Graph API.
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
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
There are many great azure libraries available on GitHub; however, I didn't find one that really suited my needs so I created this enhanced one.

Here's why:
* Help IT foolks to add/remove user from Azure AD security groups. 
* Get user and groups informations.

<br>
<br>


<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

1. Python version >= 3.8
2. Azure AD App Registration with the following role assigned *(App delegation)*:


| Role | Description |
| --- | --- |
| `Groups.ReadWrite.All` | To add/remove user from Azure AD Group |
| `User.Read.All` | To read user information |

<br>

### Installation

1. Install azure-graph-helper library from PyPi 
   ```sh
    pip install azure-graph-helper
    ```
2. Ready to use :)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Import library modules

```python
   from azure-graph-helper import app_auth
   from azure-graph-helper import azure_utils
   ```

App authentication and authorization. Once get the access token is possible to interact with Azure AD Graph API.
```python

   tenant_id = '<tenant Id>'
   client_id = '<client (App) Id>'
   client_secret = '<client secret>'

   access_token = app_auth.get_access_token(tenant_id, client_id, client_secret)
   ```

<br>
<br>

**Example - Add user to AAD group:**
```python

   result = azure_utils.add_user_to_group('mario.rossi@domain.com',
                                          'block-usb-group',
                                           access_token)
   print(result)


 ```

<br><br>

 **Example - Remove user from group:**
```python

   result = azure_utils.remove_user_from_group('mario.rossi@domain.com',
                                          'block-usb-group',
                                           access_token)
   print(result)
 ```
 <br><br>

 **Error handling**<br>
 You can check 'error' key presence in JSON response: 
```python

   result = azure_utils.remove_user_from_group('mario.rossi@domain.com',
                                          'block-usb-group',
                                           access_token)

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

- [ ] Add an orchestrator to move users into groups temporarily
- [ ] Add module to reset user credential and MFA methods
- [ ] Add module to block/delete user
- [ ] Add module to manage Entra ID devices
- [ ] Add Intune modules to manage MDM joined devices

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
