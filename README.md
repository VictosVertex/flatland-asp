# Flatland ASP

**Flatland ASP** deals with the application of Answer Set Programming techniques to the [Flatland](https://www.flatland-association.org/) environment.

Its first goal is to provide a short introduction to Flatland as well as to Answer Set Programming, more precisely [Clingo](https://potassco.org/clingo/), with the help of documentation and examples.

The second and more exciting goal is to explore various ASP instantiations and encodings of the Flatland environment in order to find solutions to the problems Flatland tries to help to solve.

For any information that goes beyond this README, please visit the [FlatlandASP Wiki](https://github.com/VictosVertex/flatland-asp/wiki) or refer to the [Link section](#links)

<details>

<summary>Table of Contents</summary>

1. [Getting Started](#getting-started)
   1. [Prerequisites](#prerequisites)
   1. [Installation](#installation)
1. [General Project Structure](#general-project-structure)
1. [Links](#links)

</details>

## Getting started

To get this project up and running, just follow these simple steps.

### Prerequisites

In order to get FlatlandASP up and running the only prerequisite is [Python](https://www.python.org/). To avoid conflicts with Flatland it is currently recommended to use **Python 3.10**.

### Installation

1. Clone this repository

```sh
git clone https://github.com/VictosVertex/flatland-asp.git
```

2. Create a new python virtual environment (or use an existing one)

```sh
py -m venv my_new_python_environment
```

3. Activate the virtual environment
   <details>
   <summary>Windows</summary>

   cmd.exe

   ```sh
   source my_new_python_environment/Scripts/activate.bat
   ```

   PowerShell

   ```sh
   source my_new_python_environment/Scripts/activate.ps1
   ```

   </details>
   <details>
   <summary>Linux</summary>

   (depending on distribution):

   bash

   ```sh
   source my_new_python_environment/bin/activate
   ```

4. Go into cloned repository directory
5. Install the project as an editable package

```sh
pip install -e .
```

The project is now ready to be used in any project using the python virtual environment.

[back to top](#flatland-asp)

## General Project Structure

- `data/`
  - `data/encodings/` ASP encodings
  - `data/environments/` Environment data (`.json`) and environments (`.pkl`)
- `examples/` Examples for Flatland and ASP (Clingo)
- `src/flatlandasp`
  - `src/flatlandasp/core/flatland` Flatland related classes, schemas, mappings, static maps, etc.
  - `src/flatlandasp/core/asp` ASP/Clingo related instance descriptions, generators, etc.
  - `src/flatlandasp/core/utils` Utility functions for files, images, etc.
  - `src/flatlandasp/features/` Modular features building on `core`/each other, `API endpoints`

## Links

Useful links for more information on Flatland and Clingo

- Flatland
  - Official Flatland website: https://www.flatland-association.org/
  - Flatland on pypi: https://pypi.org/project/flatland-rl/
  - Flatland on github: https://github.com/flatland-association/flatland-rl
- Clingo
  - Clingo: https://potassco.org/clingo/
  - Potassco Guide on github: https://github.com/potassco/guide/releases/

[back to top](#flatland-asp)
