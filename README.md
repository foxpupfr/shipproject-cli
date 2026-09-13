# shipproject-cli
A CLI application to manage things for a imaginary ship transport company ( School Project )

## Dependencies
- It was made `python 3.14.7` and should run on most `python3` versions
- It needs the following modules `datetime`, `time`, `os`, `mysql.connector`
- It mainly operates on `mysql.connector` which is an extrenal module

## Setup
- Make sure you have `mysql.connector` and `python3` installed
- On Arch Linux or Arch based distros

```
sudo pacman -S python-mysql-connector   
```

```
sudo pacman -S python   
```

- On Windows

```
Download and install Python 3 from https://www.python.org/downloads/
(make sure to check "Add Python to PATH" during installation)
```

```
pip install mysql-connector-python  
```

- Then clone the repo and run it 

```
git clone https://github.com/foxpupfr/shipproject.git
cd shipproject
python3 shipproject.py
```

