# MACE - Mendoza Automated CRYSTAL Engine

<p align="center">
  <pre>
      ███╗   ███╗ █████╗  ██████╗███████╗
      ████╗ ████║██╔══██╗██╔════╝██╔════╝
      ██╔████╔██║███████║██║     █████╗  
      ██║╚██╔╝██║██╔══██║██║     ██╔══╝  
      ██║ ╚═╝ ██║██║  ██║╚██████╗███████╗
      ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝
  </pre>
</p>

<p align="center">
  <strong>A comprehensive scientific computing toolkit for CRYSTAL quantum chemistry workflows</strong>
</p>

---

## 🚀 Overview

MACE (Mendoza Automated CRYSTAL Engine) is an advanced automation framework for the CRYSTAL quantum chemistry software package. It provides end-to-end workflow management, from crystal structure preparation through electronic structure calculations to property analysis, all optimized for high-performance computing environments.

**Developed by**: Marcus Djokic (Primary Developer)  
**Contributors**: Daniel Maldonado Lopez, Brandon Lewis, William Comaskey  
**PI**: Prof. Jose Luis Mendoza-Cortes  
**Institution**: Michigan State University, Mendoza Group

## 📁 Repository Structure

```
reorganization/
├── README.md                  # This file
├── INSTALLATION.md            # Detailed installation guide
├── CLAUDE.md                  # Comprehensive technical documentation
│
├── mace_cli                   # Main MACE command-line interface
├── setup_mace.py              # Automated installation script
├── activate_mace.sh           # Environment activation script
│
├── mace/                      # Core MACE automation framework
│   ├── README.md              # MACE-specific documentation
│   ├── workflow/              # Workflow planning and execution
│   ├── queue/                 # HPC queue management
│   ├── database/              # Material tracking database
│   ├── submission/            # SLURM job submission
│   ├── recovery/              # Error detection and recovery
│   └── utils/                 # Analysis and utility tools
│
├── Crystal_d12/               # D12 input file generation
│   ├── README.md              # D12 tools documentation
│   ├── NewCifToD12.py         # CIF to D12 converter
│   ├── CRYSTALOptToD12.py     # Generate D12 from optimized structures
│   └── example_configs/       # Pre-configured calculation settings
│
├── Crystal_d3/                # D3 property calculation generation
│   ├── README.md              # D3 tools documentation
│   ├── CRYSTALOptToD3.py      # Generate property calculations
│   ├── d3_kpoints.py          # K-point path generation
│   └── example_configs/       # Property calculation templates
│
└── code/                      # Legacy scripts (preserved for compatibility)
    ├── Job_Scripts/           # Original job management tools
    ├── Check_Scripts/         # Status checking utilities
    ├── Plotting_Scripts/      # Visualization tools
    ├── Post_Processing_Scripts/ # Analysis utilities
    └── Band_Alignment/        # Band alignment calculations
```

## 🎯 Key Components

### 1. **MACE Framework** (`mace/`)
The heart of the automation system, providing:
- **Workflow Management**: Plan and execute complex calculation sequences
- **Queue Optimization**: Intelligent SLURM job scheduling and monitoring
- **Material Database**: Complete calculation history and provenance tracking
- **Error Recovery**: Automatic detection and fixing of common calculation errors
- **File Organization**: Systematic management of inputs, outputs, and results

### 2. **D12 Input Generation** (`Crystal_d12/`)
Tools for creating CRYSTAL input files:
- **CIF Conversion**: Automated conversion from crystallographic information files
- **Configuration Templates**: Pre-configured settings for common calculations
- **Optimization Extraction**: Generate new calculations from optimized geometries
- **JSON Configuration**: Save and reuse calculation settings

### 3. **D3 Property Calculations** (`Crystal_d3/`)
Generate property calculation inputs:
- **Band Structures**: Automatic k-path generation based on space group
- **Density of States**: Total and projected DOS with orbital resolution
- **Transport Properties**: Boltzmann transport calculations
- **Charge/Potential**: 3D charge density and electrostatic potential

### 4. **Legacy Tools** (`code/`)
Original scripts maintained for compatibility:
- Job submission and monitoring
- Output file analysis
- Property extraction
- Visualization tools

## 🔒 Workflow Isolation (NEW)

MACE now supports **workflow isolation** to prevent conflicts when running multiple workflows in the same directory. This feature addresses database contamination, material ID collisions, and queue manager conflicts that occurred when multiple workflows shared resources.

### Isolation Modes

1. **Isolated** (Recommended) - Complete separation with workflow-specific databases
2. **Shared** - Traditional behavior with shared database (backward compatible)
3. **Hybrid** - Shared schema with isolated data

### How It Works

The workflow isolation system provides:
- **Separate databases** per workflow to prevent material ID collisions
- **Independent job queues** with per-workflow limits and management
- **Isolated file storage** for calculation tracking and results
- **Automatic cleanup** and archival of completed workflows

### Directory Structure with Isolation

```
working_directory/
├── .mace_context_workflow_123/       # Hidden context directory
│   ├── materials.db                  # Isolated database
│   ├── structures.db                 # Isolated ASE database
│   ├── calculation_storage/          # Isolated file storage
│   ├── .queue_locks/                # Isolated locks
│   └── context_config.json          # Context metadata
├── workflow_configs/                # Shared configurations
└── workflow_outputs/                # Calculation outputs
```

### Using Workflow Isolation

#### Interactive Mode
When using `mace workflow --interactive`, you'll be prompted to select an isolation mode during workflow planning (Step 4.5).

#### Running Multiple Workflows Safely
```bash
# Terminal 1: Workflow for project A
cd /shared/calculations
mace workflow --interactive
# Select: Isolated mode

# Terminal 2: Workflow for project B (same directory!)
cd /shared/calculations  
mace workflow --interactive
# Select: Isolated mode

# Both workflows run independently without conflicts
```

#### Programmatic Usage
```python
from mace.workflow.context import workflow_context
from mace.database.materials_contextual import ContextualMaterialDatabase

# Execute workflow with isolation
with workflow_context("my_workflow", isolation_mode="isolated") as ctx:
    db = ContextualMaterialDatabase()
    # All database operations are isolated
```

### Benefits

- **No conflicts**: Multiple workflows can run in the same directory without interference
- **Clean organization**: Each workflow has its own hidden context directory
- **Easy cleanup**: Archive or delete entire workflow contexts when done
- **Backward compatible**: Existing scripts work unchanged in shared mode

For technical details, see the implementation in `mace/workflow/context.py`.

## ⚡ Quick Start

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd reorganization

# Run automated setup
python setup_mace.py --add-to-path

# Apply configuration
source ~/.zshrc  # or ~/.bashrc
```

See [INSTALLATION.md](INSTALLATION.md) for detailed installation instructions.

### Basic Usage

#### Interactive Workflow
```bash
# Launch interactive workflow planner
mace workflow --interactive
```

#### Quick CIF Processing
```bash
# Convert CIFs with full electronic structure workflow
mace workflow --quick-start --cif-dir ./cifs --workflow full_electronic
```

#### Direct Script Usage
```bash
# Convert CIF to D12
python Crystal_d12/NewCifToD12.py --cif_file structure.cif

# Generate property calculation
python Crystal_d3/CRYSTALOptToD3.py --input optimized.out --calc-type BAND
```

## 📚 Documentation

- **[INSTALLATION.md](INSTALLATION.md)** - Complete installation and setup guide
- **[CLAUDE.md](CLAUDE.md)** - Comprehensive technical documentation
- **[mace/README.md](mace/README.md)** - MACE framework documentation
- **[Crystal_d12/README.md](Crystal_d12/README.md)** - D12 input generation guide
- **[Crystal_d3/README.md](Crystal_d3/README.md)** - D3 property calculation guide

## 🔧 Main Scripts

### Core Interface
- **`mace_cli`** - Unified command-line interface for all MACE functionality (aliased as `mace`)
- **`setup_mace.py`** - Automated installation and environment configuration

### Input Generation
- **`Crystal_d12/NewCifToD12.py`** - Convert CIF files to CRYSTAL input
- **`Crystal_d12/CRYSTALOptToD12.py`** - Generate inputs from optimized structures
- **`Crystal_d3/CRYSTALOptToD3.py`** - Create property calculation inputs

### Workflow Management
- **`mace/run_workflow.py`** - Interactive workflow planning and execution
- **`mace/enhanced_queue_manager.py`** - Advanced HPC queue management
- **`mace/material_monitor.py`** - Real-time calculation monitoring

## 🛠️ Dependencies

Core requirements:
- Python 3.7+
- NumPy, Matplotlib, ASE, spglib
- PyYAML, pandas, PyPDF2

HPC requirements:
- SLURM workload manager
- CRYSTAL17/23 quantum chemistry software
- Intel MPI runtime

Install all dependencies:
```bash
pip install numpy matplotlib ase spglib PyPDF2 pyyaml pandas
```

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Follow existing code style
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

[License information to be added]

## 📖 Citation

If you use MACE in your research, please cite:
```
[Citation to be added]
```

## 💬 Support

- **Issues**: Report bugs via GitHub Issues
- **Documentation**: See [CLAUDE.md](CLAUDE.md) for comprehensive technical details
- **Contact**: [Contact information to be added]

---

<p align="center">
  <strong>MACE - Making CRYSTAL calculations accessible, automated, and reproducible</strong>
</p>