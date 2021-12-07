# badge-creator
A quick and simple python library and cli to create project badges

# Usage
### Example 1
The command below uses the default background color and will generate the [![license](/samples/license.png?raw=true "License")](/LICENSE?raw=true) badge as a link to the license
```
python -m badge_creator.cli -f DejaVuSans.ttf license MIT samples/license.png
```

### Example 2
The command below sets the background color and will generate the ![build](/samples/build.png?raw=true "Build Sample") badge
```
python -m badge_creator.cli -f DejaVuSans.ttf -b 00FF00 build 'passing' samples/build.png
```

### Example 3
The command below shows how the gradient and text shadow are effective at showing the content even with lighter colors.  The ![coverage](/samples/coverage.png?raw=true "Coverage Sample") badge is generated in this example

```
python -m badge_creator.cli -f DejaVuSans.ttf -b FFFF00 coverage '90%' samples/coverage.png
```
