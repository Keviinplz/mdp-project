# MDP Project

Repository that contains all the files for the MDP project.

Members:
-    Nicolas Olguin
-    Juan Quilapi
-    Kevin Pinochet

## How to development

This repository use `poetry` as package manager, [you have to install it first](https://python-poetry.org/docs/master/#installing-with-the-official-installer).

If you already have `poetry` installed, you can run `poetry install` to install all dependencies.

## Folder Structure

The repository has the following folder structure:
```
├── data             <--- Data that will use to make predictions, DO NOT UPLOAD TO GITHUB
│   ├── production   
│   └── testing
├── src              <--- source code for map-reduce framework
│   ├── mappers
│   └── reducers
├── tests            <--- code testing
├── main.py          <--- main file for map-reduce framework, with --mapper and --reducer flags to specify which mapper and reducer to use
└── main.ipynb       <--- jupyter notebook to interact with data.
```
