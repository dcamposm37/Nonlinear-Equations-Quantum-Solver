# ==============================================================================
#  Quantum Nonlinear Solvers — Makefile
# ==============================================================================
#
#  Targets
#  -------
#    install            Install Python dependencies from requirements.txt.
#
#    --- Individual solvers (pendulum) ---
#    run-lcu-lin-sv     LCU  linear    — statevector
#    run-lcu-lin-meas   LCU  linear    — measurements
#    run-lcu-nlin-sv    LCU  nonlinear — statevector
#    run-lcu-nlin-meas  LCU  nonlinear — measurements
#    run-rot-lin-sv     Rotations linear    — statevector   (TODO)
#    run-rot-lin-meas   Rotations linear    — measurements  (TODO)
#    run-rot-nlin-sv    Rotations nonlinear — statevector   (TODO)
#    run-rot-nlin-meas  Rotations nonlinear — measurements  (TODO)
#
#    --- Batch targets ---
#    run-all-sv         Run all statevector simulations     (~minutes)
#    run-all-meas       Run all measurement simulations     (~hours)
#    run-all            Run everything
#    figures            Regenerate all figures (= run-all-sv)
#
#    --- Documentation ---
#    docs               Compile LaTeX reports to PDF
#
#    --- Housekeeping ---
#    clean-figures      Delete generated figures
#    clean-docs         Delete LaTeX auxiliary files
#    clean              Full clean (figures + docs + __pycache__)
#    lint               Check code style with flake8
#    format             Auto-format with black
# ==============================================================================

# Path to the Python interpreter (using your Anaconda path detected)
PYTHON ?= C:\Users\carda\anaconda3\python.exe

# ---- Installation -----------------------------------------------------------
.PHONY: install
install:
	pip install -r requirements.txt

# ---- Individual pendulum solvers --------------------------------------------
.PHONY: run-lcu-lin-sv run-lcu-lin-meas
run-lcu-lin-sv:
	$(PYTHON) -m pendulum.solvers.lcu_linear_statevector

run-lcu-lin-meas:
	$(PYTHON) -m pendulum.solvers.lcu_linear_measurements

.PHONY: run-lcu-nlin-sv run-lcu-nlin-meas
run-lcu-nlin-sv:
	$(PYTHON) -m pendulum.solvers.lcu_nonlinear_statevector

run-lcu-nlin-meas:
	$(PYTHON) -m pendulum.solvers.lcu_nonlinear_measurements

.PHONY: run-rot-lin-sv run-rot-lin-meas run-rot-nlin-sv run-rot-nlin-meas
run-rot-lin-sv:
	$(PYTHON) -m pendulum.rotations.linear_statevector

run-rot-lin-meas:
	$(PYTHON) -m pendulum.rotations.linear_measurements

run-rot-nlin-sv:
	$(PYTHON) -m pendulum.rotations.nonlinear_statevector

run-rot-nlin-meas:
	$(PYTHON) -m pendulum.rotations.nonlinear_measurements

# ---- Lorenz solvers ---------------------------------------------------------
.PHONY: run-lorenz-be-sv run-lorenz-be-meas
run-lorenz-be-sv:
	$(PYTHON) -m lorenz.solvers.block_encoding_statevector

run-lorenz-be-meas:
	$(PYTHON) -m lorenz.solvers.block_encoding_measurements

# ---- Batch targets ----------------------------------------------------------
.PHONY: run-all-sv run-all-meas run-all figures
run-all-sv: run-lcu-lin-sv run-lcu-nlin-sv run-rot-lin-sv run-rot-nlin-sv

run-all-meas: run-lcu-lin-meas run-lcu-nlin-meas run-rot-lin-meas run-rot-nlin-meas

run-all: run-all-sv run-all-meas

figures: run-all-sv

# ---- Documentation ----------------------------------------------------------
.PHONY: docs
docs:
	cd docs && pdflatex error_propagation_analysis.tex && pdflatex error_propagation_analysis.tex

# ---- Housekeeping -----------------------------------------------------------
.PHONY: clean-figures clean-docs clean lint format
clean-figures:
	rm -f pendulum/figures/*.png
	rm -f lorenz/figures/*.png

clean-docs:
	rm -f docs/*.aux docs/*.log docs/*.out docs/*.toc

clean: clean-figures clean-docs
	find . -type d -name __pycache__ -exec rm -rf {} +

lint:
	flake8 pendulum/ lorenz/ --max-line-length=100 --ignore=E501

format:
	black pendulum/ lorenz/ --line-length=100
