# Fanduel Optimizer

Fanduel Optimizer is a Python implementation of the knapsack problem using Fandual players and salaries. It is designed to fill the standard lineup of QB, RB, RB, WR, WR, WR, TE, FLEX, and D.

Example output:
```bash
QB: Mahomes, Patrick
RB1: Gibson, Antonio
RB2: Ekeler, Austin
WR1: Samuel, Deebo
WR2: Robinson, Allen
WR3: Hill, Tyreek
TE: Hockenson, T.J.
FLEX: Montgomery, David
DEF: Detroit
Total Points: 128.6
Total Cost: 60000.0
```

## Installation

[Python-MIP](https://python-mip.readthedocs.io/en/latest/) is the only requirement for executing the optimization solver. It automatically installs COIN-OR to solve optimization problems.
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Python-MIP like this:

```bash
pip install mip
```

To use Get_Player_Data.py you must install Beautiful Soup which is a Python package to scrape website data

```bash
pip install beautifulsoup4
```

Alternatively, install the required packages from the requirements.txt file
```bash
pip install requirements.txt
```

## Usage

Use Get_player_Data.py to automatically pull salaries and projected points from [www.footballdiehards.com](https://www.footballdiehards.com/fantasyfootball/dailygames/FanDuel-Salary-data.cfm). This must be performed every new week the optimizer is used.

```
python Get_Player_Data.py
```

If pulling data using Get_Player_Data.py, you will need to manually delete players from the file Fanduel_Players.csv who aren't available for your contest including (Name, Salary, and Points).  
  
Next, simply run the Fanduel_Optimer.py script.

```
python Fanduel_Optimizer.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
MIT License

Copyright (c) 2020 James McKenna

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
