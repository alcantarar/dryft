# how to generate html API documentation using pdoc3

1. Using anaconda prompt, activate dryft environment per repository README.
2. Check that pdoc3 is installed: `pip install pdoc3`
3. Navigate to repository locally: `cd path/to/dryft`
4. Use pdoc3: `python -m pdoc --html dryft`

Html files should be located in a new folder called 'html'. Pdoc3 page is [here](https://pdoc3.github.io/pdoc)