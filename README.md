# Example Python Project - Quote of the Day

This repository serves as an example to learn how to create a python project. Our project will create a library and command line interface (cli) to get quotes from the [Quotable API](https://api.quotable.io/random). This project is meant for learning and goes over the following major steps

0. Cloning and checkout out a "tagged" version of this repository.
1. Creating and activating a conda virtual environment.
2. Creating our empty python package called `qotd`. This will be a library and a cli application.
3. Creating our `pyproject.toml` and installing our package into our virtual environment. 
4. Completing our python library and testing in a python interactive shell or script.
5. Completing our python cli interface.
6. Creating our `tests` using `pytest`.

## Step 0 - Clone Repository

The first thing that we need to do is clone this repository

1. Open up your terminal!
2. `cd` to where you save your files and folders.
3. `git clone https://github.com/JeremyBYU/project-qotd.git`
4. `cd project-qotd`

We have several versions of this repository. Lets start at the beginning (v1.0.0). Please type the following: `git checkout tags/step0`

The repo should have changed now and you should see the following file directories: 

```
project-qotd
├─ recordings
├─ .gitignore
├─ README.md
└─ LICENSE
```

Now we will `create` and `checkout` a new **branch** to begin working. Please type: `git checkout -b dev`. You now created and switched to the `dev` branch.

## Step 1 - Create conda virtual environment

We now need to create a conda virtual environment to develop our project and install its dependencies in. If you don't have conda installed please follow [these instructions](https://docs.conda.io/en/latest/miniconda.html).  With conda installed, please do the following:

1. `conda create --name quote python=3.10`. Enter `y` is prompted and hit `ENTER` key.
2. `conda activate quote` - Your conda environment should now be activated!

Great you have created a python virtual environment called "quote" that we can use for this project!

Video Walkthrough (visible only in vscode):

<video width="640" controls>
  <source src="./recordings/step1_create_conda_env.mp4" type="video/mp4">
</video> 

## Step 2 - Create `qotd` package

We will now create our `qotd` project. Please do the following

1. Create a folder `src` and inside that folder create another folder named `qotd`.
2. *Inside* the newly created `qotd` folder create a file named `__init__.py`

Your file system should look like this:

```
project-qotd
├─ src
│  └─ qotd
│     └─ __init__.py
├─ recordings
├─ README.md
└─ LICENSE
```

This creates the `qotd` package. There not much in it now but rest assured we will be creating more functionality soon! 

Now that we have a python file, lets tell `vscode` to use our conda virtual environment. Watch the video walkthrough below

Video Walkthrough (visible only in vscode):

<video width="640" height="480" controls>
  <source src="./recordings/step2_vscode_conda.mp4" type="video/mp4">
</video> 

## Step 3 - Create `pyproject.toml` file

We will now create our `pyproject.toml` file that **defines** our package. Inside the `project-qotd` directory create a new file called `pyproject.toml`. Inside the file please type (or copy/paste!) the following

```toml
[project]
name = "qotd"
version = "0.0.1"
description = "A library and cli that retrieves famous quotes from the internet"
authors = [
    {name = "Jeremy Castagno", email="JeremyBYU@gmail.com"}
]
requires-python= ">=3.9"
dependencies = [
]

[build-system]
requires = [
    "setuptools >= 35.0.2",
    "setuptools_scm >= 2.0.0, <3"
]
build-backend = "setuptools.build_meta"

[tool.setuptools.package-data]
qotd = ["*.json"]

```
### Installing our Package

Now lets **install** our package using pip. Inside your terminal please type: `pip install -e .`. This will begin installing our package into our virtual environment! 

### Verifying installation worked

Lets ensure our package is working by doing the following:

1. Inside our terminal (whose working directory should be `project-qotd`) open the interactive `python` terminal. 
2. Now type: `import qotd`

If there are no errors then that means our installation worked! You can exit the python interactive session by typing `exit()` and hit `ENTER`.

Video Walkthrough (visible only in vscode):

<video width="640" height="480" controls>
  <source src="./recordings/step3_pyproject_install.mp4" type="video/mp4">
</video> 


## Step 4 - Create library

### Create files and add `requests` package

Lets begin creating our library! The first thing we should do is create a `lib.py`, `types.py`, `helper.py`, a `cli.py` file inside `src/qotd`. Next create a top level folder called `scripts` and put a file named `run_catalog.py` in it. Your directory should look like this now:

```txt
project-qotd
├─ src
│  └─ qotd
│     ├─ __init__.py
│     ├─ types.py
│     ├─ lib.py
│     ├─ helper.py
│     ├─ data
│     │  └─ default-catalog.json
│     └─ cli.py
├─ scripts
│  └─ run_catalog.py
├─ recordings
├─ README.md
├─ pyproject.toml
└─ LICENSE
```

We will be saving any data we download from the server into a data file called `data/default-catalog.json`. Please put the following in this file:

```json
{
"available_authors": {},
"available_tags": {},
"available_quotes": {}
}
```

Now lets add the [requests](https://requests.readthedocs.io/en/latest/) package as a dependency to our library. **Requests** will allow us to easily communicate with the internet. Update your `pyproject.toml` file:

```toml
...
dependencies = [
    "requests"
]
...
```

Remember, anytime we update `pyproject.toml` means we need to reinstall our software. Open your terminal and type `pip install -e .`. You will see it fetch the `requests` package and install it into our virtual environment.


### Create our library

There is too much to write here! Please just watch the video for this part!

### Build Wheels (Optional)

Now that your library is created you may be interested in distributing it. You can do this by building a *wheel*. Do the following:

1. `pip wheel -w build --no-deps .`

You should now see a file with the **.whl** suffix in the `build` folder. This wheel can be shared with others by uploading to pypi or even in an e-mail. See [here](https://realpython.com/python-wheels/) for more details
## Step 5 - Create CLI

There is too much to write here! Please just watch the video for this part!

After creating the cli don't forget that we need to reinstall our software. Open your terminal and type `pip install -e .`. You can now use your CLI. Type `qotd --help` to see all options and commands.

## Step 6 - Create Tests

We want to use the [pytest]() package to test our library. However, people who install our package (our users) should not need to install pytest! To handle that, we will mark pytest as an *optional* dependency.  

Update your `pyproject.toml` as so:

```toml
[project]
name = "qotd"
version = "0.0.1"
description = "A library and cli that retrieves famous quotes from the internet"
authors = [
    {name = "Jeremy Castagno", email="JeremyBYU@gmail.com"}
]
requires-python= ">=3.9"
dependencies = [
    "requests",
    "click"
]

[project.optional-dependencies]
dev = ["pytest"]

[project.scripts]
qotd = "qotd.cli:cli"

[build-system]
requires = [
    "setuptools >= 35.0.2",
    "setuptools_scm >= 2.0.0, <3"
]
build-backend = "setuptools.build_meta"

[tool.setuptools.package-data]
qotd = ["*.json"]
```

This adds the optional dependency category called `dev`. If we are *developing* this software then we can now install our package as so: `pip install -e ".[dev]"`. Users of our library will not need the `[dev]` tag.

Please watch the full video to see how to write our tests. The final directory structure should look like this:


```txt
project-qotd
├─ tests
│  ├─ test_qotd_types.py
│  ├─ test_qotd_lib.py
│  └─ fixtures
│     └─ single.json
├─ src
│  └─ qotd
│     ├─ __init__.py
│     ├─ types.py
│     ├─ lib.py
│     ├─ helper.py
│     ├─ data
│     │  └─ default-catalog.json
│     └─ cli.py
├─ scripts
│  └─ run_catalog.py
├─ recordings
├─ README.md
├─ pyproject.toml
└─ LICENSE
```

# Switching Tags

The evolution of this repository has been tagged according to steps described above. This means that you can switch to different points in time to the repository

You can switch tags by doing the following:

1. `git reset --hard tags/step1`
2. `git clean -d -x -n`

You can then walk through the history of the repository like so:

1. `git reset --hard tags/step2`

and so on. When you are done, just checkout the last tag

1. `git reset --hard tags/step6.2`

List of all tags:

```bash
$ git tag
step0
step1
step2
step3
step4.1
step4.2
step4.3
step4.4
step5
step6.1
step6.2
```






