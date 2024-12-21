import numpy as np
import matplotlib.pyplot as plt
from collections import Counter,defaultdict

class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.startColor = color
        self.clasColor=color


class DynamicGrid:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.grid = defaultdict(list)

    def _get_cell_coords(self, x, y):
        return (int(x // self.cell_size), int(y // self.cell_size))

    def add_point(self, point):
        cell_coords = self._get_cell_coords(point.x, point.y)
        self.grid[cell_coords].append(point)

    def get_neighbors(self, x, y, k):
        cell_coords = self._get_cell_coords(x, y)
        neighbors = []

        # area 3x3
        for i in range(-1, 2):
            for j in range(-1, 2):
                check_cell = (cell_coords[0] + i, cell_coords[1] + j)
                neighbors.extend(self.grid[check_cell])

        # We sort the neighbors by distance and select the first k
        neighbors.sort(key=lambda p: np.sqrt((p.x - x) ** 2 + (p.y - y) ** 2))
        return neighbors[:k]

def initialize_points():
    initial_points = {
        'R': [[-4500, -4400], [-4100, -3000], [-1800, -2400], [-2500, -3400], [-2000, -1400]],
        'G': [[4500, -4400], [4100, -3000], [1800, -2400], [2500, -3400], [2000, -1400]],
        'B': [[-4500, 4400], [-4100, 3000], [-1800, 2400], [-2500, 3400], [-2000, 1400]],
        'P': [[4500, 4400], [4100, 3000], [1800, 2400], [2500, 3400], [2000, 1400]],
    }

    points = []

    for color, coords in initial_points.items():
        for coord in coords:
            point = Point(coord[0], coord[1], color)
            points.append(point)

    return points


def generate_new_point(current_class):
    if current_class == 'R':
        x = np.random.uniform(-5000, 500) if np.random.rand() < 0.99 else np.random.uniform(-5000, 5000)
        y = np.random.uniform(-5000, 500) if np.random.rand() < 0.99 else np.random.uniform(-5000, 5000)
    elif current_class == 'G':
        x = np.random.uniform(-500, 5000) if np.random.rand() < 0.99 else np.random.uniform(-5000, 5000)
        y = np.random.uniform(-5000, 500) if np.random.rand() < 0.99 else np.random.uniform(-5000, 5000)
    elif current_class == 'B':
        x = np.random.uniform(-5000, 500) if np.random.rand() < 0.99 else np.random.uniform(-5000, 5000)
        y = np.random.uniform(-500, 5000) if np.random.rand() < 0.99 else np.random.uniform(-5000, 5000)
    elif current_class == 'P':
        x = np.random.uniform(-500, 5000) if np.random.rand() < 0.99 else np.random.uniform(-5000, 5000)
        y = np.random.uniform(-500, 5000) if np.random.rand() < 0.99 else np.random.uniform(-5000, 5000)

    return Point(x, y, current_class)

# def euclidianDistance(p1, p2):
#     return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

# def classify(new_point, points,k):
#     distances = []
#     for point in points:
#         distance=euclidianDistance(point,new_point)
#         distances.append((distance, point.clasColor))
#
#     distances.sort(key=lambda x: x[0])
#
#     neighbors = distances[:k]
#     neighbor_colors = [neighbor[1] for neighbor in neighbors]
#     most_common_color = Counter(neighbor_colors).most_common(1)[0][0]
#
#     return most_common_color
def classify(new_point, grid, k):
    cell_coords = grid._get_cell_coords(new_point.x, new_point.y)
    neighbors = []

    # area 3x3
    for i in range(-1, 2):
        for j in range(-1, 2):
            check_cell = (cell_coords[0] + i, cell_coords[1] + j)
            neighbors.extend(grid.grid[check_cell])

    # If the found neighbors are not enough, we expand the search to an even larger radius
    radius = 2
    while len(neighbors) < k:
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                check_cell = (cell_coords[0] + i, cell_coords[1] + j)
                # only new points
                neighbors.extend(p for p in grid.grid[check_cell] if p not in neighbors)

        radius += 1

    neighbors.sort(key=lambda p: np.sqrt((p.x - new_point.x) ** 2 + (p.y - new_point.y) ** 2))
    closest_neighbors = neighbors[:k]

    neighbor_colors = [neighbor.clasColor for neighbor in closest_neighbors]
    most_common_color = Counter(neighbor_colors).most_common(1)[0][0]

    return most_common_color


def visualize_points(points,k,accuracy):
    color_map = {
        'R': 'red',
        'G': 'green',
        'B': 'blue',
        'P': 'purple'
    }
    classified_x_coords = [point.x for point in points]
    classified_y_coords = [point.y for point in points]
    classified_colors = [color_map[point.clasColor] for point in points]

    plt.figure(figsize=(10, 10))

    plt.scatter(classified_x_coords, classified_y_coords, c=classified_colors, s=100, alpha=0.7, edgecolors='k')

    plt.title(f'Points Visualization for k={k}. Success is {accuracy:.2f}%')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.xlim(-5000, 5000)
    plt.ylim(-5000, 5000)

    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.axvline(0, color='black', linewidth=0.5, ls='--')

    plt.show()


def evaluate_accuracy(points):
    correct_count = sum(1 for point in points if point.startColor == point.clasColor)
    total_count = len(points)

    if total_count == 0:
        accuracy = 0
    else:
        accuracy = (correct_count / total_count) * 100

    print(f'Accuracy: {accuracy:.2f}% ({correct_count}/{total_count})')
    return accuracy


def main():
    cell_size = 250
    num_points_to_generate = 40000
    classes = ['R', 'G', 'B', 'P']
    testPoints=[]

    for i in range(num_points_to_generate):
        current_class = classes[i % len(classes)]
        new_point = generate_new_point(current_class)
        testPoints.append(new_point)

    for k in [1,3,7,15]:
        points = initialize_points()
        grid = DynamicGrid(cell_size)
        for point in points:
            grid.add_point(point)
        for point in testPoints:
            classified_color = classify(point, grid, k)

            point.clasColor = classified_color
            points.append(point)
            grid.add_point(point)

        accuracy = evaluate_accuracy(points)
        visualize_points(points, k, accuracy)
        for tpoint in testPoints:
            tpoint.clasColor=tpoint.startColor


if __name__ == '__main__':
    main()