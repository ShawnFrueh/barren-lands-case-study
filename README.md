# target-case-study

## Setup (Python 3.7)
Create your ENV and enter it. (I used conda for this.)
- `conda env create -f ./conda_env.yml`
- `conda activate barren_lands`

if using another environment type, make sure it is `python 3.7` and pip install 
the `requirements.txt` file.

### Test (using env)
`python -m pytest -v -s --cov=barren_lands tests`


### Run (using env)
Use `--vis` to display the image result using the default os image viewer.
- `python case_study.py --zones "0 292 399 307"`
- `python case_study.py --zones "48 192 351 207" "48 392 351 407" "120 52 135 547" "260 52 275 547"`
- Use `--gui` to open the interactive GUI application
  - `python case_study.py --gui`
  - `python case_study.py --gui --zones "0 292 399 307"`

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

Connected Components: Information here used to split up the zones into islands
- [Rectangles into islands of connected regions](https://stackoverflow.com/questions/2254697/how-can-i-group-an-array-of-rectangles-into-islands-of-connected-regions)

icon
- https://www.vecteezy.com/vector-art/90874-vector-rolling-hills-flat-icons


####Post code research:
- [js rectangle decomposition](https://github.com/mikolalysenko/rectangle-decomposition)
- [Fewest Rectangles to cover](https://stackoverflow.com/questions/5919298/algorithm-for-finding-the-fewest-rectangles-to-cover-a-set-of-rectangles-without)
- [Great paper by David Eppstein](https://arxiv.org/pdf/0908.3916v1.pdf)
- [Rectangular Decomposition of Binary Images](http://library.utia.cas.cz/separaty/2012/ZOI/suk-rectangular%20decomposition%20of%20binary%20images.pdf)
  - In this paper, it talks about the various methods to tackle this problem and shows there is no "generally best" method. You have to balance between time and memory consumption.
  
 ## Case study conclusion:
 Parsing though this puzzle was quite fun. While I initially attempted as much as I could on my own.
 I did have to reach out to the inter-webs to check out a few ways of solving some steps. Taking a
 quick look as what the web had to offer I came across an [image](https://i.stack.imgur.com/ay5pt.png)
 that helped me determine how I wanted to solve the task at hand. Left->Right->Top->Bottom. This
 helped fill the regions and Initially I though I was done. I had the zones and the list of zones in
 order from least to largest. I wasn't until I was re-reading the synopsis and discovered that I had
 interpreted the outputs incorrectly and that it wasn't the individual zones but rather the 
 individual islands. 
 
 Trying to find the connected pairs of rectangles to create the islands, I came across 
 [this post](https://stackoverflow.com/questions/2254697/how-can-i-group-an-array-of-rectangles-into-islands-of-connected-regions)
 about connected components. I was then able to use the information here to correctly separate the
 different zones into their respective islands. 
 
 How to accelerate and scale this to use in a production environment? I was looking into how I was
 solving the topic and with the amount of looping that was happening I figured they must be a way
 to help parallelize the code and I came across this paper: [GPU-accelerated rectangular 
 decomposition for sound propagation modeling in 2d](https://www.researchgate.net/publication/335740556_GPU-accelerated_rectangular_decomposition_for_sound_propagation_modeling_in_2D)
 the audio visuals for figure 7 are incredible. The code to handle such a task can be found on their
 github links.
 - [Adaptive Boxes](https://github.com/jnfran92/adaptive-boxes)
 - [Adaptive Boxes GPU](https://github.com/jnfran92/adaptive-boxes-gpu)
