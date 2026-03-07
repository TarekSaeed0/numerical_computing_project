<div align="center">
<a href="https://git.io/typing-svg">
 <img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=900&size=40&pause=1000&color=4493F8&width=650&lines=Numerical+Computing+Project" alt="Typing SVG" />
</a>

<p align="center">A full-stack application for numerical analysis</p>

<div align="center">
<a href="https://github.com/TarekSaeed0/numerical-computing-project/graphs/contributors">
  <picture>
    <source media="(prefers-color-scheme: dark)"  srcset="https://img.shields.io/github/contributors/TarekSaeed0/numerical-computing-project?style=for-the-badge&labelColor=%23151b23&color=%234493f8">
    <source media="(prefers-color-scheme: light)" srcset="https://img.shields.io/github/contributors/TarekSaeed0/numerical-computing-project?style=for-the-badge&labelColor=%23f6f8fa&color=%230969da">
    <img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/TarekSaeed0/numerical-computing-project?style=for-the-badge&labelColor=%23151b23&color=%234493f8">
  </picture>
</a>
<a href="https://github.com/TarekSaeed0/numerical-computing-project/pulse">
  <picture>
    <source media="(prefers-color-scheme: dark)"  srcset="https://img.shields.io/github/last-commit/TarekSaeed0/numerical-computing-project?style=for-the-badge&labelColor=%23151b23&color=%234493f8">
    <source media="(prefers-color-scheme: light)" srcset="https://img.shields.io/github/last-commit/TarekSaeed0/numerical-computing-project?style=for-the-badge&labelColor=%23f6f8fa&color=%230969da">
    <img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/TarekSaeed0/numerical-computing-project?style=for-the-badge&labelColor=%23151b23&color=%234493f8">
  </picture>
</a>
<a href="https://github.com/TarekSaeed0/numerical-computing-project/stargazers">
  <picture>
    <source media="(prefers-color-scheme: dark)"  srcset="https://img.shields.io/github/stars/TarekSaeed0/numerical-computing-project?style=for-the-badge&labelColor=%23151b23&color=%234493f8">
    <source media="(prefers-color-scheme: light)" srcset="https://img.shields.io/github/stars/TarekSaeed0/numerical-computing-project?style=for-the-badge&labelColor=%23f6f8fa&color=%230969da">
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/TarekSaeed0/numerical-computing-project?style=for-the-badge&labelColor=%23151b23&color=%234493f8">
  </picture>
    </a>
</div>

</div>

## Features

- Solving systems of simultaneous linear equations
- Solving non-linear equations
- Various numerical methods to use and compare
- Setting a precision for the calculations to be done in
- Step by step solution

## Download

| ![Windows](https://img.shields.io/badge/Windows-0078D4?logo=windows&logoColor=white&style=for-the-badge)                                                                    | ![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white&style=for-the-badge)                                                                        | ![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black&style=for-the-badge)                                                                      |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Download](https://github.com/TarekSaeed0/numerical_computing_project/releases/download/numerical_computing_project-v0.1.0/numerical_computing_project_0.1.0_x64_en-US.msi) | [Download](https://github.com/TarekSaeed0/numerical_computing_project/releases/download/numerical_computing_project-v0.1.0/numerical_computing_project_0.1.0_aarch64.dmg) | [Download](https://github.com/TarekSaeed0/numerical_computing_project/releases/download/numerical_computing_project-v0.1.0/numerical_computing_project_0.1.0_amd64.deb) |

See [releases](https://github.com/TarekSaeed0/numerical_computing_project/releases) for all available installers

## Build

### Dependencies

- [Python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Node.js](https://nodejs.org/en/download)
- [Rust](https://rust-lang.org/tools/install/)
- [Tauri](https://v2.tauri.app/start/prerequisites/)

Run the following to create a virtual environment:

```sh
python -m venv venv
```

Then, activate the environment, depending on your shell the command differs, but for example, in Bash:

```bash
source venv/bin/activate
```

and in Powershell:

```ps1
PS C:\> venv\Scripts\Activate.ps1
```

Install the dependencies for the backend:

```sh
pip install -r backend/requirements.txt
```

Finally, build the Tauri applications

```sh
cd frontend
npm run tauri build
```
