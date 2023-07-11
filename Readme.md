# Projects_v2

A repository with 4 branches:

- `main`: A branch for **2048** (in `client` folder), used for building a React web application on Github Pages. Also include the code for the Graduation Thesis.
- `SoftEng`: A branch for **Software Engineering** course in VNUHCM_ITUS.
- `gh-pages`: A branch for **2048**, automatically used for the results of Github Actions.
- `vnuhcm-itus`: A branch for all the resources of **Faculty of Information Technology, VNUHCM - University of Science**.

## Branch `main`

### Introduction

This is a repository for all codes in the Graduation Thesis for Tuan Anh Bui Le, a senior student from the Faculty of
Information Technology - Vietnam National University of Ho Chi Minh City, University of Science.

### Project Structure

```
.
└── projects_v2/
    ├── app/
    │   ├── aws/ # All files for the webapp
    │   ├── includes/ # All files for the states management
    │   └── scripts/ # All files for the automation scripts
    ├── assets/ # All files for references
    │   ├── fullstack/
    │   ├── infra/
    │   ├── k8s/
    │   ├── karpenter/
    │   ├── mocks/
    │   └── terraform/
    ├── client # All files for 2048 game
    ├── .gitignore # Git ignore file
    ├── bitbucket_pipelines.yml # Bitbucket Pipelines configuration
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
