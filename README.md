# Scientific Calculator

A Python-based scientific calculator project built with Kivy for the AQA Computer Science NEA and extended further for personal interest. The application provides a graphical calculator interface with a custom expression engine, scientific functions, and a bitmap-style display.

## Overview

This project implements a calculator that can:
- evaluate arithmetic expressions entered through a button-based GUI,
- perform scientific operations such as trigonometry, logarithms, powers, roots, and factorials,
- use mathematical constants such as $\pi$ and $e$,
- store and recall variables and memory values,
- display input and output in a calculator-style interface.

## Features

- Basic arithmetic: addition, subtraction, multiplication, division, negatives, percentages
- Scientific operations:
  - trigonometric functions: sin, cos, tan and inverse functions
  - logarithms: natural log, base 10 log, custom base log
  - powers and roots: squares, cubes, custom powers, square roots, cube roots
  - factorial, permutations, and combinations
- Mathematical constants: $\pi$, $e$
- Variable and memory support: A–F, X, Y, M, and Ans
- Interactive GUI with calculator-style buttons and indicator lights
- Expression parsing and evaluation handled by the project’s own logic modules

## Requirements

- Python 3.10+
- Kivy

Install the required dependency with:

```bash
pip install kivy
```

## Running the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/AQA-CS-NEA---Scientific-Calculator.git
   cd AQA-CS-NEA---Scientific-Calculator
   ```

2. Install dependencies:
   ```bash
   pip install kivy
   ```

3. Start the calculator:
   ```bash
   python main.py
   ```

## Project Structure

- main.py — application entry point
- core/ — core controller and input/output interface logic
- expression/ — expression parsing, evaluation, and normalisation
- gui/ — Kivy GUI layout, screens, and widgets
- math_op/ — mathematical operations and constants
- router/ — input routing and state handling
- utilities/ — shared helpers and custom types

## Development Notes

The calculator is split into separate modules so that UI handling, expression processing, and mathematical computation are kept independent. This makes it easier to extend the calculator with new buttons, functions, or display behaviour.

## License

See the LICENSE file for licensing information.
