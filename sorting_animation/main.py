import pygame
import random
import time

pygame.init()

num_elements = 200
TIME_DELAY = 200

WIDTH, HEIGHT = num_elements * 4, num_elements * 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algorithm Sort Visualization")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

element_width = WIDTH / num_elements
element_height = HEIGHT / num_elements
elements = list(range(1, num_elements+1))
random.shuffle(elements)

def draw_elements(elements, color_positions=None, got_time=1):
    screen.fill(BLACK)
    if got_time == 1: display_time(time.perf_counter() - start_time[0] - (TIME_DELAY / 1000 * n_delays[0]))
    elif got_time == 2: display_time(res_time[0])
    for i, height in enumerate(elements):
        color = WHITE
        if color_positions and i in color_positions:
            if isinstance(color_positions[i], tuple):
                color = color_positions[i]
            else: color = RED if color_positions[i] == 'comparing' else GREEN
        pygame.draw.rect(screen, color, ((i * element_width, HEIGHT - element_height * height), (element_width, element_height * height)))
    pygame.display.update()

def display_time(elapsed_time):
    font = pygame.font.SysFont("Cascadia", 36)
    text = font.render(f"Time: {elapsed_time:.2f} seconds", True, WHITE)
    screen.blit(text, (10, 10))


# SORTING ALGORITHMS

def bubble_sort(elements):
    pygame.display.set_caption("Bubble Sort")
    n = len(elements)
    for i in range(n):
        for j in range(0, n-i-1):
            draw_elements(elements, {j: 'comparing', j+1: 'comparing'})    
            if elements[j] > elements[j+1]:
                elements[j], elements[j+1] = elements[j+1], elements[j]
                draw_elements(elements, {j: 'swapped', j+1: 'swapped'})
        draw_elements(elements)


def selection_sort(elements):
    pygame.display.set_caption("Selection Sort")
    n = len(elements)
    for i in range(n-1):
        min_idx = i
        for j in range(i+1, n):
            draw_elements(elements, {j: 'comparing', j+1: 'comparing'})
            if elements[j] < elements[min_idx]:
                min_idx = j
        
        elements[i], elements[min_idx] = elements[min_idx], elements[i]
        draw_elements(elements, {i: 'swapped', min_idx: 'swapped'})
        draw_elements(elements)


def insertion_sort(elements):
    pygame.display.set_caption("Insertion Sort")
    n = len(elements)
    for i in range(1, n):
        j = i
        while j > 0 and elements[j] < elements[j-1]:
            draw_elements(elements, {j: 'comparing', j-1: 'comparing'})
            elements[j], elements[j-1] = elements[j-1], elements[j]
            draw_elements(elements, {j: 'swapped', j-1: 'swapped'})
            j -= 1
        draw_elements(elements)


def merge_sort(elements, left=0, right=num_elements-1):
    
    pygame.display.set_caption("Merge Sort")

    def merge(elements, left, middle, right):
        left_copy = elements[left:middle + 1]
        right_copy = elements[middle + 1:right + 1]
        
        left_index, right_index = 0, 0
        sorted_index = left
        
        while left_index < len(left_copy) and right_index < len(right_copy):
            draw_elements(elements, {sorted_index: 'comparing'})
            
            if left_copy[left_index] <= right_copy[right_index]:
                elements[sorted_index] = left_copy[left_index]
                left_index += 1
            else:
                elements[sorted_index] = right_copy[right_index]
                right_index += 1
            
            sorted_index += 1
            draw_elements(elements, {sorted_index - 1: 'swapped'})
        
        while left_index < len(left_copy):
            elements[sorted_index] = left_copy[left_index]
            left_index += 1
            sorted_index += 1
            draw_elements(elements, {sorted_index - 1: 'swapped'})
        
        while right_index < len(right_copy):
            elements[sorted_index] = right_copy[right_index]
            right_index += 1
            sorted_index += 1
            draw_elements(elements, {sorted_index - 1: 'swapped'})    

    if left < right:
        middle = (left + right) // 2
        merge_sort(elements, left, middle)
        merge_sort(elements, middle + 1, right)
        merge(elements, left, middle, right)

        
def quick_sort(elements, low=0, high=num_elements-1):

    pygame.display.set_caption("Quick Sort")

    def partition(elements, low, high):
        pivot = elements[high]
        i = low - 1
        draw_elements(elements, {high: BLUE})
        for j in range(low, high):
            draw_elements(elements, {j: RED, high: BLUE})
            if elements[j] < pivot:
                i += 1
                elements[i], elements[j] = elements[j], elements[i]
                draw_elements(elements, {i: GREEN, j: GREEN, high: BLUE})
        elements[i + 1], elements[high] = elements[high], elements[i + 1]
        draw_elements(elements, {i + 1: GREEN, high: BLUE})
        return i + 1
        
    if low < high:
        pivot_index = partition(elements, low, high)
        quick_sort(elements, low, pivot_index - 1)
        quick_sort(elements, pivot_index + 1, high)


def radix_sort(elements, base = 10):
    
    pygame.display.set_caption(f"Radix Sort base {base}")

    def count_sorting(elements, exp):
        n = len(elements)
        output = [0] * n
        count = [0] * base
        
        for i in range(n):
            idx = elements[i] // exp
            count[idx % base] += 1
        
        for i in range(1, base):
            count[i] += count[i-1]

        i = n-1
        while i >= 0:
            idx = elements[i] // exp
            output[count[idx % base] - 1] = elements[i]
            count[idx % base] -= 1
            i -= 1
        
        i = 0
        for i in range(n):
            elements[i] = output[i]

    Max = max(elements)

    exp = 1
    while Max / exp >= 1:
        count_sorting(elements, exp)
        pygame.time.delay(TIME_DELAY)
        n_delays[0] += 1
        draw_elements(elements)
        exp *= base

def counting_sort(elements):

    pygame.display.set_caption("Counting Sort")

    Max = max(elements)
    Min = min(elements)

    n = Max - Min + 1
    count = [0] * n
    output = [0] * len(elements)

    for i in range(len(elements)):
        count[elements[i] - Min] += 1
        draw_elements(elements, {i: BLUE})
        pygame.time.delay(TIME_DELAY // 50)
        n_delays[0] += 0.02

    for i in range(1, n):
        count[i] += count[i - 1]

    for i in range(n):
        idx = count[elements[i] - Min] - 1
        output[idx] = elements[i]
        count[elements[i] - Min] -= 1
        draw_elements(output[:count[elements[i] - Min] + 1], {count[elements[i] - Min]: GREEN})
        pygame.time.delay(TIME_DELAY // 50)
        n_delays[0] += 0.02

    for i in range(n):
        elements[i] = output[i]
        draw_elements(elements, {i: GREEN})
        pygame.time.delay(TIME_DELAY // 50)
        n_delays[0] += 0.02


# MAIN

start_time = [0]
res_time = [0]
n_delays = [0]

def main(sort):
    sorting = False
    sorted = False
    finished = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sorting = True
                    sort = sort[:-1]
                    random.shuffle(elements)
                    sorted = False
                    finished = False
                    start_time[0] = time.perf_counter()
                    n_delays[0] = 0
        
        if sorting:
            # SELECT YOUR SORTING ALGORITHM
            if isinstance(sort[-1], list): sort[-1][0](elements, sort[-1][1])
            else: sort[-1](elements)
            sorting = False
            res_time[0] = time.perf_counter() - start_time[0] - (TIME_DELAY / 1000 * n_delays[0])
            sorted = True

        if sorted and not finished:
            for k in range(num_elements):
                draw_elements(elements, {i: 'swapped' for i in range(k)}, got_time=2)
            finished = True
        elif sorted:
            draw_elements(elements, {i: 'swapped' for i in range(num_elements)}, got_time=2)
        else:
            draw_elements(elements, got_time=0)

        pygame.display.update()
    
if __name__ == "__main__":
    main([None, bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort, [radix_sort, 2], [radix_sort, 10], counting_sort][::-1])
    
