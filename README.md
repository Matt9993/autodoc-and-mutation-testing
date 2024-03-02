# Project to showcase mutation testing and documenting
The goal of this simple repo is to showcase 2 libraries that can save time for you
as a developer in the long run and also help you find bugs.
- Mutation testing
- Auto-documenting code


### README content:

- Dependency installation/usage
- Mutation testing (`mutmut`)
- Auto-doc library (`Sphinx`)
- Autodoc-pydantic (sphinx extension)


## The hosted static website
The hosted docs is available [here](http://autodoc-showcase.s3-website-eu-west-1.amazonaws.com) when you are connected to the company VPN.

## Dependency installation/usage
Use the project root as your working directory.

Run `poetry shell` to spawn the poetry shell and activate your virtual environment.

Run `poetry install` to install the project dependencies.

**Poe tasks**

To run the unit tests: `poe unit-test`

To run the test coverage: `poe test-coverage`

To run the mutation tests: `poe mutation`

To run the document generation: `poe auto-doc`
The above will only generate/update the `rst` files in the docs/ folder.
You still need to manually update some things:
- models.rst when you add new pydantic models



## Mutation testing
In every project testing is crucial, and although we can't always set our target at 100% coverage as an
acceptance criteria, but we always have to aim for that. And sometimes as history proved it even 100% coverage
is not enough. Sometimes a really unexpected thing can happen and your program will crash.

And to fill the uncertainty some mutation testing libraries were born.

What are mutation tests?
Mutation tests will detect small modifications (mutations) in the code. Surviving mutations represent subtle 
changes that are undetectable by your tests. These mutants are potential modifications in source code that 
continuous integration checks would miss.

In this project you can experiment with one of these libraries called `mutmut`.
Official Pypi [link](https://pypi.org/project/mutmut/) .

### Usage of `mutmut`
If you check the repo files in the root there is a file called setup.cfg where there are just
a couple of really simple attributes to configure `mutmut`. These can be fine-tuned further when
the situation requires more than the current simple config. For details visit the official doc
linked above.

To run `mutmut` you can go to the root of the project and simply run:
```shell
mutmut run
```
The above command will show you some emojis and the results of all the mutation tests.
To further investigate where you have some so-called mutants to "kill" just run
```shell
mutmut results
```
And this is going to give you a list of error with numbers.
To check and tackle these mutations one-by-one, run the following:
```shell
mutmut show {id of the mutation}
```

To start the mutation tests you can use the `poe mutation` task.


## Generating Docs (Auto-doc library)
For document generation the project is using a python library called `Sphinx`.

### Example project situation
Before anyone is committing anything to a feature branch it is mandatory to
run the following command. For this you have to be in the root of the project.
```shell
sphinx-apidoc -o docs src
```
The above command will generate/update the `rst` files inside the `docs/` folder.
This is necessary when you updated or added something in the source folder.

In case you added a new `Pydantic` model to this project, go to the `docs/models.rst` file
and add a new line to the file based on the other models in the file.

When you updated everything in the doc files, just do the following:
```shell
cd docs/
make clean html
```
This will regenerate the html files for the documentation.
To check if your updates on the docs are as you wanted, just open the `docs/html/index.html`
file in your browser.

For easier usage just run a poe task: `poe auto-doc`


## Autodoc-pydantic
This is an extension package for `sphinx` that gives you extra features to document your
pydantic models in the best possible way.
Official [link](https://pypi.org/project/autodoc-pydantic/).


## Usage of Auto generated docs
Although you can't generate README files based on your docstring with sphinx, but you can
do something much better. There is an option to host the generated `html` docs in Github/Gitlab pages,
 AWS S3, GCS bucket and there is an option to host static websites on Azure as well.

The hosted documentation for this project is available in our S3 bucket, and you can check it out
if you visit the link in `The Hosted static website section` and you are connected to our Infinite Lambda VPN.


## Mutation test libraries comparison
#### `mutmut` Overall mutation trial summary:
 - KILLED: 42
 - SURVIVED: 11
 - TOTAL RUNS: 53

Found 11 Surviving mutants, most of them were log string modifications
and 1 case where the return string value were changed to None.

Ease of use: really easy basically 1 file (setup.cfg). Config can be fine-tuned. 
More info in the official docs.

#### `mutatest` Overall mutation trial summary:
 - DETECTED: 18
 - SURVIVED: 6
 - TOTAL RUNS: 24

Out of the 6 errors, 4 errors are if statements changed to if True in the aws_secrets.py
error handling section. For me these changes doesn't make any sense.

The rest of the errors were None return values changed to True/False.

Ease of use: easy. After installation only 1 command was enough for a base run without any config.
CDM: `mutatest -s src/ -t "pytest" -r 314`

#### `cosmic-ray` Overall mutation trial summary:
 - COMPLETE: 35
 - SURVIVED: 1
 - TOTAL RUNS: 36

With `cosmic-ray` the errors pointed out that maybe it's better
to change the `==` string compare method because it changed it to
`>=` and `<=`. Although I don't think anyone would make this mistake
but it doesn't hurt to use the `__eq__()` instead.

Other than this the only error left is when one of the test cases
removed the `@dataclass` annotation from the Counter class.

Ease of use: local setup needed. A couple of simple steps to run tests.

1.) Create config file
CDM: `cosmic-ray new-config tutorial.toml`

2.) Init context before every run
CDM: `cosmic-ray init cosmic-ray.toml testing.sqlite`

3.) Execute mutation tests
CDM: `cosmic-ray exec cosmic-ray.toml testing.sqlite`

4.) Generate report and open it in browser
CDM: `cr-html testing.sqlite > report.html`
