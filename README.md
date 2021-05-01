# target-case-study

## Setup
Create your ENV and enter it.
`conda env create -f ./conda_env.yml`

### Test (using env)
`python -m pytest -v -s --cov=barren_lands tests`


### Run (using env)
Use `--vis` to display the image result
- `python case_study.py "0 292 399 307" --vis`
- `python case_study.py "48 192 351 207" "48 392 351 407" "120 52 135 547" "260 52 275 547" --vis`


## Barren Land Analysis
```text
You have a farm of 400m by 600m where coordinates of the field are from (0, 0) to (399, 599). 
A portion of the farm is barren, and all the barren land is in the form of rectangles. Due to these rectangles of barren land, the remaining area of fertile land is in no particular shape. An area of fertile land is defined as the largest area of land that is not covered by any of the rectangles of barren land. 
Read input from STDIN. Print output to STDOUT 

Input:
You are given a set of rectangles that contain the barren land. These rectangles are defined in a string, which consists of four integers separated by single spaces, with no additional spaces in the string. The first two integers are the coordinates of the bottom left corner in the given rectangle, and the last two integers are the coordinates of the top right corner. 

Output:
Output all the fertile land area in square meters, sorted from smallest area to greatest, separated by a space. 

Sample Input : {"0 292 399 307"}
Sample Output: 116800  116800

Sample Input : {"48 192 351 207", "48 392 351 407", "120 52 135 547", "260 52 275 547"} 
Sample Output: 22816 192608
```

## References
####information gathered during the creation of the code:
The images here helped guide me to attempt filling in zones, `left`>`right`>`top`>`bottom` until they all got filled.
- [Minimum number of rectangles](https://stackoverflow.com/questions/20220215/minimum-number-of-rectangles-in-shape-made-from-rectangles)

Zone class: (Reassuring my math)
- [Point within bounding box.](https://stackoverflow.com/questions/18295825/determine-if-point-is-within-bounding-box)

icon
- https://www.vecteezy.com/vector-art/90874-vector-rolling-hills-flat-icons


####Post code research:
- [js rectangle decomposition](https://github.com/mikolalysenko/rectangle-decomposition)
- [Fewest Rectangles to cover](https://stackoverflow.com/questions/5919298/algorithm-for-finding-the-fewest-rectangles-to-cover-a-set-of-rectangles-without)
- [Great paper by David Eppstein](https://arxiv.org/pdf/0908.3916v1.pdf)
- [Rectangular Decomposition of Binary Images](http://library.utia.cas.cz/separaty/2012/ZOI/suk-rectangular%20decomposition%20of%20binary%20images.pdf)
  - In this paper, it talks about the various methods to tackle this problem and shows there is no "generally best" method. You have to balance between time and memory consumption.
  
 ## Case study conclusion:
 