from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
from typing import List, Optional, Dict, Any
import random
from pydantic import BaseModel
import os

app = FastAPI(title="Sorting Algorithms Visualizer")

# Define templates directory
templates = Jinja2Templates(directory="templates")

# Define model for sort request
class SortRequest(BaseModel):
    array: List[int]
    algorithm: str

# Define model for sort step
class SortStep(BaseModel):
    array: List[int]
    comparisons: int
    swaps: int
    current_indices: List[int] = []
    auxiliary: Optional[List[int]] = None  # For merge sort visualization
    pivot_index: Optional[int] = None  # For quick sort visualization

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_visualizer(request: Request):
    """Render the main visualization page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/random-array")
async def get_random_array(size: int = 10, min_val: int = 1, max_val: int = 100):
    """Generate a random array for sorting"""
    return {"array": [random.randint(min_val, max_val) for _ in range(size)]}

@app.post("/api/sort", response_model=List[SortStep])
async def sort_array(request: SortRequest):
    """Perform the selected sorting algorithm and return the steps for visualization"""
    algorithm = request.algorithm.lower()
    arr = request.array.copy()
    
    if algorithm == "bubble":
        return bubble_sort(arr)
    elif algorithm == "selection":
        return selection_sort(arr)
    elif algorithm == "insertion":
        return insertion_sort(arr)
    elif algorithm == "merge":
        return merge_sort(arr)
    elif algorithm == "quick":
        return quick_sort(arr)
    elif algorithm == "heap":
        return heap_sort(arr)
    elif algorithm == "counting":
        return counting_sort(arr)
    else:
        return bubble_sort(arr)  # Default to bubble sort

def bubble_sort(arr: List[int]) -> List[SortStep]:
    """Implementation of bubble sort algorithm with step tracking"""
    steps = []
    n = len(arr)
    
    # Initial state
    steps.append(SortStep(
        array=arr.copy(),
        comparisons=0,
        swaps=0
    ))
    
    total_comparisons = 0
    total_swaps = 0
    
    for i in range(n):
        for j in range(0, n - i - 1):
            total_comparisons += 1
            
            # Record the comparison step
            steps.append(SortStep(
                array=arr.copy(),
                comparisons=total_comparisons,
                swaps=total_swaps,
                current_indices=[j, j+1]
            ))
            
            if arr[j] > arr[j + 1]:
                # Swap elements
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                total_swaps += 1
                
                # Record the swap step
                steps.append(SortStep(
                    array=arr.copy(),
                    comparisons=total_comparisons,
                    swaps=total_swaps,
                    current_indices=[j, j+1]
                ))
    
    # Final state
    steps.append(SortStep(
        array=arr.copy(),
        comparisons=total_comparisons,
        swaps=total_swaps
    ))
    
    return steps

def selection_sort(arr: List[int]) -> List[SortStep]:
    """Implementation of selection sort algorithm with step tracking"""
    steps = []
    n = len(arr)
    
    # Initial state
    steps.append(SortStep(
        array=arr.copy(),
        comparisons=0,
        swaps=0
    ))
    
    total_comparisons = 0
    total_swaps = 0
    
    for i in range(n):
        min_idx = i
        
        # Find the minimum element in the unsorted part
        for j in range(i + 1, n):
            total_comparisons += 1
            
            # Record the comparison step
            steps.append(SortStep(
                array=arr.copy(),
                comparisons=total_comparisons,
                swaps=total_swaps,
                current_indices=[min_idx, j]
            ))
            
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # Swap the found minimum element with the first element
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            total_swaps += 1
            
            # Record the swap step
            steps.append(SortStep(
                array=arr.copy(),
                comparisons=total_comparisons,
                swaps=total_swaps,
                current_indices=[i, min_idx]
            ))
    
    # Final state
    steps.append(SortStep(
        array=arr.copy(),
        comparisons=total_comparisons,
        swaps=total_swaps
    ))
    
    return steps

def insertion_sort(arr: List[int]) -> List[SortStep]:
    """Implementation of insertion sort algorithm with step tracking"""
    steps = []
    n = len(arr)
    
    # Initial state
    steps.append(SortStep(
        array=arr.copy(),
        comparisons=0,
        swaps=0
    ))
    
    total_comparisons = 0
    total_swaps = 0
    
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        
        # Add step to show current key element
        steps.append(SortStep(
            array=arr.copy(),
            comparisons=total_comparisons,
            swaps=total_swaps,
            current_indices=[i]
        ))
        
        while j >= 0:
            total_comparisons += 1
            
            # Record the comparison step
            steps.append(SortStep(
                array=arr.copy(),
                comparisons=total_comparisons,
                swaps=total_swaps,
                current_indices=[j, j+1]
            ))
            
            if arr[j] > key:
                arr[j + 1] = arr[j]
                total_swaps += 1
                
                # Record the shift step (counts as swap)
                steps.append(SortStep(
                    array=arr.copy(),
                    comparisons=total_comparisons,
                    swaps=total_swaps,
                    current_indices=[j, j+1]
                ))
                
                j -= 1
            else:
                break
        
        arr[j + 1] = key
        
        # Add step to show key placement if it changed position
        if j + 1 != i:
            steps.append(SortStep(
                array=arr.copy(),
                comparisons=total_comparisons,
                swaps=total_swaps,
                current_indices=[j+1]
            ))
    
    # Final state
    steps.append(SortStep(
        array=arr.copy(),
        comparisons=total_comparisons,
        swaps=total_swaps
    ))
    
    return steps

def merge_sort(arr: List[int]) -> List[SortStep]:
    """Implementation of merge sort algorithm with step tracking"""
    steps = []
    
    # Initial state
    steps.append(SortStep(
        array=arr.copy(),
        comparisons=0,
        swaps=0
    ))
    
    total_comparisons = 0
    total_swaps = 0
    
    # Define recursive merge sort function
    def merge_sort_recursive(arr, start, end):
        nonlocal steps, total_comparisons, total_swaps
        
        if end - start <= 1:
            return
        
        mid = (start + end) // 2
        
        # Record division step
        steps.append(SortStep(
            array=arr.copy(),
            comparisons=total_comparisons,
            swaps=total_swaps,
            current_indices=[start, mid, end-1]
        ))
        
        # Recursively sort left and right halves
        merge_sort_recursive(arr, start, mid)
        merge_sort_recursive(arr, mid, end)
        
        # Merge the sorted halves
        left = arr[start:mid]
        right = arr[mid:end]
        
        # Record before merge
        steps.append(SortStep(
            array=arr.copy(),
            comparisons=total_comparisons,
            swaps=total_swaps,
            current_indices=list(range(start, end)),
            auxiliary=left + right
        ))
        
        i = j = 0
        k = start
        
        while i < len(left) and j < len(right):
            total_comparisons += 1
            
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            
            k += 1
            total_swaps += 1
            
            # Record merge step
            steps.append(SortStep(
                array=arr.copy(),
                comparisons=total_comparisons,
                swaps=total_swaps,
                current_indices=[k-1],
                auxiliary=left + right
            ))
        
        # Copy remaining elements
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
            total_swaps += 1
            
            steps.append(SortStep(
                array=arr.copy(),
                comparisons=total_comparisons,
                swaps=total_swaps,
                current_indices=[k-1],
                auxiliary=left + right
            ))
        
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
            total_swaps += 1
            
            steps.append(SortStep(
                array=arr.copy(),
                comparisons=total_comparisons,
                swaps=total_swaps,
                current_indices=[k-1],
                auxiliary=left + right
            ))
    
    # Call recursive function
    merge_sort_recursive(arr, 0, len(arr))
    
    # Final state
    steps.append(SortStep(
        array=arr.copy(),
        comparisons=total_comparisons,
        swaps=total_swaps
    ))
    
    return steps

def quick_sort(arr: List[int]) -> List[SortStep]:
    """Implementation of quick sort algorithm with step tracking"""
    steps = []
    
    # Initial state
    steps.append(SortStep(
        array=arr.copy(),
        comparisons=0,
        swaps=0
    ))
    
    total_comparisons = 0
    total_swaps = 0
    
    def partition(arr, low, high):
        nonlocal steps, total_comparisons, total_swaps
        
        pivot = arr[high]
        i = low - 1
        
        # Record pivot selection
        steps.append(SortStep(
            array=arr.copy(),
            comparisons=total_comparisons,
            swaps=total_swaps,
            current_indices=[low, high],
            pivot_index=high
        ))
        
        for j in range(low, high):
            total_comparisons += 1
            
            # Record comparison step
            steps.append(SortStep(
                array=arr.copy(),
                comparisons=total_comparisons,
                swaps=total_swaps,
                current_indices=[j, high],
                pivot_index=high
            ))
            
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                total_swaps += 1
                
                # Record swap step
                steps.append(SortStep(
                    array=arr.copy(),
                    comparisons=total_comparisons,
                    swaps=total_swaps,
                    current_indices=[i, j],
                    pivot_index=high
                ))
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        total_swaps += 1
        
        # Record pivot placement
        steps.append(SortStep(
            array=arr.copy(),
            comparisons=total_comparisons,
            swaps=total_swaps,
            current_indices=[i + 1, high],
            pivot_index=i + 1
        ))
        
        return i + 1
    
    def quick_sort_recursive(arr, low, high):
        if low < high:
            # Partition and get pivot index
            pi = partition(arr, low, high)
            
            # Sort elements before and after partition
            quick_sort_recursive(arr, low, pi - 1)
            quick_sort_recursive(arr, pi + 1, high)
    
    quick_sort_recursive(arr, 0, len(arr) - 1)
    
    # Final state
    steps.append(SortStep(
        array=arr.copy(),
        comparisons=total_comparisons,
        swaps=total_swaps
    ))
    
    return steps

def heap_sort(arr: List[int]) -> List[SortStep]:
    """Implementation of heap sort algorithm with step tracking"""
    steps = []
    n = len(arr)
    
    # Initial state
    steps.append(SortStep(
        array=arr.copy(),
        comparisons=0,
        swaps=0
    ))
    
    total_comparisons = 0
    total_swaps = 0
    
    # Heapify function
    def heapify(arr, n, i):
        nonlocal steps, total_comparisons, total_swaps
        
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        # Check if left child exists and is greater than root
        if left < n:
            total_comparisons += 1
            
            steps.append(SortStep(
                array=arr.copy(),
                comparisons=total_comparisons,
                swaps=total_swaps,
                current_indices=[i, left]
            ))
            
            if arr[left] > arr[largest]:
                largest = left
        
        # Check if right child exists and is greater than largest so far
        if right < n:
            total_comparisons += 1
            
            steps.append(SortStep(
                array=arr.copy(),
                comparisons=total_comparisons,
                swaps=total_swaps,
                current_indices=[largest, right]
            ))
            
            if arr[right] > arr[largest]:
                largest = right
        
        # Change root if needed
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            total_swaps += 1
            
            steps.append(SortStep(
                array=arr.copy(),
                comparisons=total_comparisons,
                swaps=total_swaps,
                current_indices=[i, largest]
            ))
            
            # Heapify the affected sub-tree
            heapify(arr, n, largest)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        total_swaps += 1
        
        steps.append(SortStep(
            array=arr.copy(),
            comparisons=total_comparisons,
            swaps=total_swaps,
            current_indices=[0, i]
        ))
        
        heapify(arr, i, 0)
    
    # Final state
    steps.append(SortStep(
        array=arr.copy(),
        comparisons=total_comparisons,
        swaps=total_swaps
    ))
    
    return steps

def counting_sort(arr: List[int]) -> List[SortStep]:
    """Implementation of counting sort algorithm with step tracking"""
    steps = []
    
    # Initial state
    steps.append(SortStep(
        array=arr.copy(),
        comparisons=0,
        swaps=0
    ))
    
    total_comparisons = 0
    total_swaps = 0
    
    # Find the range of input elements
    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val - min_val + 1
    
    # Create count array and initialize with zeros
    count = [0] * range_val
    output = [0] * len(arr)
    
    # Record the count array initialization
    steps.append(SortStep(
        array=arr.copy(),
        comparisons=total_comparisons,
        swaps=total_swaps,
        auxiliary=count.copy()
    ))
    
    # Count occurrences of each element
    for i in range(len(arr)):
        count[arr[i] - min_val] += 1
        total_comparisons += 1
        
        # Record counting step
        steps.append(SortStep(
            array=arr.copy(),
            comparisons=total_comparisons,
            swaps=total_swaps,
            current_indices=[i],
            auxiliary=count.copy()
        ))
    
    # Update count array to store position of each element
    for i in range(1, len(count)):
        count[i] += count[i - 1]
        
        # Record cumulative count update
        steps.append(SortStep(
            array=arr.copy(),
            comparisons=total_comparisons,
            swaps=total_swaps,
            auxiliary=count.copy()
        ))
    
    # Build the output array
    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1
        total_swaps += 1
        
        temp_array = arr.copy()
        # Update the original array with the values we've placed so far
        for j in range(len(arr)):
            if j < len(arr) - i:
                temp_array[j] = output[j]
        
        # Record element placement step
        steps.append(SortStep(
            array=temp_array,
            comparisons=total_comparisons,
            swaps=total_swaps,
            current_indices=[count[arr[i] - min_val]],
            auxiliary=count.copy()
        ))
    
    # Copy the output array back to the original array
    for i in range(len(arr)):
        arr[i] = output[i]
    
    # Final state
    steps.append(SortStep(
        array=arr.copy(),
        comparisons=total_comparisons,
        swaps=total_swaps
    ))
    
    return steps

