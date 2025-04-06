# UVM to PyUVM Converter (uvm2pyuvm)

This project provides a tool to convert UVM SystemVerilog code into PyUVM Python code. The conversion process is automated and designed to handle multiple `.sv` files efficiently.

## Project Structure

```
uvm_converter
├── src
│   ├── converter.py       # Main logic for UVM to PyUVM conversion
│   └── utils
│       └── __init__.py    # Utility functions for the conversion process
├── input                   # Directory for input .sv files
│   └── (place .sv files here)
├── output                  # Directory for converted PyUVM files
│   └── (converted files will be saved here)
├── requirements.txt        # List of dependencies for the project
└── README.md               # Documentation for the project
```

## Getting Started

### Prerequisites

Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Installation

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required dependencies by running:

   ```
   pip install -r requirements.txt
   ```

### Usage

1. Place your `.sv` files in the `input` directory.
2. Run the conversion script by executing:

   ```
   python src/converter.py
   ```

3. The converted PyUVM files will be saved in the `output` directory.

### Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request with your changes.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.