document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const arrayContainer = document.getElementById('array-container');
    const auxiliaryContainer = document.getElementById('auxiliary-container');
    const algorithmSelect = document.getElementById('algorithm');
    const arraySizeInput = document.getElementById('array-size');
    const sizeValueDisplay = document.getElementById('size-value');
    const speedInput = document.getElementById('speed');
    const speedValueDisplay = document.getElementById('speed-value');
    const generateBtn = document.getElementById('generate-btn');
    const sortBtn = document.getElementById('sort-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const resetBtn = document.getElementById('reset-btn');
    const comparisonsDisplay = document.getElementById('comparisons');
    const swapsDisplay = document.getElementById('swaps');
    const timeComplexityDisplay = document.getElementById('time-complexity');
    const spaceComplexityDisplay = document.getElementById('space-complexity');
    const algorithmDescription = document.getElementById('algorithm-description');
    const themeBtn = document.getElementById('theme-btn');

    // State variables
    let array = [];
    let sortingSteps = [];
    let currentStepIndex = 0;
    let animationInterval = null;
    let isPaused = false;
    let isSorting = false;
    let barElements = [];
    let auxiliaryBarElements = [];
    
    // Algorithm information
    const algorithmInfo = {
        bubble: {
            name: "Bubble Sort",
            description: "Bubble Sort is a simple comparison-based algorithm. It repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. The process continues until no more swaps are needed.",
            timeComplexity: "O(n²)",
            spaceComplexity: "O(1)",
            bestCase: "O(n) - when array is already sorted"
        },
        selection: {
            name: "Selection Sort",
            description: "Selection Sort divides the input list into two parts: a sorted sublist and an unsorted sublist. It repeatedly finds the minimum element from the unsorted sublist and moves it to the end of the sorted sublist.",
            timeComplexity: "O(n²)",
            spaceComplexity: "O(1)",
            bestCase: "O(n²) - even if array is sorted"
        },
        insertion: {
            name: "Insertion Sort",
            description: "Insertion Sort builds the final sorted array one item at a time. It takes one element from the input data and finds its correct position in the already sorted part of the array.",
            timeComplexity: "O(n²)",
            spaceComplexity: "O(1)",
            bestCase: "O(n) - when array is almost sorted"
        },
        merge: {
            name: "Merge Sort",
            description: "Merge Sort is an efficient, divide-and-conquer algorithm. It divides the input array into two halves, recursively sorts them, and then merges the sorted halves.",
            timeComplexity: "O(n log n)",
            spaceComplexity: "O(n)",
            bestCase: "O(n log n) - consistent performance"
        },
        quick: {
            name: "Quick Sort",
            description: "Quick Sort is an efficient, divide-and-conquer algorithm that picks an element as a pivot and partitions the array around the pivot. Different strategies can be used to select the pivot.",
            timeComplexity: "O(n log n)",
            spaceComplexity: "O(log n)",
            bestCase: "O(n log n) - with good pivot selection"
        },
        heap: {
            name: "Heap Sort",
            description: "Heap Sort converts the array into a max heap, then repeatedly extracts the maximum element and rebuilds the heap until the array is sorted.",
            timeComplexity: "O(n log n)",
            spaceComplexity: "O(1)",
            bestCase: "O(n log n) - consistent performance"
        },
        counting: {
            name: "Counting Sort",
            description: "Counting Sort is a non-comparison-based algorithm that works by counting the number of objects having distinct key values, and using arithmetic to determine their positions in the output.",
            timeComplexity: "O(n + k)",
            spaceComplexity: "O(n + k)",
            bestCase: "O(n + k) - where k is the range of input"
        }
    };

    // Initialize the visualization
    initVisualization();

    // Theme toggle functionality
    themeBtn.addEventListener('click', toggleTheme);

    function toggleTheme() {
        const body = document.body;
        const icon = themeBtn.querySelector('i');
        
        if (body.classList.contains('dark-theme')) {
            body.classList.remove('dark-theme');
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        } else {
            body.classList.add('dark-theme');
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    }

    // Event Listeners
    algorithmSelect.addEventListener('change', updateAlgorithmInfo);
    arraySizeInput.addEventListener('input', updateSizeValue);
    speedInput.addEventListener('input', updateSpeedValue);
    generateBtn.addEventListener('click', generateNewArray);
    sortBtn.addEventListener('click', startSorting);
    pauseBtn.addEventListener('click', togglePause);
    resetBtn.addEventListener('click', resetVisualization);

    function initVisualization() {
        updateAlgorithmInfo();
        generateNewArray();
    }

    function updateAlgorithmInfo() {
        const algorithm = algorithmSelect.value;
        const info = algorithmInfo[algorithm];
        
        if (info) {
            algorithmDescription.innerHTML = `
                <p>${info.description}</p>
                <h3>Characteristics:</h3>
                <ul>
                    <li><strong>Average Time Complexity:</strong> ${info.timeComplexity}</li>
                    <li><strong>Space Complexity:</strong> ${info.spaceComplexity}</li>
                    <li><strong>Best Case:</strong> ${info.bestCase}</li>
                </ul>
            `;
            
            timeComplexityDisplay.textContent = info.timeComplexity;
            spaceComplexityDisplay.textContent = info.spaceComplexity;
        }
    }

    function updateSizeValue() {
        const size = arraySizeInput.value;
        sizeValueDisplay.textContent = size;
        
        if (!isSorting) {
            generateNewArray();
        }
    }

    function updateSpeedValue() {
        const speed = speedInput.value;
        const delayMs = 101 - speed; // Invert the scale (higher = faster)
        speedValueDisplay.textContent = `${delayMs} ms`;
        
        if (animationInterval) {
            clearInterval(animationInterval);
            if (!isPaused && isSorting) {
                startAnimation();
            }
        }
    }

    function generateNewArray() {
        if (isSorting) return;
        
        resetVisualization();
        const size = parseInt(arraySizeInput.value);
        array = [];
        
        // Generate random array
        for (let i = 0; i < size; i++) {
            array.push(Math.floor(Math.random() * 100) + 1);
        }
        
        // Render the array
        renderArray();
        
        // Reset stats
        comparisonsDisplay.textContent = '0';
        swapsDisplay.textContent = '0';
    }

    function renderArray() {
        arrayContainer.innerHTML = '';
        barElements = [];
        
        const maxValue = Math.max(...array);
        const containerHeight = arrayContainer.clientHeight - 20; // Account for padding
        const barWidth = Math.max(5, Math.min(30, arrayContainer.clientWidth / array.length - 2));
        
        array.forEach((value, index) => {
            const barHeight = (value / maxValue) * containerHeight;
            const bar = document.createElement('div');
            bar.className = 'bar';
            bar.style.height = `${barHeight}px`;
            bar.style.width = `${barWidth}px`;
            
            const valueLabel = document.createElement('div');
            valueLabel.className = 'bar-value';
            valueLabel.textContent = value;
            bar.appendChild(valueLabel);
            
            arrayContainer.appendChild(bar);
            barElements.push(bar);
        });
    }

    function renderAuxiliaryArray(auxiliaryArray) {
        if (!auxiliaryArray || auxiliaryArray.length === 0) {
            auxiliaryContainer.style.display = 'none';
            return;
        }
        
        auxiliaryContainer.style.display = 'flex';
        auxiliaryContainer.innerHTML = '';
        auxiliaryBarElements = [];
        
        const maxValue = Math.max(...auxiliaryArray);
        const containerHeight = auxiliaryContainer.clientHeight - 20;
        const barWidth = Math.max(5, Math.min(30, auxiliaryContainer.clientWidth / auxiliaryArray.length - 2));
        
        auxiliaryArray.forEach((value) => {
            const barHeight = (value / maxValue) * containerHeight;
            const bar = document.createElement('div');
            bar.className = 'auxiliary-bar';
            bar.style.height = `${barHeight}px`;
            bar.style.width = `${barWidth}px`;
            
            auxiliaryContainer.appendChild(bar);
            auxiliaryBarElements.push(bar);
        });
    }

    async function startSorting() {
        if (isSorting) return;
        
        // Disable controls
        isSorting = true;
        sortBtn.disabled = true;
        generateBtn.disabled = true;
        algorithmSelect.disabled = true;
        arraySizeInput.disabled = true;
        resetBtn.disabled = false;
        pauseBtn.disabled = false;
        
        // Get sorting algorithm
        const algorithm = algorithmSelect.value;
        
        try {
            // Fetch sorting steps from the API
            const response = await fetch('/api/sort', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    array: array,
                    algorithm: algorithm
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to fetch sorting steps');
            }
            
            sortingSteps = await response.json();
            currentStepIndex = 0;
            
            // Start animation
            startAnimation();
        } catch (error) {
            console.error('Error:', error);
            resetVisualization();
            alert('Failed to fetch sorting steps. Please try again.');
        }
    }

    function startAnimation() {
        if (animationInterval) {
            clearInterval(animationInterval);
        }
        
        const speed = 101 - parseInt(speedInput.value); // Invert the scale
        
        animationInterval = setInterval(() => {
            if (currentStepIndex >= sortingSteps.length) {
                finishSorting();
                return;
            }
            
            visualizeStep(sortingSteps[currentStepIndex]);
            currentStepIndex++;
        }, speed);
    }

    function visualizeStep(step) {
        // Update statistics
        comparisonsDisplay.textContent = step.comparisons;
        swapsDisplay.textContent = step.swaps;
        
        // Reset all bar colors
        barElements.forEach(bar => {
            bar.className = 'bar';
        });
        
        // Update array representation
        const maxValue = Math.max(...step.array);
        const containerHeight = arrayContainer.clientHeight - 20;
        
        step.array.forEach((value, index) => {
            const barHeight = (value / maxValue) * containerHeight;
            barElements[index].style.height = `${barHeight}px`;
            barElements[index].querySelector('.bar-value').textContent = value;
        });
        
        // Highlight current operation
        if (step.current_indices && step.current_indices.length > 0) {
            step.current_indices.forEach(index => {
                if (index >= 0 && index < barElements.length) {
                    barElements[index].classList.add('comparing');
                }
            });
        }
        
        // Highlight pivot for quick sort
        if (step.pivot_index !== undefined && step.pivot_index !== null) {
            if (step.pivot_index >= 0 && step.pivot_index < barElements.length) {
                barElements[step.pivot_index].classList.add('pivot');
            }
        }
        
        // Render auxiliary array for merge sort or counting sort
        if (step.auxiliary) {
            renderAuxiliaryArray(step.auxiliary);
        } else {
            auxiliaryContainer.style.display = 'none';
        }
        
        // For the final step, mark all as sorted
        if (currentStepIndex === sortingSteps.length - 1) {
            barElements.forEach(bar => {
                bar.className = 'bar sorted';
            });
        }
    }

    function togglePause() {
        isPaused = !isPaused;
        
        if (isPaused) {
            clearInterval(animationInterval);
            pauseBtn.textContent = 'Resume';
            pauseBtn.classList.remove('warning');
            pauseBtn.classList.add('success');
        } else {
            startAnimation();
            pauseBtn.textContent = 'Pause';
            pauseBtn.classList.remove('success');
            pauseBtn.classList.add('warning');
        }
    }

    function finishSorting() {
        clearInterval(animationInterval);
        isSorting = false;
        isPaused = false;
        
        // Mark all bars as sorted
        barElements.forEach(bar => {
            bar.className = 'bar sorted';
        });
        
        // Reset button states
        pauseBtn.disabled = true;
        pauseBtn.textContent = 'Pause';
        pauseBtn.classList.remove('success');
        pauseBtn.classList.add('warning');
        resetBtn.disabled = false;
        generateBtn.disabled = false;
    }

    function resetVisualization() {
        // Clear animation interval
        if (animationInterval) {
            clearInterval(animationInterval);
        }
        
        // Reset state
        isSorting = false;
        isPaused = false;
        currentStepIndex = 0;
        sortingSteps = [];
        
        // Reset UI
        comparisonsDisplay.textContent = '0';
        swapsDisplay.textContent = '0';
        auxiliaryContainer.style.display = 'none';
        
        // Reset buttons
        sortBtn.disabled = false;
        generateBtn.disabled = false;
        pauseBtn.disabled = true;
        resetBtn.disabled = true;
        algorithmSelect.disabled = false;
        arraySizeInput.disabled = false;
        
        pauseBtn.textContent = 'Pause';
        pauseBtn.classList.remove('success');
        pauseBtn.classList.add('warning');
        
        // Render the current array
        renderArray();
    }
});