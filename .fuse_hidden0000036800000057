# Documentation Build Script

This repository includes a Python script to build the EDS 217 course website for GitHub Pages deployment with **smart incremental build support** and **advanced cleaning capabilities**.

## Overview

The EDS 217 website is built using [Quarto](https://quarto.org/), which renders `.qmd` and `.ipynb` files into a static website deployed to the `docs/` folder for GitHub Pages.

**🚀 Key Features**:
- **Incremental builds by default**: Only rebuilds files that have changed since your last git commit
- **Smart cleaning**: Remove intermediate files (HTML, _files/, etc.) from course materials
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Integrated conda environment**: Automatically activates the `eds217_2025` environment

## Build Script Usage

### Basic Commands

```bash
# Incremental build (default - only changed files)
python build_docs.py
# or
./build_docs.py

# Full rebuild (rebuild everything)
python build_docs.py --full
# or
python build_docs.py -f

# Incremental build and serve locally
python build_docs.py --serve
# or
python build_docs.py -s

# Full rebuild and serve locally
python build_docs.py --full --serve

# Clean intermediate files only (no build)
python build_docs.py --clean
# or
python build_docs.py -c

# Clean and then do full rebuild
python build_docs.py --clean --full
```

## Command Options

### Build Options
- **`--full` or `-f`**: Force complete rebuild of all files (overrides incremental mode)
- **`--serve` or `-s`**: Build and automatically start a local server for preview

### Cleaning Options
- **`--clean` or `-c`**: Clean intermediate files from course materials directories

### Option Combinations
- **Default behavior**: Incremental build, show next steps
- **`--serve`**: Incremental build + start local server
- **`--full`**: Complete rebuild, show next steps  
- **`--full --serve`**: Complete rebuild + start local server
- **`--clean`**: Clean intermediate files only (no build)
- **`--clean --full`**: Clean intermediate files + complete rebuild
- **`--clean --serve`**: Clean intermediate files + incremental build + serve

## What the Script Does

### Standard Build Process
1. **Activate Environment**: Automatically activate the `eds217_2025` conda environment
2. **Check Prerequisites**: Verify that Quarto is installed and you're in the correct directory
3. **🆕 Smart File Detection** (incremental mode): Use git to detect which `.qmd` and `.ipynb` files have changed since the last commit
4. **Clean Previous Build**: Remove old files from the `docs/` directory
5. **Build Website**: Run `quarto render` on all files (full build) or only changed files (incremental build) with progress indicator
6. **Verify Build**: Check that the build completed successfully and required files exist
7. **Report Status**: Show build summary and next steps
8. **Serve Locally** (optional): Start a local server to preview your changes

### 🧹 Cleaning Process (with --clean flag)
The `--clean` option removes intermediate build files from the `course-materials/` directories:

**Files and directories removed:**
- `*.html` - Rendered HTML files
- `*_files/` - Quarto output directories  
- `*.ipynb_checkpoints/` - Jupyter checkpoints
- `*/.quarto/` - Quarto cache directories
- LaTeX auxiliary files (`*.aux`, `*.log`, `*.out`, `*.toc`, etc.)
- Other temporary build artifacts

**Benefits of cleaning:**
- ✅ Removes stale intermediate files that can cause build conflicts
- ✅ Reduces repository size by eliminating generated files
- ✅ Ensures fresh builds without cached artifacts
- ✅ Helps troubleshoot build issues caused by outdated intermediate files

## 🚀 Incremental Build Features

**Automatic Change Detection**: The script uses git to automatically detect:
- Modified files since the last commit (`git diff --name-only HEAD`)
- Staged changes (`git diff --name-only --cached`)
- New untracked files (`git ls-files --others --exclude-standard`)

**Intelligent Fallbacks**: 
- If not in a git repository: Falls back to full build
- If no previous commits: Falls back to full build
- If no changes detected: Skips build entirely (with option to force full build)

**File Type Filtering**: Only processes `.qmd` and `.ipynb` files, respecting the exclusions in `_quarto.yml`

### Progress Indicators

The script shows detailed progress information during builds:
- **File-by-file progress**: Shows each file being built with progress counter (e.g., "[5/23] Building: file.qmd")
- **Timing information**: Displays elapsed time and estimated time remaining (ETA)
- **Progress percentage**: Shows completion percentage for the current build
- **Individual file timing**: Shows how long each file takes to render
- **Build summary**: Final statistics including total time, average per file, fastest/slowest files
- **Real-time feedback**: Shows current file being processed and rendering status
- **Error handling**: Shows ❌ if individual files fail with detailed error information

**Example output:**
```
🚀 Starting full build (23 files to process)

[ 1/23] (  0.0%) Building: course-materials/day1.qmd
        ⏱️  Elapsed: 0.5s
        🔨 Rendering... ✅ Done (2.3s)

[ 2/23] (  4.3%) Building: course-materials/day2.qmd
        ⏱️  Elapsed: 2.8s (ETA: 48.3s)
        🔨 Rendering... ✅ Done (1.8s)

📊 Build completed!
   ⏱️  Total time: 45.2s
   📈 Average per file: 2.0s
   📁 Files processed: 23
   ⚡ Fastest file: 0.8s
   🐌 Slowest file: 4.2s
```

## Prerequisites

- [Quarto](https://quarto.org/docs/get-started/) must be installed
- The `eds217_2025` conda environment must exist (see [Environment Setup](README.md#-getting-started))
- Run the script from the project root directory (where `_quarto.yml` is located)
- **🆕 For incremental builds**: Git repository with at least one commit (automatic fallback to full build otherwise)

**Note**: The script automatically activates the `eds217_2025` environment before building.

## Typical Workflows

### Option 1: Fast Incremental Development (Recommended)
1. Make changes to your `.qmd` files or course materials
2. **Incremental build and preview** (builds only changed files):
   ```bash
   python build_docs.py --serve
   ```
3. Review your changes in the browser (opens automatically)
4. Press `Ctrl+C` to stop the local server
5. Commit and push changes to GitHub:
   ```bash
   git add .
   git commit -m "Update course content"
   git push origin main
   ```

### Option 2: Clean Development Workflow
1. Make extensive changes to course materials
2. **Clean intermediate files and rebuild**:
   ```bash
   python build_docs.py --clean --full --serve
   ```
3. Review the complete rebuilt site
4. Commit and push changes to GitHub

### Option 3: Quick Cleanup
1. **Clean intermediate files only** (no rebuild):
   ```bash
   python build_docs.py --clean
   ```
2. Review what was cleaned and commit if needed

### Option 4: Complete Rebuild (When Needed)
1. Make extensive changes or troubleshoot build issues
2. **Full build and preview**:
   ```bash
   python build_docs.py --full --serve
   ```
3. Review the complete rebuilt site
4. Commit and push changes to GitHub

## When to Use Each Option

### Use Incremental Build (Default) When:
- ✅ Making content updates to individual course materials
- ✅ Fixing typos or small changes
- ✅ Adding new course materials
- ✅ Regular development workflow
- ✅ **Speed is important** (builds 5-10x faster for small changes)

### Use Full Build (`--full`) When:
- 🔄 Troubleshooting build issues
- 🔄 Making changes to `_quarto.yml` configuration
- 🔄 Updating global styles or templates
- 🔄 After major git operations (rebasing, etc.)
- 🔄 Publishing final version
- 🔄 **When incremental build doesn't capture all dependencies**

### Use Clean (`--clean`) When:
- 🧹 Repository feels cluttered with intermediate files
- 🧹 Experiencing unexplained build issues
- 🧹 Before major releases or when switching branches
- 🧹 **Intermediate files are causing conflicts**
- 🧹 Want to reduce repository size

## Build Performance

### Enhanced Progress Tracking:
- **📊 Real-time progress**: See exactly which files are being processed and how many remain
- **⏱️ Timing estimates**: Get ETA based on average file processing times
- **📈 Performance insights**: Identify slow-building files for optimization
- **🎯 Granular feedback**: Individual file timing helps with debugging build issues

### Incremental Build Benefits:
- **⚡ 5-10x faster** for small changes (seconds instead of minutes)
- **🎯 Targeted rebuilds** - only processes changed files
- **🔍 Clear feedback** - shows exactly which files are being built with progress counters
- **💚 Environmentally friendly** - uses less CPU and energy

### Example Performance:
- **Full build**: ~2-5 minutes for entire course website (with detailed file-by-file progress)
- **Incremental build**: ~10-30 seconds for 1-3 changed files (with individual file timing)
- **No changes**: ~2 seconds (skips build entirely)
- **Clean operation**: ~5-10 seconds

### Progress Tracking Features:
- **File counters**: `[15/42]` shows current progress through all files
- **Percentage completion**: Shows how much of the build is complete
- **ETA calculation**: Estimates remaining time based on average file processing speed
- **Individual timing**: See which files are slow to help optimize your content
- **Summary statistics**: Get insights into build performance with fastest/slowest file times

## Troubleshooting

### General Issues
- **"Quarto not found"**: Install Quarto from https://quarto.org/docs/get-started/
- **"eds217_2025 environment not found"**: Create the environment using one of the setup guides in the README
- **"_quarto.yml not found"**: Make sure you're running the script from the project root directory
- **Permission denied**: Make sure the script is executable with `chmod +x build_docs.py`

### Incremental Build Issues
- **"Not in a git repository"**: Script automatically falls back to full build
- **Build seems incomplete**: Use `--full` flag to rebuild everything
- **Changes not detected**: Ensure files are saved and try `git status` to verify changes
- **Dependencies not updated**: Some changes (like `_quarto.yml` modifications) require `--full` rebuild

### Cleaning Issues
- **"No course-materials directory found"**: Script will report this and continue
- **Permission denied during cleaning**: Ensure you have write permissions to the course-materials directory
- **Files won't delete**: Some files might be in use; close any open editors and try again

### When Incremental Builds Don't Work
If you encounter issues with incremental builds:
1. **Clean first**: `python build_docs.py --clean`
2. **Use full build**: `python build_docs.py --full`
3. **Check git status**: `git status` to see what files are changed
4. **Commit changes first**: Sometimes uncommitted changes aren't detected properly
5. **Report the issue**: If incremental builds consistently fail, please report it

## Manual Build

If you prefer to build manually:
```bash
# Full build
quarto render

# Build specific files
quarto render course-materials/day1.qmd
quarto render course-materials/interactive-sessions/1a_iPython_JupyterLab.qmd

# Clean manually (remove intermediate files)
find course-materials -name "*.html" -delete
find course-materials -name "*_files" -type d -exec rm -rf {} +
```

## Migration Notes for Existing Users

**Simplified workflow**: Previously there were both shell and Python scripts. Now there's only the Python script for easier maintenance.

**New features available:**
- **`--clean` option**: Remove intermediate files from course materials
- **Enhanced cross-platform compatibility**: Works consistently across all operating systems
- **Same build behavior**: All previous commands still work exactly the same

**Command migration:**
- Previous: `./build_docs.sh` → **New**: `python build_docs.py`
- Previous: `./build_docs.sh --serve` → **New**: `python build_docs.py --serve`
- Previous: `./build_docs.sh --full` → **New**: `python build_docs.py --full` 