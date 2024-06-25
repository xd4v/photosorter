
# About this

This scripts will reorganise all files placed in the `input` folder, such as

```
.
├── README.md
├── files
│   └── input
│       ├── Screenshot 2024-05-15 at 11.23.39 AM.png
│       ├── image.png
│       ├── test
│       │   └── file3.png
│       └── test1
│           ├── file1.pdf
│           └── file2.pdf
├── history.json
├── requirements.txt
└── script.py
```

to something sorted by creation date, so it's easy to find back files: 

```
.
├── README.md
├── files
│   ├── input
│   │   ├── test
│   │   └── test1
│   └── output
│       ├── 2024-05-07
│       │   ├── file1.pdf
│       │   └── file2.pdf
│       ├── 2024-05-14
│       │   └── image.png
│       ├── 2024-05-15
│       │   └── Screenshot 2024-05-15 at 11.23.39 AM.png
│       └── 2024-05-17
│           └── file3.png
├── history.json
├── requirements.txt
└── script.py
```


In my case, I use the script to sort the (hundreds) photos I take.
It's _much_ easier to skim through stuff this way, I can then simply add a some
more information to the "date folder", eg. a place or an event, making sure to
keep the date first so folder are properly displayed in a chronologic order on
my computer.


# Install

Clone this repo and 

```
python script.py
```

# Revert a rename

Simply swap the `revert` in `run()` from `script.py`.

```python

# will place all files from input folder to output folder based on creation date
run(revert=False)


# will undo last changes
run(revert=True)
```
