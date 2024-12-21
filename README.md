# Evolution 

### Task

A Zen garden is an area covered with coarser sand (small pebbles). 
However, it also contains non-movable larger objects such as stones, statues, structures, and plants.
The monk has to adjust the sand in the garden with a rake so that strips of

The strips can only go horizontally or vertically, never diagonally. He always starts at the edge 
of the garden and pulls a straight strip to the other edge or to an obstacle. At the edge - outside the 
garden he can walk as he wishes. But if he comes to an obstacle - a stone or already raked sand - he must
turn around if he has somewhere to go. If he has free directions left and right, it is his business 
where he turns. If he has only one direction free, he turns there. If he has nowhere to turn, it's game over.
A successful game is one in which the monk can rake the whole garden, given the rules, for the maximum possible number of squares.
The output is the coverage of a given garden by the monk's passes.

---

# Classification

The task involves implementing a k-Nearest Neighbors (k-NN) classifier for classifying points in a 2D space. 
The space has dimensions from -5000 to +5000 for both X and Y coordinates. There are four classes
for points in the space: red (R), green (G), blue (B), and purple (P). Initially, each class has 5 points 
with predefined coordinates, for a total of 20 points.

### Task Overview:

**Initial Points:** 
Each class (R, G, B, P) has 5 initial points located at specific coordinates.

**Classify Function:**
Project implement a classify(int X, int Y, int k) function. This function classifies a new point 
at coordinates (X, Y) based on the k-NN algorithm using the specified k value (which can be 1, 3, 7, or 15). 
The function should then add this new point to the 2D space and return the assigned class.

**k-NN Algorithm:**
The classification is based on the k-NN algorithm, where the class of a new point is determined by the majority 
class of its nearest neighbors (based on Euclidean distance). The k value determines how many nearest neighbors are considered.

**Random Point Generation:**
Project will generate 40,000 new points (10,000 from each class). 
Each class has a 99% probability of points appearing in a specific region of the 2D space:
Red (R): 99% chance for X < +500 and Y < +500.
Green (G): 99% chance for X > -500 and Y < +500.
Blue (B): 99% chance for X < +500 and Y > -500.
Purple (P): 99% chance for X > -500 and Y > -500.
The remaining 1% of points can appear anywhere in the 2D space, ensuring variability.

**Accuracy Evaluation:**
After classifying each generated point, it compare the returned class 
to the actual class of the generated point to evaluate the classifier’s accuracy.

**Visualization:**
For each of the four experiments (with k = 1, 3, 7, and 15), it will visualize
the classification results by coloring the entire 2D space. The regions of the 
space will be colored according to the class assigned by the classifier,
allowing it to visually assess the classifier's performance.

**Experiment:** 
Project will conduct four experiments, one for each value of k, 
and for each experiment, the generated points will be the same. 

---

# Neuronal network

### Task for part one:

The goal of this project is to develop a neural network to perform a regression on a dataset 
of housing in California. The goal is to predict the median house price for California counties
based on several data points such as population, income, and location. The dataset contains 20,640 cases with 
8 data points, such as median income, property age, and average occupancy, as well as a target value,
which is the median house price.

### Task for part two:

The task at hand involves implementing the backpropagation algorithm from scratch and using 
it to train a simple feedforward neural network (also known as a multilayer perceptron, MLP). 
Backpropagation is a crucial part of the training process for neural networks, enabling the model 
to learn by minimizing the error between predicted and actual outputs.
This implementation will require creating both forward propagation (to compute the output of the network) 
and backpropagation (to calculate gradients and update weights) then test the algorithm by training 
a neural network on a simple dataset.
