# Projects_v2

A repository with 3 branches:

- `main`: A branch that includes the code for the Graduation Thesis.
- `SoftEng`: A branch for **Software Engineering** course in VNUHCM_ITUS.
- `vnuhcm-itus`: A branch for all the resources of **Faculty of Information Technology, VNUHCM - University of Science**.

## Branch `main`

### Introduction

This is a branch for all codes in the Graduation Thesis for Tuan Anh Bui Le, a senior student from the Faculty of
Information Technology - Vietnam National University of Ho Chi Minh City, University of Science.

### Project Structure

```
.
└── projects_v2/
    ├── .github/
    │   ├── ISSUE_TEMPLATE/ # All templates for issues
    │   ├── workflows/ # All workflows for Github Actions
    │   └── bitbucket-pipelines.yml # Bitbucket Pipelines configuration file
    │   └── CODE_OF_CONDUCT.md # Code of Conduct file
    │   └── CONTRIBUTING.md # Contributing file
    │   └── dependabot.yml # Dependabot configuration file
    ├── app/
    │   ├── aws/ # All files for the webapp
    │   ├── includes/ # All files for the states management
    │   └── scripts/ # All files for the automation scripts
    ├── assets/ # All files for references (not used for Graduation Thesis)
    │   ├── else/
    │   ├── THPTQG/
    │   ├── python-reviewer-anthony/
    ├── .gitignore # Git ignore file
    ├── LICENSE # License file
    └── Readme.md # This file
```

### Notices

Before working with this repository, please make sure that you have installed all the
dependencies with latest versions. To check if anything is not working,
run this script **at the root folder of this repository**:

```bash
bash app/scripts/dependencies.sh
```
