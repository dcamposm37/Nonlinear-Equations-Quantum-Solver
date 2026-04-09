## **El Agente Cuántico : Automating quantum simulations** 

**Ignacio Gustin**[1] , **Luis Mantilla Calderón**[2] _[,]_[6] , **Juan B. Pérez-Sánchez**[1] , **Chris Crebolder**[2] _[,]_[6] , **Jérôme F. Gonthier**[8] , **Mohammad Ghazi Vakili**[1] _[,]_[2] , **Yuma Nakamura**[2] _[,]_[5] _[,]_[6] , **Karthik Panicker**[1] _[,]_[6] , **Manav Ramprasad**[2] _[,]_[6] , **Zijian Zhang**[2] _[,]_[6] , **Yunheng Zou**[2] _[,]_[6] , **Varinia Bernales**[1] _[,]_[2] _[,]_[5] _[,][∗]_ , **Alán Aspuru-Guzik**[1] _[,]_[2] _[,]_[3] _[,]_[4] _[,]_[5] _[,]_[6] _[,]_[7] _[,]_[8] _[,][∗]_ 

> 1Department of Chemistry, University of Toronto, 80 St. George St., Toronto, ON M5S 3H6, Canada 

> 2Department of Computer Science, University of Toronto, 40 St George St., Toronto, ON M5S 2E4, Canada 

> 3Department of Materials Science & Engineering, University of Toronto, 184 College St., Toronto, ON M5S 3E4, Canada 

> 4Department of Chemical Engineering & Applied Chemistry, University of Toronto, 200 College St., Toronto, ON M5S 3E5, Canada 

> 5Acceleration Consortium, 700 University Ave., Toronto, ON M7A 2S4, Canada 

> 6Vector Institute for Artificial Intelligence, W1140-108 College St., Schwartz Reisman Innovation Campus, Toronto, ON M5G 0C6, Canada 

> 7Canadian Institute for Advanced Research (CIFAR), 661 University Ave., Toronto, ON M5G 1M1, Canada 

> 8NVIDIA Corporation, Santa Clara, CA, USA 

Quantum simulation is central to understanding and designing quantum systems across physics and chemistry. However, its practical use is often limited by the exponential growth of Hilbert space and by the increasing complexity of modern quantum-simulation software. Here we introduce El Agente Cuántico, a multi-agent AI system that automates quantum-simulation workflows by translating natural-language scientific intent into executed and validated computations across heterogeneous quantum-software frameworks. By reasoning directly over library documentation and APIs, our agentic system dynamically assembles end-to-end simulations spanning state preparation, closed- and open-system dynamics, tensor-network methods, quantum control, quantum error correction, and quantum resource estimation. The developed system unifies traditionally distinct simulation paradigms behind a single natural-language interface. Beyond reducing technical barriers, this approach opens a path toward scalable, adaptive, and increasingly autonomous quantum simulation, enabling faster exploration of physical models, rapid hypothesis testing, and closer integration between theory, simulation, and emerging quantum hardware. 

## **Date:** March 9, 2026 

**==> picture [252 x 21] intentionally omitted <==**

**----- Start of picture text -----**<br>
|||||
|---|---|---|---|
|Correspondence:|Alán|Aspuru-Guzik|alan@aspuru.com|
|and|Varinia|Bernales|varinia@bernales.org|

**----- End of picture text -----**<br>


**==> picture [57 x 32] intentionally omitted <==**

**==> picture [19 x 18] intentionally omitted <==**

**==> picture [43 x 11] intentionally omitted <==**

## **Contents** 

**==> picture [472 x 101] intentionally omitted <==**

**----- Start of picture text -----**<br>
||||||||||||||||||||||||||||||||||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|1|Introduction|3|
|2|Architecture|of|El Agente Cuántico|4|
|3|Experiments|for|quantum|simulations|5|
|3.1|State|preparation|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|6|
|3.1.1|Variational|quantum|eigensolver|(VQE)|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|6|
|3.1.2|Bell|state|preparation|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|8|
|3.1.3|Thermal|states|via|imaginary-time|evolution|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|.|9|

**----- End of picture text -----**<br>


1 

||3.2|Time-independent Hamiltonian simulation . . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|10|
|---|---|---|---|---|
|||3.2.1<br>Trotter decomposition . . . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|10|
|||3.2.2<br>Open systems dynamics using the Lindblad approximation<br>. . . . . . . . . . . . . . .||12|
|||3.2.3<br>Hierarchical equations of motion (HEOM) . . . . . . . . . . . . . . . . . . . . . . . . .||14|
||3.3|Time-dependent Hamiltonians . . . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|15|
|||3.3.1<br>Quantum optimal control . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|15|
|||3.3.2<br>Time-dependent product formulas<br>. . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|16|
|||3.3.3<br>Time-evolving block decimation (TEBD)|. . . . . . . . . . . . . . . . . . . . . . . . .|17|
|**4**|**Reproducibility benchmark**|||**19**|
|**5**|**Beyond quantum simulation**|||**20**|
||5.1|Phase diagrams of quantum systems . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|20|
||5.2|Bell-state correlations under depolarizing noise|. . . . . . . . . . . . . . . . . . . . . . . . . .|21|
||5.3|Estimating qubit requirements for quantum simulation . . . . . . . . . . . . . . . . . . . . . .||22|
||5.4|Quantum error correction . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|24|
|**6**|**Discussion**|||**25**|
||6.1|El Agente Cuántico roadmap . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|26|
|**7**|**Conclusions**|||**28**|
|**S1 **|**Agents and tools**|||**S1**|
|**S2 **|**Log **|**sessions**||**S2**|
||S2.1|Variational quantum eigensolver. . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|S2|
||S2.2|Bell states preparation . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|S5|
||S2.3|Thermal states via imaginary-time evolution . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|S7|
||S2.4|Trotter decomposition . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|S10|
||S2.5|Lindbladian dynamics . . . . . . . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|S13|
||S2.6|Hierarchical equations of motion<br>. . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|S15|
||S2.7|Quantum optimal control<br>. . . . . . . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|S18|
||S2.8|Time-dependent product formulas<br>. . . . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|S23|
||S2.9|Time-evolving block decimation (TEBD) . . . .|. . . . . . . . . . . . . . . . . . . . . . . . . .|S26|
||S2.10Phase diagrams of quantum systems . . . . . .||. . . . . . . . . . . . . . . . . . . . . . . . . .|S29|
||S2.11Bell-state correlations under depolarizing noise||. . . . . . . . . . . . . . . . . . . . . . . . . .|S32|
||S2.12Estimating qubit requirements for quantum simulation . . . . . . . . . . . . . . . . . . . . . .|||S35|
||S2.13Quantum Error Correction<br>. . . . . . . . . . .||. . . . . . . . . . . . . . . . . . . . . . . . . .|S38|
|**S3 **|**Evaluation Rubrics**|||**S40**|



2 

## **1 Introduction** 

**==> picture [236 x 235] intentionally omitted <==**

The simulation of quantum systems is central to modern science, providing a systematic way to predict, interpret, and design phenomena governed by quantum mechanics. Across quantum chemistry (1; 2), condensed-matter physics (3; 4; 5), quantum optics (6; 7), high-energy (8; 9), and materials science (10; 11), a wide range of experimentally relevant observables ultimately require solving, exactly or approximately, the dynamics and/or stationary properties of an underlying quantum system Hamiltonian. In this sense, quantum simulation serves as a computational substrate that connects Hamiltonian models to measurable outcomes, enables systematic validation and refinement of theoretical approximations, and provides access to regimes otherwise inaccessible to direct analysis or experiments. 

Despite its importance, quantum simulation remains difficult to access broadly (12). A core obstacle is that the problem size grows exponentially **Figure 1** Schematic overview of El Agente Cuántico, with system size, making realistic calculations indetailing its capabilities (upper half) and the integrated feasible without strong approximations, careful nuhigh-performance software stack and tools (bottom half). merical checks, and substantial computing resources (13; 14). Furthermore, even when powerful techniques are available, such as tensor network methods in suitable many-body regimes (15; 16; 17), efficient open system solvers (18; 19; 20), and variational approaches (21; 22; 23; 24; 25; 2), implementing them requires specialized expertise. However, the users, in general, are not all-around specialists in the theory or software ecosystem, and even experts rarely know how to employ right off-the-bat every part of an end-to-end toolchain. As a result, researchers must invest substantial effort in learning new packages, assembling workflows, diagnosing failures, maintaining compatibility across environments, and adapting to different tool interfaces (26; 27; 28). This overhead often exceeds the time spent on the scientific question itself, and it slows the path from a concrete idea to a working simulation whose results can be trusted. 

Large language models (LLMs) offer a potential path to lowering the entry barrier to performing quantum simulations (29; 30). Through large-scale pretraining and post-training methods such as reinforcement learning, modern models acquire broad technical knowledge and can apply it through in-context learning (31; 32; 33). This makes it possible to express simulation intent in natural language and have the system map that intent to concrete implementation choices, including algorithms, software libraries, parameter settings, and correctness checks (34; 35; 36). Reasoning models have further improved multi-step planning, code synthesis, and iterative self-correction (37; 34; 36). Representative examples include OpenAI o1 (38), DeepSeek R1 (39), Gemini 2.5 (40), and Nemotron 4 (41), together with detailed system and model cards that document training procedures, capabilities, and limitations for the GPT-5 series (42), Gemini models (43), and the Claude family (44). Consequently, LLMs are increasingly able to support workflows in which the model does not merely describe what to do but helps execute the steps that turn a scientific question into a working simulation. 

In parallel, a rapidly expanding ecosystem of scientific agent systems has emerged (45). General-purpose agents now demonstrate end-to-end research loops that integrate reasoning with tool use, encompassing literature survey, hypothesis generation, verification, implementation, and reporting.(46) NovelSeek (47) is an early example that explores end-to-end hypothesis generation and validation. PaperQA (48) advances literature search and retrieval by enabling question answering over full-text scientific papers. The Kosmos agent (49) spans literature search, ideation, implementation, and report generation across domains such as biology and materials science. The Virtual Lab (50) demonstrates collaborative AI agents that design and experimentally validate scientific discoveries. The AI Scientist (51; 52) executes independent research workflows in machine learning tasks. 

3 

Alongside these general-purpose systems, domain-specific agents are gaining traction in settings that demand specialized tools and deep expertise. In scientific research orchestration, ORGANA (53) is a domain-specific agent that structures and coordinates complex research workflows by operating over formalized scientific artifacts, objectives, and constraints, rather than acting as an unconstrained general-purpose assistant. In chemistry, early systems such as ChemCrow (54) and Coscientist (55) demonstrated the potential of tool-using agents, while more recent work, including ChemAgent (56), extends this paradigm through multi-agent coordination for literature reasoning and complex laboratory operations. In quantum chemistry and electronic structure, El Agente Q (57) targets ab initio simulation workflows by translating high-level scientific objectives into executable computational pipelines. In physics, SciExplorer (58) uses a single LLM agent with access to general-purpose coding and analysis tools to infer equations of motion or Hamiltonians of initially unknown systems from simulated data. In mathematics, Ax Prover (59) is a multi-agent system for automated theorem proving that can operate autonomously or in collaboration with human experts. In astronomy, StarWhisper Telescope (60) automates observational planning and data processing. In scholarly communication and biological research, DORA (61) is a domain-specific agent for academic writing, producing publication-ready manuscripts from structured scientific sources. 

In quantum computing and hardware, AI for quantum computing and agent-based approaches to quantumphysics research have been gaining traction.(62; 63) For example, _k_ -agents (64) provide a framework for autonomously calibrating superconducting qubit experimental devices, QCR-LLM (65) integrates quantum algorithms for combinatorial problems in the reasoning process of LLMs, and PhIDO (66) addresses automated design of integrated photonic circuits. Furthermore, Saggio et al. (67) report an experimental reinforcementlearning demonstration on a programmable integrated nanophotonic platform, Elliott et al. (68) introduce quantum adaptive agents with efficient long-term memory for learning in partially observed/non-Markovian environments, Thompson et al. (69) analyze energetic advantages for quantum agents executing complex online strategies and Yun et al. (70) propose multi-agent reinforcement learning using variational quantum circuits. Quantum-agentic platforms that define quantum agents and outline hybrid architectures have also been proposed (71). Lemma (72), a commercial tool developed by Axiomatic uses an agentic system to create mathematical models (digital twins) of physics publications. Similarly, Kipu Quantum outlines a roadmap toward market-ready QC and QC+AI products built around platform-based solutions and iterative customer feedback.(73) 

Motivated by these developments, and leveraging our previous work and infrastructure on El Agente Q(57), we introduce El Agente Cuántico, a multi-agent system designed to automate quantum simulation workflows by translating natural language prompts into executed and validated computations over a high-performance quantum software stack (see Fig. 1). The system is grounded in the surrounding software ecosystem through direct access to library documentation and usage examples, which it leverages to recover the relevant APIs and implementation details needed to generate and run code end-to-end. More broadly, this reasoning guided deep research into documentation, which offers an efficient mechanism for software adaptation, enables the agent to rapidly align with new libraries, evolving interfaces, and domain-specific conventions. 

The remainder of the paper is organized as follows. Section 2 presents the architecture and overall design of the multi-agent system. Section 3 tackles representative examples across a broad range of quantum simulation tasks. Section 4 evaluates the robustness and reproducibility of El Agente Cu’antico through systematic benchmarks based on repeated and independent executions of representative problems. Section 5 addresses problems that extend beyond quantum simulations. Section 6 discusses the broader implications and limitations of the proposed approach, and outlines a strategic roadmap for El Agente Cuántico. Finally, in Section 7, we present the concluding remarks. 

## **2 Architecture of El Agente Cuántico** 

El Agente Cuántico uses the cognitive architecture of El Agente (57), designed to enhance the agent’s reasoning, execution, and long-term operation. As a novelty, we deliberately employ a minimalist agent architecture designed to exploit the intrinsic reasoning and execution capabilities of state-of-the-art large language models, rather than constraining behavior through extensive human-crafted tools, prompts, or rigid workflows. The system consists of a set of high-capacity LLM nodes, one per software, connected through a 

4 

central orchestrator that solely coordinates data exchange, inter-software execution, and user interfacing (see Fig. 2). 

Our agent’s architecture incorporates expert agents on quantum software frameworks and platforms, including the general-purpose CUDA-Q(74) programming platform for high-performance quantum simulation workflows, PennyLane for quantum and hybrid programming (75), Qiskit for quantum circuit development and execution (76), QuTiP for general open and closed quantum systems simulation (77), TeNPy for tensor-network simulations (78), and Tequila for flexible quantum algorithm design (79). 

Each agent consists of an LLM that operates with minimal persistent context and without a domain-specific tool or engineered cognition (80; 81; 82). Instead, agents dynamically invoke targeted web search to retrieve software documentation or scientific literature, and Python code for execution. This design contrasts with many other agentic frameworks that rely on large libraries of human-engineered tools, long contextual instructions or reasoning workflows, and task-specific decomposition policies, which can inadvertently limit adaptability and induce brittle behavior when confronted with unanticipated scientific questions. By keeping the agents comparatively “free” of imposed structure, our approach emphasizes model-internal abstraction and on-demand knowledge acquisition from primary sources, aligning more closely with how human researchers interact with computational tools and documentation. In this sense, our architecture exploits intrinsic LLM capabilities for task execution while being optimized for method discovery in open-ended research settings. 

Current quantum-simulation software can be combined, but typically only through workflows that are fixed in advance by developers or users. For example, a researcher may decide ahead of time which program is responsible for generating a circuit, which one runs the simulation, and which one analyzes the results, and then manually connect these steps. In El Agente Cuántico, the “quantum simulations expert” instead makes these decisions at runtime based on the scientific goal, choosing how to connect available tools on demand. This allows simulation workflows to adapt to the problem rather than being constrained by predefined software pipelines. 

## **3 Experiments for quantum simulations** 

Quantum simulation refers to the use of computational methods to approximate the properties and dynamics of quantum systems starting from an underlying Hamiltonian description. Depending on the physical setting and the observables of interest, this may involve preparing quantum states, simulating real- or imaginary-time evolution, or computing expectation values under unitary or effective non-unitary dynamics. 

For closed quantum systems, time evolution is commonly governed by the Schrödinger equation, 

**==> picture [292 x 22] intentionally omitted <==**

Solving Equation (1) requires specifying an initial state _|ψ_ (0) _⟩_ and a Hamiltonian _H_ ( _t_ ), which may be time-dependent or time-independent. In practice, the exponential growth of the Hilbert space with system size makes exact solutions intractable beyond small systems. This motivates the use of approximate simulation strategies that balance accuracy, computational cost, and applicability across different physical regimes, and that often require careful choices of algorithms, software tools, and validation procedures. 

In this section, we benchmark the ability of El Agente Cuántico to autonomously translate naturallanguage scientific intent into executed and validated quantum-simulation workflows. Rather than providing a comprehensive review of the underlying techniques, each subsection focuses on a concrete simulation task and evaluates whether the agent can identify appropriate algorithms, software tools, and validation strategies directly from the prompt. The examples are organized by task type — state preparation, timeindependent dynamics, and time-dependent dynamics — and together span a representative cross-section of quantum-simulation methodologies used in current practice. 

For each example, we begin with a brief introduction to the relevant scientific context of the problem, followed by a summary of the task posed to the agent, the aspects of El Agente capability showcased by the example, and the agents and software tools involved in the run. We then present the prompt provided to the agent and its corresponding response. For clarity, the agent’s response shown in the blue box corresponds to a 

5 

**==> picture [378 x 329] intentionally omitted <==**

**Figure 2** Multiagentic architecture of El Agente Cuántico. The central agent orchestrates different experts capable of designing and executing code using a specific quantum simulation package. 

lightly edited version of its original output, modified solely for conciseness. Detailed descriptions of the agent available tools, and the complete unedited interaction logs for all experiments are provided in the Supporting Information (Secs. S1 and S2). 

## **3.1 State preparation** 

## **3.1.1 Variational quantum eigensolver (VQE)** 

This method provides a practical approach for computing molecular ground states on noisy intermediate-scale quantum hardware (21). The method begins by selecting a parametrized ansatz _|ψ_ ( _θ_ ) _⟩_ , where _θ_ denotes the set of variational parameters that control the quantum circuit used to prepare the state. The algorithm relies on the variational principle, 

**==> picture [124 x 11] intentionally omitted <==**

which states that the expectation value of the Hamiltonian _H_ over any trial state provides an upper bound to the exact ground-state energy _E_ 0. Minimizing _E_ ( _θ_ ) over _θ_ therefore approximates the true ground state. 

To evaluate the energy on a quantum device, the molecular electronic Hamiltonian is mapped to a qubit Hamiltonian through a fermion-to-qubit encoding such as Jordan–Wigner (83; 14; 84) or Bravyi–Kitaev (85). This yields an operator decomposition of the form 

**==> picture [60 x 22] intentionally omitted <==**

where the coefficients _hi_ are real scalars determined by the one- and two-electron integrals, and the _Pi_ are 

6 

tensor products of Pauli operators acting on the qubit register. The corresponding expectation values _⟨Pi⟩θ_ are obtained by repeated measurement of the ansatz state on the quantum device. 

The VQE algorithm proceeds iteratively: (1) prepare the parametrized state _|ψ_ ( _θ_ ) _⟩_ on the quantum hardware, (2) measure the expectation values _⟨Pi⟩θ_ and reconstruct the energy _E_ ( _θ_ ), (3) compute a classical update of the parameters _θ_ using an optimization routine, and (4) repeat until convergence. 

For molecular benchmarks, we employ the unitary coupled-cluster singles and doubles (UCCSD) ansatz, which incorporates electron correlation through an anti-Hermitian excitation operator (86; 87; 88), 

**==> picture [114 x 14] intentionally omitted <==**

where _|ϕ_ HF _⟩_ is the Hartree–Fock reference state and 

**==> picture [178 x 28] intentionally omitted <==**

contains the single- and double-excitation operators in second quantization. Here, _i, j_ label occupied orbitals, _a, b_ label virtual orbitals, and _a[†] p_[/] _[a][p]_[denote][fermionic][creation][and][annihilation][operators.][The][unitary][form] ensures norm preservation and provides a systematically improvable, chemically motivated ansatz. 

**What we asked.** We asked El Agente Cuántico to read the CUDA-Q manual and compute the VQE ground-state energy of H2 over bond distances from 0.4 to 2.2 Å, benchmark against the exact energies, and generate/interpret a dissociation-curve plot. 

**What this showcases.** This example tests end-to-end autonomy for a standard chemistry workflow: selecting an ansatz (UCCSD), executing a parameter sweep, validating against a reference method, and producing publication-quality plots plus a physically meaningful error analysis. 

**Used agent/tools:** quantum scientist agent, cudaq expert agent, deepsearch, python REPL, submit python jobs and view png file, see supplementary information for detailed description. The answer was verified to be correct. 

**Prompt** Read the CUDA-Q manual and compute the VQE energy of H2 over bond distances from 0.4 to 2.2 Å and compare against the exact answer. For the plot, create a figure of the dissociation curve and explain the physical meaning and where the curve deviates from exact energies. 

7 

## **Response** 

**Left panel, PES.** Morse-like potential with equilibrium at 0.70 Å. VQE (coral circles) perfectly overlaps Exact (navy dots) while HF (teal) diverges catastrophically at stretched geometries. 

**Right panel, Errors.** Log scale (10 _[−]_[6] to 10[4] mHa) reveals 5 orders of magnitude separating VQE errors ( _∼_ 10 _[−]_[4] mHa) from HF errors ( _∼_ 10[2] mHa), with chemical accuracy threshold clearly in between. 

**Static correlation.** HF fails because a single Slater determinant cannot represent the entangled superposition needed for correct dissociation. VQE’s UCCSD ansatz captures this physics exactly. 

**==> picture [404 x 154] intentionally omitted <==**

**Figure 3** Plots generated by El Agente Cuántico. On the left, potential energy surface (PES) of H2 computed via VQE with the UCCSD ansatz, compared to FCI and HF. On the right, absolute energy errors on a log scale. 

## **3.1.2 Bell state preparation** 

Bell states are canonical examples of maximally entangled two-qubit states and serve as foundational resources in quantum information science (89). The state ( _|_ 00 _⟩_ + _|_ 11 _⟩_ ) _/√_ 2, first discussed in the context of quantum nonlocality by Bell (90), exhibits perfect correlations in both the Z and X measurement bases. Individual outcomes remain random, while joint statistics cannot be explained by any classical model that assumes local realism. Owing to this structure, Bell states support central quantum protocols such as quantum teleportation (91), superdense coding (92), and a wide range of entanglement-based benchmarking methods (93). They therefore provide a minimal and analytically transparent setting for studying entanglement, coherence, and two-qubit observables using quantum hardware or simulators. 

**What we asked.** We asked El Agente Cuántico to read the CUDA-Q manual and implement a 2-qubit circuit that prepares the Bell state ( _|_ 00 _⟩_ + _|_ 11 _⟩_ ) _/√_ 2, then estimate _⟨Z ⊗ Z⟩_ (computational basis) and _⟨X ⊗ X⟩_ (X basis) from 4096-shot measurements, and plot/analyze the results. 

**What this showcases.** This example probes whether the agent can translate a minimal entanglement task into correct circuit construction, basis changes, statistics-to-observables postprocessing, and sanity-checking via the known ideal correlations. 

**Used agent/tools:** quantum scientist agent, cudaq expert agent, deepsearch, python REPL, submit python jobs and view png file, see supplementary information for detailed description. The answer was verified to be correct. 

**Prompt** Read the CUDA-Q manual and create a 2-qubit quantum circuit that prepares a Bell state ( _|_ 00 _⟩_ + _|_ 11 _⟩_ ) _/√_ 2. Start in _|_ 00 _⟩_ . Apply a Hadamard gate on qubit 0 and then a CNOT with control qubit 0 and target qubit 1. Measure both qubits in the computational _⟨Z⟩_ basis with 4096 shots and return the measurement counts. From those counts, compute and return the expectation value of _Z ⊗ Z_ . Then also estimate the expectation value of _X ⊗ X_ by measuring in the X basis, again with 4096 shots, and return both the counts and the estimated _⟨X ⊗ X⟩_ . Plot and analyze the results. 

8 

## **Response** 

**Left panel 1, Z-basis measurements.** The outcomes are nearly equally split between _|_ 00 _⟩_ (51 _._ 4%) and _|_ 11 _⟩_ (48 _._ 6%), with no occurrences of _|_ 01 _⟩_ or _|_ 10 _⟩_ . The slight imbalance from a 50/50 distribution is consistent with finite sampling noise from 4096 shots. 

**Left panel 2, X-basis measurements.** The near-50 _/_ 50 split persists in the X basis, confirming strong correlations in multiple measurement bases. Unlike classically correlated states, which appear uncorrelated in X, the Bell state exhibits correlations in both bases, enabling violations of Bell inequalities. 

**Left panel 3, Expectation values.** _⟨Z ⊗ Z⟩_ = +1 (perfect correlation in Z-basis), _⟨X ⊗ X⟩_ = +1 (perfect correlation in X-basis), _⟨Y ⊗ Y ⟩_ = _−_ 1 (perfect anti-correlation in Y-basis). The combination (+1 _,_ +1 _, −_ 1) uniquely identifies _|_ Φ[+] _⟩_ among the four Bell states. 

**==> picture [404 x 134] intentionally omitted <==**

**Figure 4** Plots generated by El Agente Cuántico characterizing a 2-qubit Bell state prepared on a quantum simulator. The left and center panels show measurement counts in _Z_ and _X_ bases. The right panel shows the qubit correlations _⟨Z ⊗ Z⟩_ , _⟨X ⊗ X⟩_ , and _⟨Y ⊗ Y ⟩_ . 

## **3.1.3 Thermal states via imaginary-time evolution** 

Preparing thermal states of interacting many-body systems is a central task in quantum simulation. At inverse temperature _β_ = 1 _/T_ , the equilibrium state is described by the Gibbs density matrix, 

**==> picture [150 x 23] intentionally omitted <==**

which encodes the thermodynamic and correlation properties of the system. For lattice models such as the one-dimensional Hubbard Hamiltonian (94), 

**==> picture [194 x 26] intentionally omitted <==**

imaginary-time evolution (95; 96) provides a practical classical approach to approximating _ρ_ ( _β_ ) by evolving an initial state under _e[−][βH]_ . The resulting state can be validated by examining thermodynamic observables such as the temperature dependence of the energy and local occupancies. 

**What we asked.** We asked El Agente Cuántico to read the TenPy manual and compute the entanglement entropy for the 1D Bose–Hubbard model using purification-based imaginary-time evolution with a second-order Trotterization. 

**What this showcases.** This example evaluates whether the agent can move beyond simple state preparation and correctly set up tensor-network finite-temperature machinery (purification + imaginary time), while producing a quantitative observable (entanglement entropy) from the resulting state. 

**Used agent/tools:** quantum scientist agent, tenpy expert agent, deepsearch, python REPL, submit python jobs and view png file, see supplementary information for detailed description. The answer was verified to be correct. 

9 

**Prompt** Prepare a Gibbs state of a 1D Hubbard model on a classical computer using imaginary-time evolution. Consider a 10-site Hubbard chain with open boundary conditions, hopping _t_ = 1, on-site interaction _U_ = 4, and half filling. Target an inverse temperature 1 _/T_ = 2. Explain how to validate that the resulting state is thermal by checking energies and occupancies. 

## **Response** 

**Panel (a), energy vs 1/T.** As temperature decreases, the Boltzmann distribution favors lower-energy states, so the average energy drops monotonically toward the ground state. 

**Panel (b), site occupancy.** The canonical ensemble at fixed _N_ = 10 electrons maintains exactly one electron per site on average, as expected for half-filling. 

**Panel (c), double occupancy.** The strong on-site repulsion _U_ = 4 suppresses double occupancy by 64%. This is the hallmark of Hubbard physics—electrons avoid sharing sites due to Coulomb repulsion. 

**Panel (d), entanglement entropy.** Von Neumann entropy S at each bond cutting the chain. The purification MPS has entanglement from both quantum correlations and thermal mixing. Higher entropy at the center is typical for finite systems with open boundaries. 

**==> picture [359 x 294] intentionally omitted <==**

**Figure 5** Plots generated by El Agente Cuántico preparing and validating a thermal state of a 10-site Hubbard chain using imaginary-time evolution. 

## **3.2 Time-independent Hamiltonian simulation** 

## **3.2.1 Trotter decomposition** 

When simulating the dynamics of Hamiltonians of the form _H_ = _H_ 1 + _H_ 2 + _· · ·_ + _Hn_ , where [ _Hi, Hj_ ] _̸_ = 0 for _i_ = _j_ and each _Hi_ is easily diagonalizable, it is common to perform Trotterization (97). This method is a standard technique for simulation using quantum computers and approximates the exponential of _H_ by _r_ 

10 

repetitions of the individual dynamics of each _Hj_ , 

**==> picture [102 x 31] intentionally omitted <==**

There are multiple ways to compute the products of single-term exponentials to obtain a better approximation of _e[iHt]_ . For example, high-order product formulas (98) or corrected product formulas (99) achieve better error scaling than the first-order approximation mentioned before. 

**What we asked.** We asked El Agente Cuántico to simulate closed-system time evolution for a timeindependent Hamiltonian using a Trotterized product-formula approach, including an explicit comparison/validation against a reference evolution where possible. 

**What this showcases.** This example focuses on method selection for Hamiltonian simulation (product formulas) and tests whether the agent can reason about algorithmic accuracy (step size/Trotter error), implement the workflow in a concrete software stack, and validate dynamics with a controlled benchmark. 

**Used agent/tools:** quantum scientist agent, cudaq expert agent, deepsearch, python REPL, submit python jobs and view png file, see supplementary information for detailed description. The answer was verified to be correct. 

**Prompt** Read the CUDA-Q manual and implement a simulation of the transverse-field Ising model for a 10-qubit chain with open boundary conditions. Compute the dynamics of the magnetization _⟨Z⟩_ for two parameter regimes, _J_ coup = 10 _J_ with _h_ = 0 _._ 1 _J_ , and _J_ coup = 0 _._ 1 _J_ with _h_ = 10 _J_ . Start the evolution from a Haar-random initial state and simulate the dynamics over a total time of 10 seconds using a second-order product formula with 1000 time steps. Generate a heatmap where the x-axis corresponds to qubit position, the y-axis to time, and the color scale to the _Z_ -magnetization, for each of these two phases. Analyze the resulting magnetization dynamics between the two parameter choices. 

11 

## **Response** 

**Left panel, strong coupling.** Slow, smooth dynamics dominated by _ZZ_ interactions; coherent spatial correlations across the chain; and spatial structure reflecting collective behavior. 

**Right panel, strong field.** Fast oscillatory dynamics with horizontal banding; nearly independent qubit precession at frequency _∼_ 2 _h_ ; rapid oscillation period around 0 _._ 06 s; and weak inter-qubit correlations due to small coupling. 

The contrast clearly illustrates the quantum phase transition behavior of the Transverse-field Ising model: the ferromagnetic phase (strong coupling) vs. the paramagnetic phase (strong field). 

**==> picture [404 x 179] intentionally omitted <==**

**Figure 6** Plots generated by El Agente Cuántico time evolving a 10-qubit transverse-field Ising chain using Trotterization in two parameter regimes: strong coupling (left) and strong field (right). 

## **3.2.2 Open systems dynamics using the Lindblad approximation** 

Realistic quantum systems interact with surrounding degrees of freedom, which leads to decoherence (100; 101; 102; 103; 104) and dissipation (105; 106; 107; 108; 109) that cannot be captured by unitary evolution. In such cases, the dynamics of the reduced density matrix _ρ_ ( _t_ ) is described by a quantum master equation. Under the assumptions of complete positivity, trace preservation, and Markovianity, the generator of the evolution takes the Gorini–Kossakowski–Sudarshan–Lindblad (GKSL) form (110; 111; 112) 

**==> picture [302 x 26] intentionally omitted <==**

where the dissipator is defined as 

**==> picture [306 x 14] intentionally omitted <==**

The operators _Ck_ represent environmental channels and determine how populations and coherences decay. The GKSL structure ensures that the evolution remains physical and preserves positivity and the trace of the density matrix. 

For a single qubit, the Lindblad equation provides a clear description of how coherent Bloch sphere motion competes with irreversible relaxation. A standard example is amplitude damping generated by _C_ = _[√] γ σ−_ , which drives population from the excited state to the ground state at rate _γ_ while attenuating coherences. The expectation value 

**==> picture [277 x 11] intentionally omitted <==**

highlights the contrast between closed- and open-system evolution. Unitary dynamics generates undamped oscillations, whereas in the presence of dissipation, the trajectories decay toward the stationary state. 

12 

QuTiP (77) provides efficient solvers for the numerical propagation of Schrödinger and Lindblad equations. The following example illustrates how El Agente Cuántico uses this functionality to model dissipative single-qubit dynamics. 

**What we asked.** We asked El Agente Cuántico to read the QuTiP manual and compare a single qubit’s dynamics under (i) unitary evolution and (ii) Lindblad evolution, for _H_ = _σx_ +[1] 2 _[σ][z]_[,][initial] _[X]_[eigenstates] _|_ + _⟩, |−⟩_ , and a decay channel _C_ = _[√] γσ−_ with _γ_ = 0 _._ 2, reporting _⟨Z_ ( _t_ ) _⟩_ over _t ∈_ [0 _,_ 40]. 

**What this showcases.** This example tests solver/tool choice (Schrödinger vs. master equation), correct handling of collapse operators and expectations, and the agent’s ability to present a clear closed-vs-open comparison plot and interpretation. 

**Used agent/tools:** quantum scientist agent, qutip expert agent, deepsearch, python REPL, submit python jobs and view png file, see supplementary information for detailed description. The answer was verified to be correct. 

**Prompt** Read the QuTiP manual and compare the dynamics of a single qubit under unitary evolution and under open system Lindblad evolution using: 

**Hamiltonian:** _H_ = _σx_ +[1] 2 _[σ][z]_[,] **[Initial condition:]**[Use][the][plus][and][minus][eigenstates][of][X.] **[Dissipation:]**[Use][a] collapse operator _C_ = _[√] γσ−_ , with _γ_ = 0.2. **Evolution:** Use a time range from _t_ = [0 _,_ 40] with 400 time steps. **Output:** Plot the expectation value of Z as a function of time for each initial state and compare closed and open dynamics. 

## **Response** 

**Panel (a), Unitary Evolution:** Shows persistent Rabi-like oscillations for both _|_ + _⟩_ (dark blue, solid) and _|−⟩_ (light blue, dashed) initial states with amplitude _∼_ 0.4 

**Panel (b), Lindblad Evolution:** Shows damped oscillations converging to a steady state with a horizontal dashed line at _⟨Z⟩≈_ -0.33 

**Physical interpretation:** The Hamiltonian _H_ = _σx_ + 0 _._ 5 _σz_ creates a tilted effective magnetic field causing Rabi-like precession. The collapse operator _C_ = _[√] γσ−_ induces spontaneous emission ( _|_ 1 _⟩→|_ 0 _⟩_ decay). Competition between coherent driving (H) and dissipation ( _γ_ ) produces a non-trivial steady state where _∼_ 67% population is in _|_ 0 _⟩_ . Crucially, the steady state is unique. Both initial states converge to the same value, demonstrating loss of memory of initial conditions (a hallmark of open quantum systems). 

**==> picture [448 x 168] intentionally omitted <==**

**Figure 7** Plots generated by El Agente Cuántico comparing the oscillatory behaviour of unitary and Lindblad dynamics on a single qubit. 

13 

## **3.2.3 Hierarchical equations of motion (HEOM)** 

The hierarchical equations of motion provide a powerful and widely used framework for modeling open quantum dynamics when the assumptions underlying the Lindblad equation are no longer valid. Many condensed phase systems interact with environments characterized by strong coupling and long-lived correlations, which prevents a Markovian master equation from describing the evolution of the reduced density matrix. In the HEOM(113; 114) formalism, the system Hamiltonian _H_ evolves together with a hierarchy of auxiliary density operators that encode the full influence of the bath. This approach retains non-Markovian memory and offers an essentially exact treatment of dissipation for environments with structured spectral features. 

In practical applications, the bath is described by a spectral density, such as the Drude–Lorentz form, with parameters including the reorganization energy ( _λ_ ), the cutoff rate ( _γ_ ), and the temperature ( _T_ ). The corresponding bath correlation functions are written as sums of exponentials. Each exponential generates one level of auxiliary operators, whose couplings capture the exchange of coherence and population between the system and the environment. Truncation at a finite hierarchy depth ( _L_ ) together with a chosen number of Matsubara terms ( _K_ ) yields a controllable approximation that converges to the exact dynamics as these parameters are increased. QuTiP provides an efficient implementation of this method, enabling accurate simulation of excitonic dynamics on physically relevant timescales. 

**What we asked.** We asked El Agente Cuántico to use QuTiP’s HEOM implementation to simulate exciton population dynamics in the FMO complex at two temperatures (300 K and 77 K), propagating for 1 ps and plotting all site populations versus time with an analysis of temperature-dependent coherence. 

**What this showcases.** This example stresses a “heavier” open-quantum-systems workflow: selecting a specialized method (HEOM), executing it with realistic parameters, and extracting physically interpretable data from the computed trajectories. 

**Used agent/tools:** quantum scientist agent, qutip expert agent, literature search, deepsearch, python REPL, submit python jobs and view png file, see supplementary information for detailed description. The answer was verified to be correct. 

**Prompt** Read QuTiP’s manual and use the HEOM implementation to simulate exciton dynamics in the Fenna–Matthews–Olson (FMO) complex. Use the following parameters: 

**==> picture [366 x 97] intentionally omitted <==**

**----- Start of picture text -----**<br>
|||||||||||||||||||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|240|.|0|−|87|.|7|5|.|5|−|5|.|9|6|.|7|−|13|.|7|−|9|.|9|
|||
||−|87|.|7|315|.|0|30|.|8|8|.|2|0|.|7|11|.|8|4|.|3||
|||
||5|.|5|30|.|8|0|.|0|−|53|.|5|−|2|.|2|−|9|.|6|6|.|0||
|||
|System Hamiltonian|(115;|116;|117) =||−|5|.|9|8|.|2|−|53|.|5|130|.|0|−|70|.|7|−|17|.|0|−|63|.|3|.|
||6|.|7|0|.|7|−|2|.|2|−|70|.|7|285|.|0|81|.|1|−|1|.|3||
|||
||−|13|.|7|11|.|8|−|9|.|6|−|17|.|0|81|.|1|435|.|0|39|.|7||
|−|9|.|9|4|.|3|6|.|0|−|63|.|3|−|1|.|3|39|.|7|245|.|0|
|||

**----- End of picture text -----**<br>


**Bath parameter:** Drude–Lorentz spectral density with reorganization energy _λ_ = 35 cm _[−]_[1] , cutoff time 1 _/γ_ = 50 fs, and temperature _T_ = 300 K and _T_ = 77 K. Hierarchy depth _L_ = 4, number of Matsubara terms _K_ = 2. **Initial condition:** system localized on site 0. **Dynamics:** propagate for 1 ps and record site populations vs. time. **Report:** Plot all site populations as a function of time at the two different temperatures and analyze the results. 

14 

## **Response** 

**Left panel, T = 300 K.** The initially excited Site 0 decays smoothly from population 1.0 to about 0.27 with only weak oscillations. Population spreads broadly across the complex: Sites 1–3 each reach roughly 13–22 percent, and even high-energy Site 5 reaches about 4 percent. The overall behavior is predominantly incoherent and diffusive. 

**Right panel, T = 77 K.** Site 0 undergoes a rapid drop in the first _∼_ 100 fs followed by clear oscillations and partial recovery, retaining about 46 percent population at 1 ps. Oscillatory features appear across several sites, and population remains concentrated on lower-energy sites (mainly 2 and 3), while higher-energy sites (4–6) stay below 2 percent. The dynamics are more coherent and wavelike than at room temperature. 

## **Consistency with Literature** 

- The energy funnel behavior toward Site 3 (BChl 3) is well-documented 

- Temperature-dependent rates agree with theoretical predictions 

**==> picture [400 x 146] intentionally omitted <==**

**Figure 8** Plots generated by El Agente Cuántico simulating exciton dynamics in the FMO complex using HEOM at two temperatures: 300 K (left) and 77 K (right). 

## **3.3 Time-dependent Hamiltonians** 

## **3.3.1 Quantum optimal control** 

Quantum optimal control provides a principled way to design time-dependent fields that guide a system toward a chosen target state with high fidelity. The Gradient Ascent Pulse Engineering (GRAPE) algorithm (118) is widely used because it computes analytic gradients of the fidelity with respect to the controls, thereby enabling efficient optimization over large pulse parametrizations. A Lambda type three-level system offers a simple and instructive platform for this task (119). The states _|_ 1 _⟩_ , _|_ 2 _⟩_ , and _|_ 3 _⟩_ are connected through two independent control Hamiltonians that couple _|_ 1 _⟩_ to _|_ 2 _⟩_ and _|_ 2 _⟩_ to _|_ 3 _⟩_ . The objective is to maximize population transfer from the initial state _|_ 1 _⟩_ to the target state _|_ 3 _⟩_ while suppressing occupation of the intermediate state _|_ 2 _⟩_ . This setting provides a clear benchmark for gradient-based optimization and illustrates how GRAPE identifies high-fidelity solutions that exploit coherent control pathways within the system Hamiltonian. 

**Whatweasked.** We asked El Agente Cuántico to read QuTiP manual and solve a GRAPE optimal-control problem for a Λ-type three-level system, transferring population _|_ 1 _⟩→|_ 3 _⟩_ while minimizing occupation of _|_ 2 _⟩_ . 

**What this showcases.** This example shows that the agent can run a full optimization-and-validation loop: mapping a control objective to the correct library routines, handling time-dependent controls, and producing diagnostics that expose both success (high fidelity) and limitations of the chosen cost function. 

**Used agent/tools:** quantum scientist agent, qutip expert agent, deepsearch, python REPL, submit python jobs and view png file, see supplementary information for detailed description. The answer was verified to be correct. 

15 

**Prompt** Read the QuTiP manual and solve a quantum control problem for a Λ-type three-level system (levels _|_ 1 _⟩_ , _|_ 2 _⟩_ , _|_ 3 _⟩_ ). The goal is to transfer population from the ground state _|_ 1 _⟩_ to the target state _|_ 3 _⟩_ while minimizing the occupation of the intermediate state _|_ 2 _⟩_ . 

**Control Hamiltonians:** _Hc_ 1 = ( _|_ 1 _⟩⟨_ 2 _|_ + _|_ 2 _⟩⟨_ 1 _|_ ) (Pump coupling). _Hc_ 2 = _|_ 2 _⟩⟨_ 3 _|_ + _|_ 3 _⟩⟨_ 2 _|_ ) (Stokes coupling). **The Optimization:** Use the GRAPE algorithm. **Duration:** T=40 (arbitrary time units) with time slots = 3000. **Validation:** After optimizing the pulses, run a time-evolution simulation using the generated pulses to verify the dynamics. **Output:** A plot showing the Control Pulses (Amplitude vs Time) and a plot showing the populations vs Time. Print the final fidelity. 

## **Response** 

**Left panel (Control pulses):** Both pulses are oscillatory and overlap in time. 

**Right panel (Populations):** _P_ 1 (blue): Smoothly depletes from 1 _→_ 0. _P_ 2 (orange): Peaks at 83% mid-transfer, return to 0. _P_ 3 (green): build to _∼_ 1 _._ 0 (99.99999% fidelity) 

**Important Note:** The standard GRAPE algorithm optimizes only for final state fidelity, not for minimizing intermediate state occupation during the transfer. The solution found is mathematically optimal for the endpoint but does NOT minimize _|_ 2 _⟩_ occupation during evolution. 

**==> picture [448 x 111] intentionally omitted <==**

**Figure 9** Plots generated by El Agente Cuántico solving a quantum optimal control problem for a Lambdatype three-level system using the GRAPE algorithm. The left panel shows the control pulses, and the right panel shows the state populations over time. 

## **3.3.2 Time-dependent product formulas** 

Product formulas can also be used for simulating time-dependent Hamiltonians (120). A common example of these Hamiltonians is Floquet models, such as kicked systems (121), which are periodically updated by instantaneous changes to the Hamiltonian every period _T_ . The standard form of such Hamiltonian is given by 

**==> picture [142 x 29] intentionally omitted <==**

Simulating the dynamics of these systems requires approximating the time-ordered exponential of the Hamiltonian: 

**==> picture [313 x 26] intentionally omitted <==**

Here, we show El Agente Cuántico approximating the Floquet dynamics of a kicked Ising chain using product formulas implemented in CUDA-Q. 

**What we asked.** We asked El Agente Cuántico to read the CUDA-Q manual and simulate Floquet dynamics of a periodically kicked Ising chain (10 qubits, open boundaries) using time-dependent productformula methods, then visualize and analyze the resulting driven dynamics. 

**What this showcases.** This example tests whether the agent can correctly translate a time-ordered exponential problem into an implementable Floquet step (drift + kicks), choose an appropriate simulation strategy in CUDA-Q, and extract time-domain signatures of nontrivial driven behavior. 

16 

**Used agent/tools:** quantum scientist agent, cudaq expert agent, deepsearch, python REPL, submit python jobs and view png file, see supplementary information for detailed description. The answer was verified to be correct. 

## **Prompt** 

Read CUDA-Q manual and simulate the Floquet dynamics of a periodically kicked Ising chain with 10 qubits and open boundary conditions. The system has nearest-neighbor _ZZ_ interactions with coupling _J_ = 1, and is kicked every _T_ = 1 by a global transverse field in X. Use a strong kick with strength _h_ = 2 _J_ so that the effect of the drive is clearly visible in the dynamics. Initialize the system in a Haar-random state and simulate the evolution for 10 Floquet periods. Plot a heatmap of _⟨Zi_ ( _t_ ) _⟩_ , with qubit index on the x-axis, Floquet step (time) on the y-axis, and color representing the local magnetization. 

## **Response** 

We observe irregular red–blue patches fluctuating around white, with all magnetization values remaining very small ( _∥⟨Z⟩∥ <_ 0 _._ 09). There is no discernible spatial pattern or temporal ordering. 

## **Physical interpretation.** 

- **Thermalization:** The near-zero magnetization across the entire space–time grid indicates that the system has effectively thermalized to an infinite-temperature state, as expected for chaotic Floquet dynamics. 

- **Scrambling:** The rapid, sign-changing fluctuations reflect strong information scrambling. The large kicks ( _h_ = 2 _J_ ) drive efficient mixing of quantum states and suppress any coherent structure. 

The featureless, noise-like fluctuations around zero confirm that the kicked Ising chain is deep in the chaotic regime, acting as a quantum thermalizer rather than supporting stable or long-lived coherent dynamics. 

**==> picture [270 x 214] intentionally omitted <==**

**Figure 10** Plots generated by El Agente Cuántico simulating the Floquet dynamics of a kicked Ising chain using time-dependent product formulas. The heatmap shows the local magnetization _⟨Zi_ ( _t_ ) _⟩_ over space and time. 

## **3.3.3 Time-evolving block decimation (TEBD)** 

Many interesting phenomena in quantum dynamics arise from time-dependent Hamiltonians. An example of such is Floquet time crystals (FTC) (122; 123). These systems are characterized by having a _T_ -periodic Hamiltonian _H_ ( _t_ + _T_ ) = _H_ ( _t_ ), but there exists an order parameter _O_ with a longer than _T_ period, _⟨O_ ( _t_ + _nT_ ) _⟩_ = 

17 

_⟨O_ ( _t_ ) _⟩_ with _n >_ 1. When the lifetime of these oscillations is finite but long compared to the driving period, the system is called a prethermal Floquet time crystal (124). A common method to use for simulating the dynamics of one-dimensional quantum many-body systems is time-evolving block decimation (TEBD) (125; 126). Below, we show El Agente Cuántico simulating the dynamics of a prethermal Floquet time crystal using TEBD. 

**What we asked.** We asked El Agente Cuántico to simulate nonequilibrium dynamics of a 1D many-body system using TEBD (tensor-network time evolution), and to extract observables that diagnose the dynamical phase of interest. 

**What this showcases.** This example probes whether the agent can select and configure a tensor-network method, using TeNPy, appropriate for larger 1D systems, manage time stepping and truncation controls, and connect the computed observables to a clear physical conclusion (rather than only producing raw plots). 

**Used agent/tools:** quantum scientist agent, tenpy expert agent, literature search, deepsearch, python REPL, submit python jobs and view png file, see supplementary information for detailed description. The answer was verified to be correct. 

## **Prompt** 

Simulate Floquet dynamics with TD-DMRG for a 1D disordered spin-1/2 chain. Use a periodically driven Hamiltonian with period _T_ = _τ_ 1 + _τ_ 2. During 0 _< t < τ_ 1, evolve under a strong global _x_ -field plus interactions and disorder: _H_ =[�] _i_[Ω] _[x][S] i[x]_[+ ∆] _[i][S] i[z]_[+] _[ J]_[(] _[S] i[x][S] i[x]_ +1[+] _[ S] i[y][S] i[y]_ +1 _[−][S] i[z][S] i[z]_ +1[)][.][During] _[τ]_[1] _[< t < T]_[,] switch to a global _y_ -field, _H_ =[�] _i_[Ω] _[y]_[(1] _[ −][ε]_[)] _[S] i[y]_[+ ∆] _[i][S] i[z]_[+] _[ H][i,i]_[+1][.][Choose][Ω] _[x][τ]_[1] _[≈][π]_[so][each][period] approximately flips the _x_ -polarization. Use the following parameters: system size _L_ = 10 spins, maximum bond dimension _χ_ max = 100, time step _δt_ = 0 _._ 03, evolve for _N_ periods = 50 Floquet periods, average over _N_ disorder = 5 disorder realizations, and scan _ε ∈{_ 0 _,_ 0 _._ 15 _,_ 0 _._ 3 _}_ . Keep the Hamiltonian parameters as before: _J_ = 1, Ω _x_ = Ω _y_ = 4 _J_ , _τ_ 1 = _π/_ (2Ω _x_ ) _≈_ 0 _._ 393, _τ_ 2 = 0 _._ 5, and disorder strength _W_ = 2 _J_ . 

Initialize the system in a product state polarized along + _x_ . Evolve stroboscopically for many periods using TD-DMRG (TEBD or TDVP), keeping truncation errors under control. Use disorder ∆ _i ∈_ ( _−W, W_ ) and average over several realizations. After each Floquet period, measure the bulk _x_ -magnetization and plot it versus the number of periods. Vary _ε_ to identify regimes with long-lived period-doubling (subharmonic 2 _T_ oscillations) versus rapid decay due to heating. Track entanglement growth and discuss how it limits the reachable simulation time. 

18 

## **Response** 

**Panel (a) - Magnetization:** Stroboscopic _⟨S[x] ⟩_ vs Floquet period with clear period-doubling oscillations. The alternating pattern demonstrates discrete-time crystal behavior, with the decay depending on the imperfection _ε_ . 

**Panel (b) - Entanglement:** Slow logarithmic growth of entanglement entropy _S_ , confirming MBL protection ( _S ≈_ 2 _._ 0 _<<_ 3 _._ 47 thermal limit). 

Three curves for _ε ∈_ 0 _,_ 0 _._ 15 _,_ 0 _._ 3 with shaded error bands ( _±_ 1 _σ_ from disorder averaging). 

This simulation provides direct numerical evidence for the MBL-protected discrete time crystal phase: a driven quantum system that spontaneously oscillates at twice the driving period, protected from thermalization by many-body localization. 

**==> picture [404 x 159] intentionally omitted <==**

**Figure 11** Plots generated by El Agente Cuántico simulating a prethermal Floquet time crystal using TDDMRG (TEBD). Panel (a) shows the stroboscopic magnetization exhibiting period-doubling oscillations, and panel (b) shows the entanglement entropy growth over time. 

## **4 Reproducibility benchmark** 

To evaluate the robustness and reproducibility of El Agente Cuántico, we perform a systematic benchmark based on repeated, independent executions of representative quantum-simulation tasks. The aim of this benchmark is to assess consistency under identical prompts, rather than to optimize peak performance. We consider some of the problems introduced in the previous section, including variational quantum eigensolver (VQE) (Sec. 3.1.1), Bell-state preparation (Sec. 3.1.2), transverse-field Ising dynamics (Sec. 3.2.1), open-system Lindblad dynamics (Sec. 3.2.2), and hierarchical equations of motion (HEOM) (Sec. 3.2.3). For the VQE benchmark, we deliberately use the Tequila framework instead of CUDA-Q in order to test the agent’s performance across a different software stack. 

Each task is executed ten times using the same prompt, with all runs fully independent and no shared memory or persistent context between executions. Each run is evaluated by a human expert using a structured rubric that assesses three aspects, namely correctness of the implementation, quality and validation of the results, and clarity of the final report, with a maximum score of 100 points per run. Partial credit is assigned where appropriate. Five evaluators, consisting of two postdoctoral researchers and three PhD students, participate in the assessment, with a single evaluator assigned consistently to each benchmark task across all repetitions. The full evaluation rubric and detailed point assignments for each benchmark task are provided in the Supporting Information (Sec. S3). 

Table 1 summarizes the benchmark results. Across all tasks, the agent attains consistently high scores over repeated executions, demonstrating robust and reproducible performance across a diverse set of quantumsimulation problems and software frameworks. While the specific code generated by the agent may differ between runs, this variability reflects the existence of multiple valid implementations for the same physical 

19 

**Table 1** Reproducibility benchmark for El Agente Cuántico. Each benchmark task was executed independently ten times using identical prompts. Scores correspond to expert evaluation using a structured rubric with a maximum score of 100 per run. The detailed grading criteria and evaluation rubric are provided in the Sec. S3 of the Supporting Information. 

|**Task**|**Software**|**R1**|**R2**|**R3**|**R4**|**R5**|**R6**|**R7**|**R8**|**R9**|**R10**|**Average Score**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|VQE|Tequila|100|100|100|100|100|100|100|100|100|100|100|
|Bell state|CUDA-Q|100|100|100|100|100|100|100|100|100|80|98|
|Ising|CUDA-Q|100|100|100|90|100|90|100|100|100|100|98|
|Lindblad|QuTiP|100|100|100|100|70|100|100|100|100|100|97|
|HEOM|QuTiP|100|100|100|100|100|100|100|100|100|100|100|



task and does not affect the correctness of the results. Perfect reproducibility is observed for the VQE and HEOM benchmarks, where all repetitions yield fully correct implementations and analyses. 

The deviations from the maximum score can be attributed to isolated and well-defined issues that do not compromise the validity of the overall workflows. In the Bell-state benchmark, Run 10 produced correct data and executable code but exhibited minor visualization problems, including a missing axis label and overlapping annotations for which we deducted 20 points. In the Lindblad benchmark, Run 5 computed _⟨σy_ ( _t_ ) _⟩_ instead of the requested _⟨σz_ ( _t_ ) _⟩_ , for which a substantial score reduction was applied even though the dynamical simulation and physical interpretation were otherwise correct. For the transverse-field Ising benchmark, some variability across runs is expected because the dynamics originate from random initial states. Nonetheless, in Run 4 and Run 6 the initial states were random but not strictly Haar distributed, which motivated a small score reduction despite consistent physics and numerical evolution across repetitions. 

## **5 Beyond quantum simulation** 

Solving the Schrödinger equation, or an approximation of it, is often a step in a larger problem. In this section, we demonstrate the capabilities of El Agente Cuántico in solving problems beyond quantum simulation. This includes, for example, constructing phase diagrams of quantum systems, combining multiple toolkits to study quantum systems, estimating qubit requirements for quantum simulation and quantum error correction. 

## **5.1 Phase diagrams of quantum systems** 

Many-body quantum systems exhibit rich phase diagrams that can be explored through quantum simulation. Often, an order parameter is used to characterize the system’s different phases. An interesting example is found in the study of computational phases of quantum matter (127; 128). For example, it was shown that for the one-dimensional transverse field cluster Hamiltonian defined by, 

**==> picture [188 x 30] intentionally omitted <==**

the string-order parameter _⟨ZXIX · · · IXZ⟩_ can be used to identify if the ground state can be used for measurement-based quantum computation (MBQC) (129). We show El Agente Cuántico using tenpy (78) to compute the phase diagram of this model and estimate the computational phase transition with a simple but complete prompt below. 

**What we asked.** We asked El Agente Cuántico to use DMRG to compute the ground state of the 1D transverse-field cluster Hamiltonian (ring geometry), evaluate the nonlocal string-order parameter _ZXIX · · · IXZ_ for system sizes _N_ = 11 _,_ 21 _,_ 41, plot the order parameter versus coupling, and estimate the critical point. 

20 

**What this showcases.** This example tests autonomy on an end-to-end many-body study: selecting a tensornetwork ground-state algorithm, implementing a nonlocal diagnostic observable, performing finite-size comparisons, and extracting a phase-transition estimate from computed data. 

**Used agent/tools:** quantum scientist agent, tenpy expert agent, literature search, deepsearch, python REPL, submit python jobs and view png file, see supplementary information for detailed description. The answer was verified to be correct. 

**Prompt** Use DMRG to prepare the ground state of the one-dimensional transverse field cluster Hamiltonian over a ring of _N_ qubits (interpolate with cos and sin between these cluster Hamiltonian and the magnetic field). Compute the string-order parameter _ZXIX · · · IXZ_ for multiple strengths of the cluster Hamiltonian over 11, 21, and 41 qubits. Plot the string-order parameter as a function of the cluster Hamiltonian strength for the different system sizes and estimate the critical point. 

## **Response** 

I implemented DMRG simulations (tolerance 10 _[−]_[5] ) for the transverse field cluster Hamiltonian. 

**Physical Interpretation:** _•_ SPT Phase ( _θ < θc_ ): String order _O ≈_ 1, indicating symmetry-protected topological order _•_ Trivial Phase ( _θ > θc_ ): String order _θ →_ 0, no topological order _•_ Critical Point: _θc/π ≈_ 0 _._ 236 (extrapolated), close to theoretical _π/_ 4 = 0 _._ 25 _•_ The transition sharpens with increasing system size, consistent with a quantum phase transition. 

**==> picture [448 x 158] intentionally omitted <==**

**Figure 12** Plots generated by El Agente Cuántico simulating the computational phase diagram of the transverse field cluster Hamiltonian using DMRG. 

## **5.2 Bell-state correlations under depolarizing noise** 

Bell states provide a minimal setting to probe how entanglement degrades under realistic noise channels. Whereas the previous example considered an ideal implementation using CUDA-Q, here we test whether El Agente Cuántico can use the Qiskit framework to prepare the same Bell state and evaluate how depolarizing noise affects multi-basis quantum correlations. 

**What we asked.** We asked El Agente Cuántico to simulate Bell-state measurements in the presence of depolarizing noise and analyze how noise degrades correlations, including a comparison between measurement bases. 

**What this showcases.** This example highlights cross-tool robustness and “glue” reasoning: the agent must find a backend that actually supports noisy simulation in the installed environment, run the experiment, and interpret basis-dependent degradation as an accumulated-gate-error effect. 

**Used agent/tools:** quantum scientist agent, qiskit expert agent, literature search, deepsearch, python REPL, submit python jobs and view png file, see supplementary information for detailed description. The answer was verified to be correct. 

21 

**Prompt** Read the Qiskit manual and prepare the Bell state ( _|_ 00 _⟩_ + _|_ 11 _⟩_ ) _/√_ 2. Start in _|_ 00 _⟩_ , apply a Hadamard gate on qubit 0, and then a CNOT with control qubit 0 and target qubit 1. Add a depolarizing noise channel with probability _p_ to both qubits after the CNOT gate. Simulate the circuit for _p ∈{_ 0 _,_ 0 _._ 05 _,_ 0 _._ 1 _,_ 0 _._ 2 _,_ 0 _._ 3 _}_ . For each value of _p_ , run 4096 shots in the _Z_ basis, return the measurement counts, and compute _⟨Z ⊗ Z⟩_ . Then insert Hadamard gates on both qubits to measure in the _X_ basis, run 4096 shots, return the measurement counts, and compute _⟨X ⊗ X⟩_ . Plot both correlators as functions of _p_ and comment on how the noise degrades the Bell-state correlations. 

## **Response** 

**Physical interpretations.** The measurement count plots visually demonstrate that _•_ ideal Bell state produces only correlated outcomes ( _|_ 00 _⟩_ , _|_ 11 _⟩_ ) _•_ Depolarizing noise introduces anti-correlated outcomes ( _|_ 01 _⟩_ , _|_ 10 _⟩_ ) _•_ High noise limit: Distribution approaches uniform (maximally mixed state) _•_ X-basis degradation is 2-3x faster due to additional Hadamard gates also experiencing noise. 

**==> picture [359 x 330] intentionally omitted <==**

**Figure 13** Plots generated by El Agente Cuántico simulating Bell-states under depolarizing noise. The top plot shows 2-qubit correlations as a function of noise strength. The bottom plots show the tomographic measurement counts for different noise levels in both Z and X bases. 

## **5.3 Estimating qubit requirements for quantum simulation** 

Quantum computation is an emerging technology for simulating quantum systems. One of the most promising algorithms for estimating ground-state energies is quantum phase estimation (QPE) (130; 89), relevant for quantum chemistry applications (14). Below, we show the general structure of QPE for estimating the ground-state energy of a Hamiltonian _H_ using a unitary operator _U_ = _e[−][iHt]_ and an input state _|ψ⟩_ with non-zero overlap with the ground state _|E_ 0 _⟩_ : 

22 

**What we asked.** We asked El Agente Cuántico to read the PennyLane manual, build the second-quantized electronic Hamiltonian of water (STO-3G), map it to qubits (Jordan–Wigner), construct a logical (non-faulttolerant) QPE circuit targeting chemical accuracy, and use PennyLane’s resource-estimation tools to estimate logical qubits and non-Clifford gate counts from Hamiltonian-simulation segments. 

**What this showcases.** This example tests whether the agent can move from “simulate a system” to “estimate feasibility”: assembling a chemistry Hamiltonian, selecting a canonical algorithm (QPE), and reporting meaningful logical-level space/time costs with clear scaling interpretation. 

**Used agent/tools:** quantum scientist agent, pennylane expert agent, literature search, deepsearch, python REPL, submit python jobs and view png file, see supplementary information for detailed description. The answer was verified to be correct. 

**==> picture [321 x 114] intentionally omitted <==**

**----- Start of picture text -----**<br>
| 0 ⟩ H<br>| 0 ⟩ H<br>n qubits QFT [†]<br>... ... ...<br>| 0 ⟩ H<br>m<br>|ψ⟩ U [2][0] U [2][1] . . . U [2] [n][−] [1] |E 0 ⟩<br>**----- End of picture text -----**<br>


However, implementing QPE requires significant quantum resources, commonly measured in terms of logical qubits and non-Clifford gates (e.g., _T_ gates), which measure the space and gate complexity, respectively. Below, we show El Agente Cuántico estimating these resources for simulating the water molecule in the STO-3G basis using PennyLane (75). 

**Prompt** Read the PennyLane manual and construct the second-quantized electronic Hamiltonian of water in the STO-3G basis. Use the Jordan-Wigner transformation to map the Hamiltonian to a qubit representation. Then build a logical (non–fault-tolerant) quantum phase estimation (QPE) circuit that would estimate the ground-state energy of water within chemical accuracy, and use PennyLane’s resource-estimation tools to approximate: (1) the number of logical qubits required and (2) the number of non-Clifford (e.g., _T_ ) gates arising from the Hamiltonian-simulation segments of the QPE routine. Report and discuss these logical-level resource estimates. 

23 

## **Response** 

**(a) Left panel, qubit breakdown.** 14 system (4.8%) vs 276 ancilla (95.2%) = 290 total. 

**(b) Right panel, required Toffoli gates.** Toffoli gates vs error (log-scale), showing _O_ (1 _/ϵ_ ) scaling with chemical accuracy marked in green. 

For water QPE at chemical accuracy, you need 290 logical qubits and _∼_ 112M Toffoli gates. 

**==> picture [404 x 166] intentionally omitted <==**

**Figure 14** Plots generated by El Agente Cuántico estimating space-time resources for QPE of the water molecule. (Left) Qubit breakdown. (Right) Required Toffoli gates for various target errors. 

## **5.4 Quantum error correction** 

Physical qubits are highly susceptible to noise arising from imperfect control, measurement errors, and decoherence, which can rapidly destroy stored information. Quantum error correction (QEC) overcomes this limitation by encoding logical quantum information into correlated states of multiple physical qubits, enabling errors to be detected and corrected without directly measuring the encoded state. Since its introduction in the mid-1990s, QEC has become the central component of fault-tolerant quantum computing, establishing that arbitrarily long quantum computations are possible provided physical error rates remain below a threshold value (131; 132; 133; 134). 

Among the many QEC schemes developed to date, surface codes have emerged as one of the leading candidates for large-scale implementations due to their high threshold value. These codes arrange qubits on a twodimensional lattice and rely only on local measurements, making them well-suited to current hardware architectures. This family of codes, when using an appropriate decoder such as minimum-weight perfect matching (MWPM) (135) or Union-Find (UF) (136), enables logical error rates to be exponentially reduced by increasing the code’s distance (137; 138). Recent experimental progress has begun to demonstrate logical memories whose performance improves with system size, showing promise toward practical fault-tolerant quantum devices (139; 140; 141; 142; 143). 

**What we asked.** We asked El Agente Cuántico to implement a surface-code logical _Z_ -basis memory experiment using Stim , for distances _d_ = 3 _,_ 5 _,_ 7, rounds _R_ = _d_ , and 3 _×_ 10[6] shots per distance, with two-qubit depolarizing noise ( _p_ = 0 _._ 003) applied on every CNOT, then compute the logical observable _ZL_ from final data-qubit parities. 

**What this showcases.** This example evaluates whether the agent can execute a modern QEC workflow end-toend: selecting a decoder-ready simulation backend, running large-shot Monte Carlo experiments, computing logical observables, and connecting results to the expected distance-scaling behavior of logical error rates. 

**Used agent/tools:** quantum scientist agent, cudaq expert agent, deepsearch, python REPL, submit python jobs and view png file, see supplementary information for detailed description. The answer was verified to be correct. 

24 

**Prompt** Implement and run a surface-code logical memory experiment in the Z basis using CUDA-Q QEC with the Stim backend on CPU. Use the following parameters: 

**Distances:** d = 3, 5, 7. **Rounds:** R = d stabilizer-measurement rounds. **Shots:** N = 3000000 per distance **State:** prepare logical _|_ 0 _L⟩_ (Z-basis memory). **Noise:** apply two-qubit depolarizing noise with probability p = 0.003 on every CX (CNOT) gate only. **Sampling:** for each shot, sample Stim detector events and final data-qubit Z measurements. **Logical observable:** compute measured _ZL_ as the parity of the final data-qubit Z outcomes along the chosen logical _ZL_ string. **Decoding:** build the Stim-generated detector error model (DEM) and decode using PyMatching (MWPM). **Plots:** report a single plot of d vs logic error gate for the data with and without the decoder, and add theoretical estimation. 

**Response** The figure shows the logical error rate versus code distance for a Z-basis surface-code memory, comparing raw measurements (red), MWPM-decoded results (blue), and a threshold-model prediction (green). Without decoding, the logical error rate increases with distance because larger codes require more physical qubits, CNOT gates, and measurement rounds, leading to accumulated errors that scale approximately as _p_ raw _∼ d_[3] . In contrast, decoding produces a rapidly decreasing logical error rate with distance, consistent with correction of up to _⌊_ ( _d −_ 1) _/_ 2 _⌋_ errors and the expected scaling _pL ∼_ ( _p/p_ th)[(] _[d]_[+1)] _[/]_[2] . Quantitatively, the decoded logical error drops from 0 _._ 193% at _d_ = 3 natural-language request can become an end-to-end pipeline that spans model definition, execution, and analysis across circuit simulators, open-system solvers, tensor network methods, and resource-estimation suppression as distance increases. 

**==> picture [314 x 235] intentionally omitted <==**

**Figure 15** Plot generated by El Agente Cuántico showing the exponential suppression of logical error rates in a surface-code quantum memory as a function of code distance, both with and without decoding. 

## **6 Discussion** 

In this work, we showed how El Agente Cuántico can simulate quantum-mechanical systems using a wide range of tools while keeping the workflow close to how researchers frame questions. A single natural-language request can become an end-to-end pipeline that spans model definition, execution, and analysis across circuit simulators, open-system solvers, tensor network methods, and resource-estimation utilities. This positions the agent in a useful role between scientific intent and the practical steps required by different quantum software stacks. 

25 

A central observation emerging from these experiments is that the reliability and efficiency of autonomous execution depend strongly on the clarity and internal coherence of available software documentation. When reference materials present well-defined usage patterns, consistent terminology, and sufficiently explicit examples, the agent can translate physical objectives into appropriate computational abstractions with little iteration, allowing its reasoning effort to remain focused on scientific modeling decisions rather than on reconstructing intended interfaces. When documentation instead contains ambiguous guidance, underspecified examples, or overlapping conventions, the agent must infer correct usage through iterative interaction with the software, relying on runtime feedback to resolve uncertainty. Although this adaptive process often succeeds, it introduces additional overhead and variability in execution paths. 

These observations highlight an important systemic relationship between autonomous scientific agents and the broader software ecosystems in which they operate. Clear, well-maintained documentation and consistent interface conventions amplify the agent’s ability to reason effectively across tools and domains. In this sense, El Agente Cuántico not only benefits from mature software infrastructure but also actively exercises it, revealing how scientific knowledge, software design, and executable practice interact in an integrated workflow. As agent-based systems become more prevalent, this interaction may encourage documentation practices that are simultaneously optimized for human users and machine-mediated reasoning. 

Furthermore, the results demonstrate the capacity of our agentic framework to unify simulation methodologies that are traditionally treated as distinct. Circuit-based algorithms, open quantum system dynamics, tensor network techniques, and fault-tolerant resource estimation are all accessed through a common natural language interface, despite their differing mathematical formalisms and implementation paradigms. This unification lowers the conceptual overhead required to move between methods and enables researchers to explore complementary approaches to the same physical problem within a single coherent workflow. 

Taken together, these results suggest a shift in how quantum-simulation expertise can be expressed and deployed. Rather than requiring deep familiarity with every library, syntax, and backend, researchers can articulate goals at the level of physical models and observables. At the same time El Agente Cuántico translates those goals into executable implementations across heterogeneous simulation tools. In this role, the agent functions as an enabling layer for quantum simulation rather than a replacement for human expertise, complementing scientific intuition by reducing technical friction, integrating diverse methods, and supporting iterative exploration. This reframing has the potential to accelerate exploratory research, support rapid hypothesis testing, and make advanced simulation techniques more accessible across disciplinary boundaries. Building on this foundation, the roadmap presented in the following subsection outlines how these capabilities can be extended toward richer forms of autonomy, coordination, and scientific discovery. 

## **6.1 El Agente Cuántico roadmap** 

In Figure 16 we summarize a staged roadmap for the evolution of El Agente Cuántico from task-level automation toward fully autonomous scientific discovery. The current work establishes Stage 0 (Automated Quantum Simulation), in which natural-language prompts are translated into quantum-simulation workflows exploiting the state of the art software stacks (77; 74; 78; 79; 75; 144; 76). This capability builds directly on recent advances in reasoning models and scientific agents that map high-level scientific intent to concrete computational actions (51; 52; 49; 60; 57). 

26 

**==> picture [472 x 177] intentionally omitted <==**

**Figure 16** Future stages required to develop El Agente Cuántico from an automated quantum simulation tool toward a self-driving quantum scientist capable of closed-loop hypothesis generation, experimental execution, and result interpretation. 

Subsequent development will introduce multi-backend connectivity (Stage 1), enabling seamless execution across heterogeneous computing resources, including cloud servers, GPUs, and emerging QPU platforms, with backend selection guided by the problem structure and hardware availability. As an immediate next step toward this goal, we will release a cloud-enabled alpha version of El Agente Cuántico, providing web-based access to its core automated quantum-simulation capabilities via elagente.ca. This capability will be complemented by a multi-agent scientific architecture (Stage 2), in which specialized domain agents such as quantum chemistry, materials, and drug-discovery agents developed within the Matter Lab[1] ecosystem collaborate through agent-to-agent communication to decompose tasks, cross-validate results, and assemble end-to-end scientific workflows, in line with broader trends in multi-agent scientific AI (64; 145; 57; 66). 

At the workflow level, hybrid quantum-classical integration (Stage 3) will establish closed-loop pipelines that combine classical solvers, tensor network methods, and quantum circuits. This approach follows the dominant strategy for near-term quantum simulation and variational algorithms (21; 146; 98; 14). As execution moves closer to hardware, hardware-aware compilation and scheduling (Stage 4) will account for device-specific constraints such as qubit connectivity, native gate sets, noise properties, and HPC or QPU scheduling policies. In doing so, the agent’s reasoning layer will be directly connected to modern quantum compilation, hardware software co-design, and performance-aware execution frameworks (146; 147; 99; 120). 

As circuit depth and system size increase, AI-driven error mitigation and quantum error correction (Stage 5) will support the automated selection, implementation, and evaluation of mitigation techniques and error correcting codes. This will rely on fast stabilizer simulation, decoder optimization, and learning based control methods (144; 148; 64). At the logical level, a fault-tolerant translation layer (Stage 6) will raise agent outputs from physical circuits to logical, fault-tolerant representations. This layer will also provide resource estimates and runtime analysis, connecting high-level algorithm descriptions with fault-tolerant quantum architectures. 

Beyond execution, autonomous algorithm discovery (Stage 7) will enable the agent to generate, compile, and evaluate candidate quantum algorithms, classical simulation strategies, hardware-aware fault-tolerant schemes, and control protocols using automated simulation and benchmarking loops. Instead of relying on fixed algorithm designs, the agent will explore families of circuit constructions and iteratively refine them based on accuracy, resource requirements, and noise sensitivity. Recent work by Quantinuum and Hiverge (149) demonstrates this approach feasible in quantum chemistry, where AI-driven workflows search variational algorithm spaces starting from simple templates and improve them through simulation-guided optimization, highlighting the potential of automated discovery within near-term hardware constraints. 

Finally, the roadmap culminates in a self-driving quantum scientist (Stage 8), in which hypothesis generation, computational modeling, experimental execution, and result interpretation are integrated into a closed, autonomous feedback loop. At this stage, El Agente Cuántico will autonomously formulate and refine 

> 1These papers will be published in parallel. 

27 

scientific hypotheses, select and adapt computational and experimental strategies, and iteratively update its internal models based on newly generated data. This vision directly builds on recent advances in agentic scientific systems and self-driving laboratories, where hierarchical planning, adaptive decision-making, and continuous validation enable accelerated, reproducible, and scalable discovery across computational and experimental domains (150; 151; 152; 153; 154; 155). 

## **7 Conclusions** 

In this work, we presented El Agente Cuántico, a multi-agent AI system that translates natural-language descriptions of quantum-simulation tasks into executed and analyzed workflows across a heterogeneous quantum-software stack. A central advantage of the approach is that the agent grounds its reasoning in direct searches of library manuals and documentation, allowing it to recover current APIs, implementation details, and best practices at runtime. This design enables scalable adaptation to multiple libraries and evolving interfaces without task-specific engineering, and we demonstrated this capability across state preparation, closed- and open-system dynamics, tensor-network simulations, quantum control, quantum error correction, and quantum resource estimation. 

Furthermore, this work shows how agentic AI systems can change how quantum simulations are done in the community, placing the emphasis on physical reasoning rather than on implementation details. Through El Agente Cuántico, domain expertise is articulated directly in terms of physical models, assumptions, and observables, rather than being scattered across framework-specific code. By reducing the effort required to assemble and maintain complex workflows, agentic systems enable researchers to engage more deeply with scientific questions and their interpretation, rather than with computational overhead. 

Looking forward, the roadmap presented in this work outlines a steady evolution from automated quantumsimulation workflows toward an autonomous quantum scientist. Initial advances will focus on expanding computational reach and on improving the integration of classical and quantum devices to address larger, more realistic problems. As these capabilities mature, greater autonomy in execution, decision-making, and interpretation will enable tighter integration among simulation, experimentation, and analysis. Ultimately, this progression aims to support scalable and reproducible discovery by allowing scientific intent to be translated directly into adaptive, self-directed research workflows. In this sense, the goal is not to replace scientific judgment, but to amplify it by enabling more systematic, scalable, and reproducible exploration of complex scientific problems.(156) 

## **Data and code availability** 

All the data required to evaluate the presented conclusions are available via https://doi.org/10.5683/SP3/ UAKARI 

## **Acknowledgments** 

The authors would like to acknowledge valuable discussions with Jiaru Bai, Naixu Guo, Mohsen Bagherimehrab, Shuxiang Cao, and Ignacio Franco. We gratefully acknowledge the longstanding contributions of the Matter Lab’s current and past group members (matter.toronto.edu), and in particular from El Agente team. I.G. and J.B.P. acknowledge funding of this project by the National Sciences and Engineering Research Council of Canada (NSERC) Alliance Grant #ALLRP587593-23. L.M.C. is supported by the Novo Nordisk Foundation, Grant number NNF22SA0081175, NNF Quantum Computing Programme. K.P. and M.R. acknowledge the generous support of the Canada 150 Research Chairs Program through A.A.-G. Y.N. gratefully acknowledge support from the NSERC CREATE for Accelerated Discovery (AccelD) training program hosted by the Acceleration Consortium (Grant #596133-2025) and was partially supported through a collaborative partnership with Moderna Inc. Z.Z. and Y.Z. acknowledge support from NSERC - IRCPJ 547644. This research is part of the University of Toronto’s Acceleration Consortium, which receives funding from the CFREF-2022-00042 Canada First Research Excellence Fund. This research was enabled in part by support provided by _SciNet_ and the Digital Research Alliance of Canada (alliancecan.ca) Computations were performed on the Niagara 

28 

supercomputer at the SciNet HPC Consortium. SciNet is funded by: the Canada Foundation for Innovation; the Government of Ontario; Ontario Research Fund - Research Excellence; and the University of Toronto. A.A.-G. thanks Anders G. Frøseth, for his generous support. A.A.-G. and V.B. also acknowledge the generous support of Natural Resources Canada and the Canada 150 Research Chairs program. This research is part of the University of Toronto’s Acceleration Consortium, which receives funding from the Canada First Research Excellence Fund (CFREF) via CFREF-2022-00042. This work was supported by the AI2050 program of Schmidt Sciences. This work was supported by the Defense Advanced Research Projects Agency (DARPA) under Agreement No. HR0011262E022. 

29 

## **References** 

- [1] Ira N. Levine. _Quantum Chemistry_ . Pearson, seventh edition, 2014. ISBN 978-0-321-80345-0. 

- [2] Yudong Cao, Jonathan Romero, Jonathan P. Olson, Matthias Degroote, Peter D. Johnson, Mária Kieferová, Ian D. Kivlichan, Tim Menke, Borja Peropadre, Nicolas P.D. Sawaya, et al. Quantum chemistry in the age of quantum computing. _Chem. Rev._ , 119(19):10856–10915, 2019. doi:10.1021/acs.chemrev.8b00803. 

- [3] Michael P. Marder. _Condensed matter physics_ . John Wiley & Sons, 2010. ISBN 9780470617984. 

- [4] Philip W. Anderson. _Basic notions of condensed matter physics_ . CRC press, 2018. ISBN 0805302204. 

- [5] Paul M. Chaikin, Tom C. Lubensky, and Thomas A. Witten. _Principles of condensed matter physics_ , volume 10. Cambridge university press, 1995. ISBN 9781139643054. 

- [6] Marlan O. Scully and M. Suhail Zubairy. _Quantum optics_ . Cambridge university press, 1997. ISBN 9780511813993. 

- [7] Christopher C. Gerry and Peter L. Knight. _Introductory quantum optics_ . Cambridge university press, 2023. ISBN 9780511791239. 

- [8] Malcolm S. Longair. _High energy astrophysics_ . Cambridge university press, 2011. ISBN 9780511778346. 

- [9] Donald H. Perkins. _Introduction to high energy physics_ . Cambridge university press, 2000. ISBN 9780511809040. 

- [10] Krishan K. Chawla. _Composite materials: science and engineering_ . Springer Science & Business Media, 2012. ISBN 9780387743646. 

- [11] William D. Callister and David G. Rethwisch. _Fundamentals of materials science and engineering_ . Wiley London, 2000. ISBN 9781118319222. 

- [12] Iulia M. Georgescu, Sahel Ashhab, and Franco Nori. Quantum simulation. _Rev. Mod. Phys._ , 86(1):153–185, 2014. doi:10.1103/revmodphys.86.153. 

- [13] Matthias Troyer and Uwe-Jens Wiese. Computational complexity and fundamental limitations to fermionic quantum monte carlo simulations. _Phys. Rev. Lett._ , 94(17):170201, 2005. doi:10.1103/physrevlett.94.170201. 

- [14] Alán Aspuru-Guzik, Anthony D. Dutoi, Peter J. Love, and Martin Head-Gordon. Simulated quantum computation of molecular energies. _Science_ , 309(5741):1704–1707, 2005. doi:10.1126/science.1113479. 

- [15] Ulrich Schollwöck. The density-matrix renormalization group in the age of matrix product states. _Ann. Phys._ , 326(1):96–192, 2011. doi:10.1016/j.aop.2010.09.012. 

- [16] Jens Eisert, Marcus Cramer, and Martin B. Plenio. Colloquium: Area laws for the entanglement entropy. _Rev. Mod. Phys._ , 82(1):277–306, 2010. doi:10.1103/revmodphys.82.277. 

- [17] Román Orús. A practical introduction to tensor networks: Matrix product states and projected entangled pair states. _Ann. Phys._ , 349:117–158, 2014. doi:10.1016/j.aop.2014.06.013. 

- [18] Inés De Vega and Daniel Alonso. Dynamics of non-markovian open quantum systems. _Rev. Mod. Phys._ , 89(1): 015001, 2017. doi:10.1103/revmodphys.89.015001. 

- [19] Michael H. Beck, Andreas Jäckle, Graham A. Worth, and H-D Meyer. The multiconfiguration time-dependent hartree (mctdh) method: a highly efficient algorithm for propagating wavepackets. _Phys. Rep._ , 324(1):1–105, 2000. doi:10.1016/s0370-1573(99)00047-2. 

- [20] Xinxian Chen and Ignacio Franco. Tree tensor network hierarchical equations of motion based on time-dependent variational principle for efficient open quantum dynamics in structured thermal environments. _J. Chem. Phys._ , 163:104109, 9 2025. doi:10.1063/5.0278591. 

- [21] Alberto Peruzzo, Jarrod McClean, Peter Shadbolt, Man-Hong Yung, Xiao-Qi Zhou, Peter J. Love, Alán AspuruGuzik, and Jeremy L. O’brien. A variational eigenvalue solver on a photonic quantum processor. _Nat. Commun._ , 5(1):4213, 2014. doi:10.1038/ncomms5213. 

- [22] Jarrod R. McClean, Jonathan Romero, Ryan Babbush, and Alán Aspuru-Guzik. The theory of variational hybrid quantum-classical algorithms. _New J. Phys._ , 18(2):023023, 2016. doi:10.1088/1367-2630/18/2/023023. 

- [23] Marco Cerezo, Andrew Arrasmith, Ryan Babbush, Simon C. Benjamin, Suguru Endo, Keisuke Fujii, Jarrod R. McClean, Kosuke Mitarai, Xiao Yuan, Lukasz Cincio, et al. Variational quantum algorithms. _Nat. Rev. Phys._ , 3 (9):625–644, 2021. doi:10.1038/s42254-021-00348-9. 

30 

- [24] Luis Mantilla Calderón, Robert Raussendorf, Polina Feldmann, and Dmytro Bondarenko. Measurement-based quantum machine learning. _ArXiv preprint arXiv:2405.08319_ , 2024. doi:10.48550/arXiv.2405.08319. 

- [25] Kishor Bharti, Alba Cervera-Lierta, Thi Ha Kyaw, Tobias Haug, Sumner Alperin-Lea, Abhinav Anand, Matthias Degroote, Hermanni Heimonen, Jakob S Kottmann, Tim Menke, et al. Noisy intermediate-scale quantum algorithms. _Reviews of Modern Physics_ , 94(1):015004, 2022. 

- [26] Bettina Heim, Mathias Soeken, Sarah Marshall, Chris Granade, Martin Roetteler, Alan Geller, Matthias Troyer, and Krysta Svore. Quantum programming languages. _Nat. Rev. Phys._ , 2(12):709–722, 2020. doi:10.1038/s42254020-00245-7. 

- [27] Mark Fingerhuth, Tomáš Babej, and Peter Wittek. Open source software in quantum computing. _PLoS ONE_ , 13(12):e0208561, 2018. doi:10.1371/journal.pone.0208561. 

- [28] Ryan LaRose. Overview and comparison of gate level quantum software platforms. _Quantum_ , 3:130, 2019. doi:10.22331/q-2019-03-25-130. 

- [29] Mayk Caldas Ramos, Christopher J Collison, and Andrew D White. A review of large language models and autonomous agents in chemistry. _Chem. Sci._ , 2025. doi:10.1039/d4sc03921a. 

- [30] Likang Wu, Zhi Zheng, Zhaopeng Qiu, Hao Wang, Hongchao Gu, Tingjia Shen, Chuan Qin, Chen Zhu, Hengshu Zhu, Qi Liu, et al. A survey on large language models for recommendation. _World Wide Web_ , 27(5):60, 2024. doi:10.1007/s11280-024-01291-2. 

- [31] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot learners. In _Adv. Neural Inf. Process. Syst. (NeurIPS)_ , NIPS ’20, Red Hook, NY, USA, 2020. Curran Associates Inc. ISBN 9781713829546. 

- [32] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul F. Christiano, Jan Leike, and Ryan Lowe. Training language models to follow instructions with human feedback. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors, _Adv. Neural Inf. Process. Syst._ , volume 35, pages 27730–27744. Curran Associates, Inc., 2022. ISBN 9781713871088. 

- [33] Paul F. Christiano, Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg, and Dario Amodei. Deep reinforcement learning from human preferences. In _Adv. Neural Inf. Process. Syst._ , NIPS’17, page 4302–4310, Red Hook, NY, USA, 2017. Curran Associates Inc. ISBN 9781510860964. 

- [34] Mark Chen. Evaluating large language models trained on code. _arXiv preprint arXiv:2107.03374_ , 2021. doi:10.48550/arXiv.2107.03374. 

- [35] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and Yuan Cao. React: Synergizing reasoning and acting in language models. In _Int. Conf. Learn. Represent. (ICLR)_ , 2023. URL https://openreview.net/forum?id=WE_vluYUL-X. 

- [36] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, and Peter Clark. Self-refine: Iterative refinement with self-feedback. In _Adv. Neural Inf. Process. Syst. (NeurIPS)_ , 2023. URL https://openreview.net/forum?id=S37hOerQLB. 

- [37] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, brian ichter, Fei Xia, Ed Chi, Quoc V Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors, _Adv. Neural Inf. Process. Syst._ , volume 35, pages 24824– 24837. Curran Associates, Inc., 2022. URL https://proceedings.neurips.cc/paper_files/paper/2022/file/9d56 09613524ecf4f15af0f7b31abca4-Paper-Conference.pdf. 

- [38] OpenAI. Openai o1 system card. _arXiv preprint arXiv:2412.16720_ , 2024. doi:10.48550/arXiv.2412.16720. 

- [39] DeepSeek-AI. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_ , 2025. doi:10.48550/arXiv.2501.12948. URL https://arxiv.org/abs/2501.12948. 

31 

- [40] Google Gemini Team. Gemini 2.5: Pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities. _arXiv preprint arXiv:2507.06261_ , 2025. doi:10.48550/arXiv.2507.06261. URL https://arxiv.org/abs/2507.06261. 

- [41] Nvidia, :, Bo Adler, Niket Agarwal, Ashwath Aithal, Dong H. Anh, Pallab Bhattacharya, Annika Brundyn, Jared Casper, Bryan Catanzaro, Sharon Clay, Jonathan Cohen, Sirshak Das, Ayush Dattagupta, Olivier Delalleau, Leon Derczynski, Yi Dong, Daniel Egert, Ellie Evans, Aleksander Ficek, Denys Fridman, Shaona Ghosh, Boris Ginsburg, Igor Gitman, Tomasz Grzegorzek, Robert Hero, Jining Huang, Vibhu Jawa, Joseph Jennings, Aastha Jhunjhunwala, John Kamalu, Sadaf Khan, Oleksii Kuchaiev, Patrick LeGresley, Hui Li, Jiwei Liu, Zihan Liu, Eileen Long, Ameya Sunil Mahabaleshwarkar, Somshubra Majumdar, James Maki, Miguel Martinez, Maer Rodrigues de Melo, Ivan Moshkov, Deepak Narayanan, Sean Narenthiran, Jesus Navarro, Phong Nguyen, Osvald Nitski, Vahid Noroozi, Guruprasad Nutheti, Christopher Parisien, Jupinder Parmar, Mostofa Patwary, Krzysztof Pawelec, Wei Ping, Shrimai Prabhumoye, Rajarshi Roy, Trisha Saar, Vasanth Rao Naik Sabavat, Sanjeev Satheesh, Jane Polak Scowcroft, Jason Sewall, Pavel Shamis, Gerald Shen, Mohammad Shoeybi, Dave Sizer, Misha Smelyanskiy, Felipe Soares, Makesh Narsimhan Sreedhar, Dan Su, Sandeep Subramanian, Shengyang Sun, Shubham Toshniwal, Hao Wang, Zhilin Wang, Jiaxuan You, Jiaqi Zeng, Jimmy Zhang, Jing Zhang, Vivienne Zhang, Yian Zhang, and Chen Zhu. Nemotron-4 340b technical report. _arXiv preprint arXiv:2406.11704_ , 2024. doi:10.48550/arXiv.2406.11704. URL https://arxiv.org/abs/2406.11704. 

- [42] OpenAI. Gpt-5.2 system card. System card, OpenAI, 2025. URL https://cdn.openai.com/pdf/3a4153c8-c74 8-4b71-8e31-aecbde944f8d/oai_5_2_system-card.pdf. 

- [43] Google DeepMind. Gemini 3 pro model card. https://storage.googleapis.com/deepmind-media/Model-Cards /Gemini-3-Pro-Model-Card.pdf, 2024. 

- [44] Anthropic. Claude opus 4.5 system card. System card, Anthropic, 2025. URL https://assets.anthropic.com/m /64823ba7485345a7/Claude-Opus-4-5-System-Card.pdf. 

- [45] Jiaqi Wei, Yuejin Yang, Xiang Zhang, Yuhan Chen, Xiang Zhuang, Zhangyang Gao, Dongzhan Zhou, Guangshuai Wang, Zhiqiang Gao, Juntai Cao, et al. From ai for science to agentic science: A survey on autonomous scientific discovery. _arXiv preprint arXiv:2508.14111_ , 2025. doi:10.48550/arXiv.2508.14111. 

- [46] Kexin Huang, Serena Zhang, Hanchen Wang, Yuanhao Qu, Yingzhou Lu, Yusuf Roohani, Ryan Li, Lin Qiu, Gavin Li, Junze Zhang, et al. Biomni: A general-purpose biomedical ai agent. _bioRxiv_ , 2025. doi:10.1101/2025.05.30.656746. 

- [47] NovelSeek Team, Bo Zhang, Shiyang Feng, Xiangchao Yan, Jiakang Yuan, Zhiyin Yu, Xiaohan He, Songtao Huang, Shaowei Hou, Zheng Nie, et al. Novelseek: When agent becomes the scientist–building closed-loop system from hypothesis to verification. _arXiv preprint arXiv:2505.16938_ , 2025. doi:10.48550/arXiv.2505.16938. 

- [48] Jakub Lála, Odhran O’Donoghue, Aleksandar Shtedritski, Sam Cox, Samuel G. Rodriques, and Andrew D. White. Paperqa: Retrieval-augmented generative agent for scientific research. _arXiv preprint arXiv:2312.07559_ , 2023. doi:10.48550/arXiv.2312.07559. 

- [49] Ludovico Mitchener, Angela Yiu, Benjamin Chang, Mathieu Bourdenx, Tyler Nadolski, Arvis Sulovari, Eric C Landsness, Daniel L Barabasi, Siddharth Narayanan, Nicky Evans, et al. Kosmos: An ai scientist for autonomous discovery. _arXiv preprint arXiv:2511.02824_ , 2025. doi:10.48550/arXiv.2511.02824. 

- [50] Kyle Swanson, Wesley Wu, Nash L. Bulaong, John E. Pak, and James Z. Zou. The virtual lab of ai agents designs new sars-cov-2 nanobodies. _Nature_ , 2025. doi:10.1038/s41586-025-09442-9. 

- [51] Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, and David Ha. The ai scientist: Towards fully automated open-ended scientific discovery. _arXiv preprint arXiv:2408.06292_ , 2024. doi:10.48550/arXiv.2408.06292. 

- [52] Yutaro Yamada, Robert Tjarko Lange, Cong Lu, Shengran Hu, Chris Lu, Jakob Foerster, Jeff Clune, and David Ha. The ai scientist-v2: Workshop-level automated scientific discovery via agentic tree search. _arXiv preprint arXiv:2504.08066_ , 2025. doi:10.48550/arXiv.2504.08066. 

- [53] Kourosh Darvish, Marta Skreta, Yuchi Zhao, Naruki Yoshikawa, Sagnik Som, Miroslav Bogdanovic, and . . . . Organa: A robotic assistant for automated chemistry experimentation and characterization. _arXiv preprint arXiv:2401.06949_ , 2024. doi:10.48550/arXiv.2401.06949. 

- [54] Andres M Bran, Sam Cox, Oliver Schilter, Carlo Baldassari, Andrew D White, and Philippe Schwaller. Chemcrow: Augmenting large-language models with chemistry tools. _arXiv preprint arXiv:2304.05376_ , 2023. doi:10.48550/arXiv.2304.05376. 

32 

- [55] Daniil A Boiko, Robert MacKnight, Ben Kline, and Gabe Gomes. Autonomous chemical research with large language models. _Nature_ , 624(7992):570–578, 2023. doi:10.1038/s41586-023-06792-0. 

- [56] Xiangru Tang, Tianyu Hu, Muyang Ye, Yanjun Shao, Xunjian Yin, Siru Ouyang, Wangchunshu Zhou, Pan Lu, Zhuosheng Zhang, Yilun Zhao, et al. Chemagent: Self-updating library in large language models improves chemical reasoning. _arXiv preprint arXiv:2501.06590_ , 2025. doi:10.48550/arXiv.2501.06590. 

- [57] Yunheng Zou, Austin H. Cheng, Abdulrahman Aldossary, Jiaru Bai, Shi Xuan Leong, Jorge Arturo CamposGonzalez-Angulo, Changhyeok Choi, Cher Tian Ser, Gary Tom, Andrew Wang, Zijian Zhang, Ilya Yakavets, Han Hao, Chris Crebolder, Varinia Bernales, and Alán Aspuru-Guzik. El agente: An autonomous agent for quantum chemistry. _Matter_ , 8(7):102263, 2025. ISSN 2590-2385. doi:https://doi.org/10.1016/j.matt.2025.102263. 

- [58] Maximilian Nägele and Florian Marquardt. Agentic exploration of physics models. _arXiv preprint arXiv:2509.24978_ , 2025. 

- [59] Benjamin Breen, Marco Del Tredici, Jacob McCarran, Javier Aspuru Mijares, Weichen Winston Yin, Kfir Sulimany, Jacob M Taylor, Frank HL Koppens, and Dirk Englund. Ax-prover: A deep reasoning agentic framework for theorem proving in mathematics and quantum physics. _arXiv preprint arXiv:2510.12787_ , 2025. doi:10.48550/arXiv.2510.12787. 

- [60] Cunshi Wang, Yu Zhang, Yuyang Li, Xinjie Hu, Yiming Mao, Xunhao Chen, Pengliang Du, Rui Wang, Ying Wu, Hang Yang, et al. Starwhisper telescope: an ai framework for automating end-to-end astronomical observations. _Commun. Eng._ , 4(1):184, 2025. doi:10.1038/s44172-025-00520-4. 

- [61] Vladimir Naumov, Diana Zagirova, Sha Lin, Yupeng Xie, Wenhao Gou, Anatoly Urban, Nina Tikhonova, Khadija Alawi, Mike Durymanov, Fedor Galkin, et al. Dora ai scientist: Multi-agent virtual research team for scientific exploration discovery and automated report generation. _bioRxiv_ , 2025. doi:10.1101/2025.03.06.641840. 

- [62] Yuri Alexeev, Marwa H. Farag, Taylor L. Patti, Mark E. Wolf, Natalia Ares, Alán Aspuru-Guzik, Simon C. Benjamin, Zhenyu Cai, Shuxiang Cao, Christopher Chamberland, et al. Artificial intelligence for quantum computing. _Nat. Commun._ , 16(1):10829, 2025. 

- [63] Sören Arlt, Xuemei Gu, and Mario Krenn. Towards autonomous quantum physics research using llm agents with access to intelligent tools. _arXiv preprint arXiv:2511.11752_ , 2025. 

- [64] Shuxiang Cao, Zijian Zhang, Mohammed Alghadeer, Simone D Fasciati, Michele Piscitelli, Mustafa Bakr, Peter Leek, and Alán Aspuru-Guzik. Automating quantum computing laboratory experiments with an agent-based ai framework. _Patterns_ , 6(10), 2025. doi:10.1016/j.patter.2025.101372. 

- [65] Carlos Flores-Garrigos, Gaurav Dev, Michael Falkenthal, Alejandro Gomez Cadavid, Anton Simen, Shubham Kumar, Enrique Solano, and Narendra N Hegade. Quantum combinatorial reasoning for large language models. _arXiv preprint arXiv:2510.24509_ , 2025. doi:10.48550/arXiv.2510.24509. 

- [66] Ankita Sharma, Vahid Ansari, Yuqi Fu, Rishabh Iyer, Joaquin Matres, Troy Tamas, Onur Akdeniz, Dirk R Englund, and Joyce KS Poon. Towards ai agents for photonic integrated circuit design automation. In _CLEO: Science and Innovations_ , page SS186_1. Optica Publishing Group, 2025. doi:10.1364/cleo_si.2025.ss186_1. 

- [67] Valeria Saggio, Beate E. Asenbeck, Arne Hamann, Teodor Strömberg, Peter Schiansky, Vedran Dunjko, Nicolai Friis, Nicholas C. Harris, Michael Hochberg, Dirk Englund, et al. Experimental quantum speed-up in reinforcement learning agents. _Nature_ , 591(7849):229–233, 2021. 

- [68] Thomas J Elliott, Mile Gu, Andrew JP Garner, and Jayne Thompson. Quantum adaptive agents with efficient long-term memories. _Phys. Rev. X_ , 12(1):011007, 2022. 

- [69] Jayne Thompson, Paul M. Riechers, Andrew J. P. Garner, Thomas J. Elliott, and Mile Gu. Energetic advantages for quantum agents in online execution of complex strategies. _Phys. Rev. Lett._ , 135(16):160402, 2025. 

- [70] Won Joon Yun, Yunseok Kwak, Jae Pyoung Kim, Hyunhee Cho, Soyi Jung, Jihong Park, and Joongheon Kim. Quantum multi-agent reinforcement learning via variational quantum circuit design. In _Proc. IEEE 42nd Int. Conf. Distrib. Comput. Syst. (ICDCS)_ , pages 1332–1335. IEEE, 2022. 

- [71] Eldar Sultanow, Madjid Tehrani, Siddhant Dutta, William J Buchanan, and Muhammad Shahbaz Khan. Quantum agents. _arXiv preprint arXiv:2506.01536_ , 2025. 

- [72] Axiomatic AI. Lemma closed beta release. URL https://axiomatic-ai.com/products/lemma/. Accessed: 2025-12-15. 

33 

- [73] Kipu Quantum. Roadmap toward qc and qc+ai products (linkedin post). LinkedIn, 2025. URL https: //www.linkedin.com/posts/kipu-quantum_kipu-quantum-announces-the-dawn-of-industrial-activity-74019 69816447819776-IE6w?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACo AAD89xJkBnOvIyxxqAC0rLGy8nmks-NVSUGU. 

- [74] The CUDA-Q Development Team. Cuda-q, 2025. URL https://doi.org/10.5281/zenodo.15407754. 

- [75] Ville Bergholm, Josh Izaac, Maria Schuld, Christian Gogolin, Shahnawaz Ahmed, Vishnu Ajith, M Sohaib Alam, Guillermo Alonso-Linaje, B AkashNarayanan, Ali Asadi, et al. Pennylane: Automatic differentiation of hybrid quantum-classical computations. _arXiv preprint arXiv:1811.04968_ , 2018. doi:10.48550/arXiv.1811.04968. 

- [76] Ali Javadi-Abhari, Matthew Treinish, Kevin Krsulich, Christopher J Wood, Jake Lishman, Julien Gacon, Simon Martiel, Paul D Nation, Lev S Bishop, Andrew W Cross, et al. Quantum computing with qiskit. _arXiv preprint arXiv:2405.08810_ , 2024. doi:10.48550/arXiv.2405.08810. 

- [77] Neill Lambert, Eric Giguère, Paul Menczel, Boxi Li, Patrick Hopf, Gerardo Suárez, Marc Gali, Jake Lishman, Rushiraj Gadhvi, Rochisha Agarwal, et al. Qutip 5: The quantum toolbox in python. _Phys. Rep._ , 1153:1–62, 2026. doi:10.1016/j.physrep.2025.10.001. 

- [78] Johannes Hauschild, Jakob Unfried, Sajant Anand, Bartholomew Andrews, Marcus Bintz, Umberto Borla, Stefan Divic, Markus Drescher, Jan Geiger, Martin Hefel, Kévin Hémery, Wilhelm Kadow, Jack Kemp, Nico Kirchner, Vincent S. Liu, Gunnar Möller, Daniel Parker, Michael Rader, Anton Romen, Samuel Scalet, Leon Schoonderwoerd, Maximilian Schulz, Tomohiro Soejima, Philipp Thoma, Yantao Wu, Philip Zechmann, Ludwig Zweng, Roger S. K. Mong, Michael P. Zaletel, and Frank Pollmann. Tensor network Python (TeNPy) version 1. _SciPost Phys. Codebases_ , page 41, 2024. doi:10.21468/SciPostPhysCodeb.41. URL https://scipost.org/10.21468 /SciPostPhysCodeb.41. 

- [79] Jakob S. Kottmann, Sumner Alperin-Lea, Teresa Tamayo-Mendoza, Alba Cervera-Lierta, Cyrille Lavigne, Yen Tzu-Ching, Vladislav Verteletsky, Philipp Schleich, Matthias Degroote, Skylar Chaney, Maha Kesibo, Naomi G. Curnow, Brandon Solo, Georgios Tsilimigkounakis, Claudia Zendejas-Morales, Artur Izmaylov, Alan AspuruGuzik, Francesco Scala, and Gaurav Saxena. Tequila: A platform for rapid development of quantum algorithms, November 2020. URL https://github.com/tequilahub/tequila. 

- [80] Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Voyager: An open-ended embodied agent with large language models. _arXiv preprint arXiv:2305.16291_ , 2023. doi:10.48550/arXiv.2305.16291. 

- [81] Significant Gravitas et al. Auto-GPT: An Autonomous GPT-4 Experiment. https://github.com/Significant-G ravitas/Auto-GPT, Apr 2023. Accessed: 2025-12-16. 

- [82] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. React: Synergizing reasoning and acting in language models, 2023. URL https://arxiv.org/abs/2210.03629. 

- [83] Pascual Jordan and Eugene Wigner. Über das paulische äquivalenzverbot. _Zeitschrift für Physik_ , 47(9):631–651, 1928. doi:10.1007/BF01331938. 

- [84] Rolando Somma, Gerardo Ortiz, James E. Gubernatis, Emanuel Knill, and Raymond Laflamme. Simulating physical phenomena by quantum networks. _Phys. Rev. A_ , 65(4):042323, 2002. 

- [85] Jacob T Seeley, Martin J Richard, and Peter J Love. The bravyi-kitaev transformation for quantum computation of electronic structure. _J. Chem. Phys._ , 137(22), 2012. doi:10.1063/1.4768229. 

- [86] Rodney J Bartlett and Monika Musiał. Coupled-cluster theory in quantum chemistry. _Rev. Mod. Phys._ , 79(1): 291–352, 2007. doi:10.1103/revmodphys.79.291. 

- [87] Jonathan Romero, Ryan Babbush, Jarrod R McClean, Cornelius Hempel, Peter J Love, and Alán Aspuru-Guzik. Strategies for quantum computing molecular energies using the unitary coupled cluster ansatz. _Quantum Sci. Technol._ , 4(1):014008, 2018. doi:10.1088/2058-9565/aad3e4. 

- [88] Abhinav Anand, Philipp Schleich, Sumner Alperin-Lea, Phillip W.K. Jensen, Sukin Sim, Manuel Díaz-Tinoco, Jakob S. Kottmann, Matthias Degroote, Artur F. Izmaylov, and Alán Aspuru-Guzik. A quantum computing view on unitary coupled cluster theory. _Chem. Soc. Revi._ , 51(5):1659–1684, 2022. 

- [89] Michael A. Nielsen and Isaac L. Chuang. _Quantum Computation and Quantum Information_ . Cambridge University Press, 10th anniversary edition edition, 2010. doi:10.1017/cbo9780511976667. 

34 

- [90] John S. Bell. On the einstein podolsky rosen paradox. _Physics_ , 1(3):195–200, 1964. doi:10.1142/9789812386540_0002. 

- [91] Charles H. Bennett, Gilles Brassard, Claude Crépeau, Richard Jozsa, Asher Peres, and William K. Wootters. Teleporting an unknown quantum state via dual classical and Einstein–Podolsky–Rosen channels. _Phys. Rev. Lett._ , 70(13):1895–1899, 1993. doi:10.1103/physrevlett.70.1895. 

- [92] Charles H. Bennett and Stephen J. Wiesner. Communication via one- and two-particle operators on Einstein– Podolsky–Rosen states. _Phys. Rev. Lett._ , 69(20):2881–2884, 1992. doi:10.1103/physrevlett.69.2881. 

- [93] Ryszard Horodecki, Paweł Horodecki, Michał Horodecki, and Karol Horodecki. Quantum entanglement. _Rev. Mod. Phys._ , 81(2):865–942, 2009. doi:10.1103/revmodphys.81.865. 

- [94] Fabian HL Essler, Holger Frahm, Frank Göhmann, Andreas Klümper, and Vladimir E Korepin. _The onedimensional Hubbard model_ . Cambridge University Press, 2005. doi:10.1017/cbo9780511534843. 

- [95] Adrian E Feiguin and Steven R White. Finite-temperature density matrix renormalization using an enlarged hilbert space. _Phys. Rev. B_ , 72(22):220401, 2005. doi:10.1103/physrevb.72.220401. 

- [96] Frank Verstraete, Juan J Garcia-Ripoll, and Juan Ignacio Cirac. Matrix product density operators: Simulation of finite-temperature and dissipative systems. _Phys. Rev. Lett._ , 93(20):207204, 2004. doi:10.1103/physrevlett.93.207204. 

- [97] Masuo Suzuki. Fractal decomposition of exponential operators with applications to many-body theories and monte carlo simulations. _Phys. Lett. A_ , 146(6):319–323, 1990. doi:10.1016/0375-9601(90)90962-n. 

- [98] Andrew M Childs, Yuan Su, Minh C Tran, Nathan Wiebe, and Shuchen Zhu. Theory of trotter error with commutator scaling. _Phys. Rev. X_ , 11(1):011020, 2021. doi:10.1103/physrevx.11.011020. 

- [99] Mohsen Bagherimehrab, Luis Mantilla Calderon, Dominic W Berry, Philipp Schleich, Mohammad Ghazi Vakili, Abdulrahman Aldossary, Jorge A Angulo, Christoph Gorgulla, and Alan Aspuru-Guzik. Faster algorithmic quantum and classical simulations by corrected product formulas. _arXiv preprint arXiv:2409.08265_ , 2024. doi:10.48550/arXiv.2409.08265. 

- [100] Ignacio Gustin, Chang Woo Kim, David W McCamant, and Ignacio Franco. Mapping electronic decoherence pathways in molecules. _Proc. Natl. Acad. Sci._ , 120(49):e2309987120, 2023. doi:10.26434/chemrxiv-2023-ld0d4. 

- [101] Erich Joos, H Dieter Zeh, Claus Kiefer, Domenico JW Giulini, Joachim Kupsch, and Ion-Olimpiu Stamatescu. _Decoherence and the appearance of a classical world in quantum theory_ . Springer Science & Business Media, 2013. doi:10.1007/978-3-662-03263-3. 

- [102] Ignacio Gustin, Xinxian Chen, and Ignacio Franco. Decoherence dynamics in molecular qubits: Exponential, gaussian and beyond. _J. Chem. Phys._ , 162(6), 2025. doi:10.1063/5.0246970. 

- [103] Maximilian A Schlosshauer. _Decoherence: and the quantum-to-classical transition_ . Springer Science & Business Media, 2007. ISBN 978-3-540-35773-5. 

- [104] Wenxiang Hu, Ignacio Gustin, Todd D Krauss, and Ignacio Franco. Tuning and enhancing quantum coherence time scales in molecules via light-matter hybridization. _J. Phys. Chem. Lett._ , 13(49):11503–11511, 2022. doi:10.1021/acs.jpclett.2c02877. 

- [105] Ignacio Gustin, Chang Woo Kim, and Ignacio Franco. Dissipation pathways in a photosynthetic complex. _J. Phys. Chem. Lett._ , 16:13093–13101, 2025. doi:10.1021/acs.jpclett.5c02945. 

- [106] Ulrich Weiss. _Quantum dissipative systems_ . World Scientific, 2012. doi:10.1142/1476. 

- [107] Ignacio Gustin, Chang Woo Kim, and Ignacio Franco. General framework for quantifying dissipation pathways in open quantum systems. iii. off-diagonal system-bath couplings. _arXiv preprint arXiv:2510.04372_ , 2025. doi:10.48550/arXiv.2510.04372. 

- [108] James D Whitfield, César A Rodríguez-Rosario, and Alán Aspuru-Guzik. Quantum stochastic walks: A generalization of classical random walks and quantum walks. _Phys. Rev. A_ , 81(2):022323, 2010. 

- [109] Patrick Rebentrost, Masoud Mohseni, Ivan Kassal, Seth Lloyd, and Alán Aspuru-Guzik. Environment-assisted quantum transport. _New Journal of Physics_ , 11(3):033003, 2009. 

- [110] V. Gorini, A. Kossakowski, and E. C. G. Sudarshan. Completely positive dynamical semigroups of _n_ -level systems. _J. Math. Phys._ , 17:821, 1976. doi:10.1063/1.522979. 

35 

- [111] G. Lindblad. On the generators of quantum dynamical semigroups. _Commun. Math. Phys._ , 48:119, 1976. doi:10.1007/bf01608499. 

- [112] H. P. Breuer and F. Petruccione. _The Theory of Open Quantum Systems_ . Oxford University Press, 2002. doi:10.1093/acprof:oso/9780199213900.001.0001. 

- [113] Yoshitaka Tanimura. Numerically “exact” approach to open quantum dynamics: The hierarchical equations of motion (heom). _J. Chem. Phys._ , 153(2):020901, 2020. doi:10.1063/5.0011599. 

- [114] Tatsushi Ikeda and Gregory D. Scholes. Generalization of the hierarchical equations of motion theory for efficient calculations with arbitrary correlation functions. _J. Chem. Phys._ , 152(20):204101, 2020. doi:10.1063/5.0007327. 

- [115] Julia Adolphs and Thomas Renger. How proteins trigger excitation energy transfer in the fmo complex of green sulfur bacteria. _Biophys. J._ , 91(8):2778–2797, 2006. 

- [116] Christoph Kreisbeck, Tobias Kramer, Mirta Rodriguez, and Birgit Hein. High-performance solution of hierarchical equations of motion for studying energy transfer in light-harvesting complexes. _J. Chem. Theory Comput._ , 7(7): 2166–2174, 2011. 

- [117] Christoph Kreisbeck, Tobias Kramer, and Alán Aspuru-Guzik. Scalable high-performance algorithm for the simulation of exciton dynamics. application to the light-harvesting complex ii in the presence of resonant vibrational modes. _J. Chem. Theory Comput._ , 10(9):4045–4054, 2014. 

- [118] Navin Khaneja, Tilman Reiss, Conny Kehlet, Thomas Schulte-Herbrüggen, and Steffen J. Glaser. Optimal control of coupled spin dynamics in NMR. _J. Magn. Reson._ , 172(2):296–305, 2005. doi:10.1016/j.jmr.2004.11.004. 

- [119] Nikolay V. Vitanov, Andon A. Rangelov, Bruce W. Shore, and Klaus Bergmann. Stimulated raman adiabatic passage in physics chemistry and beyond. _Rev. Mod. Phys._ , 89(1):015006, 2017. doi:10.1103/revmodphys.89.015006. 

- [120] Nathan Wiebe, Dominic W Berry, Peter Høyer, and Barry C Sanders. Simulating quantum dynamics on a quantum computer. _J. Phys. A Math. Theor._ , 44(44):445308, 2011. doi:10.1088/1751-8113/44/44/445308. 

- [121] Tomaž Prosen. General relation between quantum ergodicity and fidelity of quantum dynamics. _Phys. Rev. E._ , 65(3):036208, 2002. doi:10.1103/physreve.65.036208. 

- [122] Dominic V Else, Christopher Monroe, Chetan Nayak, and Norman Y Yao. Discrete time crystals. _Annu. Rev. Condens. Matter Phys._ , 11(1):467–499, 2020. doi:10.1146/annurev-conmatphys-031119-050658. 

- [123] Frank Wilczek. Quantum time crystals. _Phys. Rev. Lett._ , 109(16):160401, 2012. 

- [124] Dominic V Else, Bela Bauer, and Chetan Nayak. Prethermal phases of matter protected by time-translation symmetry. _Phys. Rev. X_ , 7(1):011026, 2017. doi:10.1103/physrevx.7.011026. 

- [125] Guifré Vidal. Efficient classical simulation of slightly entangled quantum computations. _Phys. Rev. Lett._ , 91(14): 147902, 2003. doi:10.1103/physrevlett.91.147902. 

- [126] Tian-Sheng Zeng and DN Sheng. Prethermal time crystals in a one-dimensional periodically driven floquet system. _Phys. Rev. B_ , 96(9):094202, 2017. doi:10.1103/physrevb.96.094202. 

- [127] Andrew C Doherty and Stephen D Bartlett. Identifying phases of quantum many-body systems that are universal<? format?> for quantum computation. _Phys. Rev. Lett._ , 103(2):020506, 2009. doi:10.1103/physrevlett.103.020506. 

- [128] Akimasa Miyake. Quantum computation on the edge of a symmetry-protected topological order. _Phys. Rev. Lett._ , 105(4):040501, 2010. doi:10.1103/physrevlett.105.040501. 

- [129] Robert Raussendorf, Wang Yang, and Arnab Adhikary. Measurement-based quantum computation in finite one-dimensional systems: string order implies computational power. _Quantum_ , 7:1215, 2023. doi:10.22331/q2023-12-28-1215. 

- [130] A Yu Kitaev. Quantum measurements and the abelian stabilizer problem. _arXiv preprint quant-ph/9511026_ , 1995. doi:10.48550/arXiv.quant-ph/9511026. 

- [131] Peter W Shor. Scheme for reducing decoherence in quantum computer memory. _Phys. Rev. A_ , 52(4):R2493, 1995. doi:10.1103/physreva.52.r2493. 

- [132] Andrew M Steane. Error correcting codes in quantum theory. _Phys. Rev. Lett._ , 77(5):793, 1996. doi:10.1103/physrevlett.77.793. 

36 

- [133] Emanuel Knill, Raymond Laflamme, and Wojciech H Zurek. Resilient quantum computation. _Science_ , 279(5349): 342–345, 1998. doi:10.1126/science.279.5349.342. 

- [134] Simon J Devitt, William J Munro, and Kae Nemoto. Quantum error correction for beginners. _Rep. Prog. Phys._ , 76(7):076001, 2013. doi:10.1088/0034-4885/76/7/076001. 

- [135] Oscar Higgott and Craig Gidney. Sparse Blossom: correcting a million errors per core second with minimum-weight matching. _Quantum_ , 9:1600, January 2025. ISSN 2521-327X. doi:10.22331/q-2025-01-20-1600. 

- [136] Nicolas Delfosse and Naomi H Nickerson. Almost-linear time decoding algorithm for topological codes. _Quantum_ , 5:595, 2021. doi:10.22331/q-2021-12-02-595. 

- [137] A Yu Kitaev. Fault-tolerant quantum computation by anyons. _Ann. Phys._ , 303(1):2–30, 2003. doi:10.1016/s00034916(02)00018-0. 

- [138] Austin G Fowler, Matteo Mariantoni, John M Martinis, and Andrew N Cleland. Surface codes: Towards practical large-scale quantum computation. _Phys. Rev. A_ , 86(3):032324, 2012. doi:10.1103/physreva.86.032324. 

- [139] Google Quantum AI. Suppressing quantum errors by scaling a surface code logical qubit. _Nature_ , 614(7949): 676–681, 2023. doi:10.1038/s41586-022-05434-1. 

- [140] Dolev Bluvstein, Simon J Evered, Alexandra A Geim, Sophie H Li, Hengyun Zhou, Tom Manovitz, Sepehr Ebadi, Madelyn Cain, Marcin Kalinowski, Dominik Hangleiter, et al. Logical quantum processor based on reconfigurable atom arrays. _Nature_ , 626(7997):58–65, 2024. doi:10.1038/s41586-023-06927-3. 

- [141] Quantum error correction below the surface code threshold. _Nature_ , 638(8052):920–926, 2025. doi:10.1038/s41586024-08449-y. 

- [142] H Aghaee Rad, T Ainsworth, RN Alexander, B Altieri, MF Askarani, R Baby, L Banchi, BQ Baragiola, JE Bourassa, RS Chadwick, et al. Scaling and networking a modular photonic quantum computer. _Nature_ , 638 (8052):912–919, 2025. doi:10.1038/s41586-024-08406-9. 

- [143] Youwei Zhao, Yangsen Ye, He-Liang Huang, Yiming Zhang, Dachao Wu, Huijie Guan, Qingling Zhu, Zuolin Wei, Tan He, Sirui Cao, et al. Realization of an error-correcting surface code with superconducting qubits. _Phys. Rev. Lett._ , 129(3):030501, 2022. doi:10.1103/physrevlett.129.030501. 

- [144] Craig Gidney. Stim: a fast stabilizer circuit simulator. _Quantum_ , 5:497, 2021. doi:10.22331/q-2021-07-06-497. 

- [145] J. Arlt et al. Ai-mandel: Autonomous idea generation and experimental design in quantum physics. _arXiv preprint arXiv:2511.11752_ , 2025. doi:10.48550/arXiv.2511.11752. 

- [146] Prakash Murali et al. Noise-adaptive compiler mappings for noisy intermediate-scale quantum computers. In _ASPLOS_ , 2019. doi:10.1145/3297858.3304075. 

- [147] Simon Sivarajah et al. t|ket〉: A retargetable compiler for nisq devices. _Quantum Sci. Technol._ , 6:014003, 2020. doi:10.1088/2058-9565/ab8e92. 

- [148] Harun Bayraktar, Ali Charara, David Clark, Saul Cohen, Timothy Costa, Yao-Lung L Fang, Yang Gao, Jack Guan, John Gunnels, Azzam Haidar, et al. cuquantum sdk: A high-performance library for accelerating quantum science. In _Proc. IEEE Int. Conf. Quantum Comput. Eng. (QCE)_ , volume 1, pages 1050–1061. IEEE, 2023. doi:10.1109/qce57702.2023.00119. 

- [149] Eric Brunner, Steve Clark, Fabian Finger, Gabriel Greene-Diniz, Pranav Kalidindi, Alexander Koziell-Pipe, David Zsolt Manrique, Konstantinos Meichanetzidis, Frederic Rapp, Alhussein Fawzi, Hamza Fawzi, Kerry He, Bernardino Romera-Paredes, and Kante Yin. Automated quantum algorithm discovery for quantum chemistry. https://www.quantinuum.com/blog/automated-quantum-algorithm-discovery-for-quantum-chemistry. Accessed: 2025-12-15. 

- [150] Gary Tom, Stefan P Schmid, Sterling G Baird, Yang Cao, Kourosh Darvish, Han Hao, Stanley Lo, Sergio Pablo-García, Ella M Rajaonson, Marta Skreta, et al. Self-driving laboratories for chemistry and materials science. _Chem. Rev._ , 124(16):9633–9732, 2024. doi:10.1021/acs.chemrev.4c00055. 

- [151] Jiaru Bai, Liwei Cao, Sebastian Mosbach, Jethro Akroyd, Alexei A Lapkin, and Markus Kraft. From platform to knowledge graph: evolution of laboratory automation. _JACS Au_ , 2(2):292–309, 2022. doi:10.1021/jacsau.1c00438. 

- [152] Monika Vogler, Simon Krarup Steensen, Francisco Fernando Ramírez, Leon Merker, Jonas Busk, Johan Martin Carlsson, Laura Hannemose Rieger, Bojing Zhang, François Liot, Giovanni Pizzi, et al. Autonomous battery 

37 

optimization by deploying distributed experiments and simulations. _Advanced Energy Materials_ , 14(46):2403263, 2024. doi:10.1002/aenm.202403263. 

- [153] Jiaru Bai, Sebastian Mosbach, Connor J Taylor, Dogancan Karan, Kok Foong Lee, Simon D Rihm, Jethro Akroyd, Alexei A Lapkin, and Markus Kraft. A dynamic knowledge graph approach to distributed self-driving laboratories. _Nat. Commun._ , 15(1):462, 2024. doi:10.1038/s41467-023-44599-9. 

- [154] Robert Rauschen, Mason Guy, Jason E Hein, and Leroy Cronin. Universal chemical programming language for robotic synthesis repeatability. _Nature Synthesis_ , 3(4):488–496, 2024. doi:10.1038/s44160-023-00473-6. 

- [155] Dario Caramelli, Daniel Salley, Alon Henson, Gerardo Aragon Camarasa, Salah Sharabi, Graham Keenan, and Leroy Cronin. Networking chemical robots for reaction multitasking. _Nat. Commun._ , 9(1):3406, 2018. doi:10.1038/s41467-018-05828-8. 

- [156] Mario Krenn, Robert Pollice, Si Yue Guo, Matteo Aldeghi, Alba Cervera-Lierta, Pascal Friederich, Gabriel dos Passos Gomes, Florian Häse, Adrian Jinich, AkshatKumar Nigam, et al. On scientific understanding with artificial intelligence. _Nat. Rev. Phys._ , 4(12):761–769, 2022. 

38 

## **Supporting information El Agente Cuántico: Automating quantum simulations** 

## **S1 Agents and tools** 

**Table S1** Summary of the current agents (A) and tools (T) comprised in El Agente cuántico. 

|**Label**|**Description**|**LLM model**|
|---|---|---|
|**Quantum scientist (A)**|A quantum-physics agent with access|claude-opus-4-5 (44)|
||to the literature and software||
||documentation that can delegate tasks||
||to specialist experts. Responsible for||
||quantum simulation tasks and||
||high-level planning.||
|**Cudaq expert (A)**|A specialized quantum computing and|claude-opus-4-5 (44)|
||algorithms agent that generates||
||CUDA-QX simulation code.||
|**Pennylane expert (A)**|A specialized quantum computing|claude-opus-4-5 (44)|
||agent that generates PennyLane||
||simulation code.||
|**Qiskit expert (A)**|A specialized quantum computing|claude-opus-4-5 (44)|
||agent that generates Qiskit simulation||
||code.||
|**Qutip expert (A)**|A specialized quantum physics agent|claude-opus-4-5 (44)|
||that generates QuTiP 5.2 simulation||
||code.||
|**Tenpy expert (A)**|A specialized physicist with expertise|claude-opus-4-5 (44)|
||in TeNPy and tensor-network methods.||
|**Tequila expert (A)**|A specialized quantum algorithms|claude-opus-4-5 (44)|
||agent that generates Tequila simulation||
||code.||
|**Literature search (T)**|Search the scientifc literature for|gpt-5.2 (42)|
||information.||
|**PDF reader (T)**|Answers questions by searching and|gpt-5-mini|
||extracting information from a provided||
||PDF document.||
|**Deepsearch (T)**|Search the expert manuals (e.g.,|gpt-5.2 (42)|
||CUDA-Q, QuTiP, PennyLane, etc)||
||for API documentation.||
|**Python REPL (T)**|Accesses a Python terminal to run|N/A|
||Python code and interacts with the||
||local machine as needed.||
|**Submit python jobs (T)**|Executes Python code on the HPC via|N/A|
||SLURM with full workspace||
||synchronization.||
|**View**png**file (T)**|Allows visualization of .png fles.|N/A|
|**Ask for clarification (T)**|Ask for clarifcations from user.|N/A|



S1 

## **S2 Log sessions** 

Here we outline the log sessions corresponding to all problems presented in the main text. For clarity, we omit comments related to file paths and figure handling, and we do not display the generated code. Nevertheless, all code and figures are publicly available via https://doi.org/10.5683/SP3/UAKARI. 

## **S2.1 Variational quantum eigensolver** 

## **Prompt** 

Read the CUDA manual and compute the VQE energy of H2 over bond distances from 0.4 to 2.2 Å and compare against the exact answer. For the plot, create a figure of the dissociation curve and explain the physical meaning and where the curve deviates from exact energies. 

## **Quantum scientist agent** 

**Action:** I’ll help you compute the VQE energy of H2 across bond distances and compare with exact results. Let me first search the CUDA-Q manual to understand the proper approach for molecular VQE calculations. 

**Tool used:** cudaq deepsearch 

query: VQE variational quantum eigensolver molecular hydrogen H2 energy calculation. 

query: CUDA-Q molecular Hamiltonian chemistry create molecular hamiltonian spin op exact diagonalization. 

S2 

## **Quantum scientist agent** 

**Action:** I now have sufficient information from the CUDA-Q manual to propose a high-level plan. Based on my search, here’s what I found: 

## **Proposed High Level Plan:** 

- Step 1: Generate Data (VQE + Exact Energies) Run in a single script that loops over bond distances from 0.4 to 2.2 Å: 

   - For each bond distance, create the _H_ 2 molecular Hamiltonian with STO-3G basis using cudaq.chemistry.create_molecular_hamiltonian(). 

   - Compute VQE energy using an appropriate variational ansatz (e.g., UCCSD-inspired or hardware-efficient). Store all results (bond distance, VQE energy, exact energy) 

   - Compute exact ground-state energy via matrix diagonalization of the Hamiltonian Store all results (bond distance, VQE energy, exact energy) 

- Step 2: Post-Analysis and Visualization. 

   - Generate publication-quality dissociation curve plot comparing VQE vs. exact energies. 

   - Compute and plot the energy error (VQE-exact) across bond distances. 

   - Physical Context (Important for Interpretation): 

      - ∗Near equilibrium ( _∼_ 0.74 Å): Single-reference character dominates. 

      - ∗ Stretched bonds ( _>_ 1 _._ 5 Å): Strong correlation and multi-reference character emerge as the bond breaks. 

      - ∗ Expected VQE challenge: At large distances, _H_ 2 dissociates to 2 open-shell H atoms. A simple single-determinant ansatz may struggle, while exact diagonalization captures all correlations. A simple single-determinant ansatz may struggle, while exact diagonalization captures all correlations 

**Shall I proceed with this 2-step plan? (yes / no / modify)** If you approve, I will delegate Step 1 to the CUDA-Q expert to generate the computational code. 

## **User:** Yes 

## **Quantum scientist agent** 

**Action:** Proceeding with Step 1. I will delegate to the CUDA-Q expert to generate the VQE code for the _H_ 2 dissociation curve. 

**Tool used:** cudaq expert 

message2agent: _Omitting for brevity_ 

## **Cudaq expert agent** 

**Action:** Let me search for more specific CUDA-Q VQE documentation: 

**Tool used:** cudaq deepsearch 

query: cudaq VQE optimize observe kernel hardware efficient ansatz 

query: cudaq.chemistry molecular hamiltonian pyscf openfermion spin_op to_matrix 

S3 

## **Cudaq expert agent** 

**Action:** Now I have good documentation. Let me create a minimal test first to verify the API works, then expand to the full dissociation curve: 

**Tool used:** submit_python_slurm code: _Omitting for brevity_ 

## **Cudaq expert agent** 

**Task Completed:** The VQE calculation completed successfully! The results show excellent agreement between VQE (UCCSD) and exact energies. Now let me delegate the visualization analysis and physical interpretation to the quantum scientist. 

## **Quantum scientist agent** 

**Action:** I’ll analyze the _H_ 2 VQE dissociation curve results. Let me start by reading the data file and displaying the generated plot, then provide a comprehensive analysis 

**Tool used:** repl_tool 

**code:** _Omitting for brevity_ 

## **Quantum scientist agent** 

**Action:** Task Complete: _H_ 2 VQE Dissociation Curve Analysis. 

**Summary:** I successfully computed the VQE energy of _H_ 2 across bond distances from 0.4 to 2.2 Åusing CUDA-Q on CPU (qpp-cpu target) and compared against exact (FCI) energies. 

## **Report Highlights:** 

## • **LEFT PANEL (PES):** 

- Morselike curve: Repulsive wall _→_ equilibrium (0.7 Å) _→_ dissociation limit (-1.0 Ha). 

- VQE _≈_ Exact: Coral circles surround navy dots perfectly - sub- _µ_ Ha agreement. 

- HF failure: Diverges at stretched geometries (19 _→_ 195 mHa error) 

## • **RIGHT PANEL (Errors, Log Scale):** 

- HF errors: _∼_ 10[2] mHa (ABOVE chemical accuracy) - fails at all points. 

**–** VQE errors: _∼_ 10 _[−]_[3] mHa (FAR BELOW chemical accuracy) — succeeds at all points. 

- 5 orders of magnitude separate VQE from HF. 

## • **Physical Interpretation:** 

- Static correlation problem: HF uses single determinant, cannot represent entangled dissociation state. 

**–** HF predicts 50% _H_[+] _H[−]_ ionic character at dissociation — physically wrong. 

- VQE/UCCSD captures the correct superposition via parameterized quantum circuit. 

S4 

## **S2.2 Bell states preparation** 

## **Prompt** 

Read the CUDA-Q manual and create a 2-qubit quantum circuit that prepares a Bell state ( _|_ 00 _⟩_ + _|_ 11 _⟩_ ) _/√_ 2. Start in _|_ 00 _⟩_ . Apply a Hadamard gate on qubit 0 and then a CNOT with control qubit 0 and target qubit 1. Measure both qubits in the computational _⟨Z⟩_ basis with 4096 shots and return the measurement counts. From those counts, compute and return the expectation value of _Z ⊗ Z_ . Then also estimate the expectation value of _X ⊗ X_ by measuring in the X basis, again with 4096 shots, and return both the counts and the estimated _⟨X ⊗ X⟩_ . Plot and analyze the results. 

## **Quantum scientist agent** 

**Action:** I’ll help you create a CUDA-Q simulation for Bell state preparation and measurement. Let me first search the CUDA-Q manual to ensure we use the correct syntax for this task. 

**Tool used:** cudaq deepsearch 

query: Bell state preparation Hadamard CNOT gate measurement expectation value sample. 

query: cudaq sample shots_count kernel x.h cx measure X basis rotation. 

## **Quantum scientist agent** 

**Action:** I now have sufficient information from the CUDA-Q manual. 

## **Proposed High Level Plan:** 

**Step 1:** Create CUDA-Q code that: (a) Prepares Bell state, (b) Measures in Z-basis (4096 shots) _→_ compute _⟨Z ⊗ Z⟩_ , (c) Measures in X-basis (4096 shots) _→_ compute _⟨X ⊗ X⟩_ , (d) Generates publicationquality plots of measurement counts and expectation values with error bars. 

This is a single-step workflow since all computations are independent once the code is written, and the plotting can be done immediately after obtaining results within the same script. 

## **Outputs to deliver:** 

- Measurement counts for Z-basis (dictionary) 

- Measurement counts for X-basis (dictionary) 

- Computed _⟨Z ⊗ Z⟩_ and _⟨X ⊗ X⟩_ 

- Publication-quality figure showing histogram of counts and expectation values 

**Shall I proceed with this plan?** (yes / no / modify) 

## **User:** Yes 

## **Quantum scientist agent** 

**Action:** Proceeding with the plan. I’ll delegate this task to the CUDA-Q expert. 

**Tool used:** cudaq expert message2agent: _Omitting for brevity_ 

S5 

## **Cudaq expert agent** 

**Action:** I’ll first search the CUDA-Q manual to understand the correct syntax for measurements and sampling, then create the script. 

**Tool used:** cudaq deepsearch 

query: cudaq.sample mz mx measurement kernel example 

query: cudaq qvector qubit Bell state cx CNOT Hadamard h gate example 

## **Cudaq expert agent** 

**Action:** Now I have the correct syntax. Let me first debug with a minimal version to ensure the measurement extraction works correctly: 

**Tool used:** submit_python_slurm 

code: _Omitting for brevity_ 

## **Cudaq expert agent** 

**Action:** I see the issue - the result object conversion and X-basis measurement need different handling. Let me fix this: 

**Tool used:** submit_python_slurm 

code: _Omitting for brevity_ 

## **Cudaq expert agent** 

**Task Completed:** The CUDA-Q simulation completed successfully! I created a complete CUDA-Q Python script for Bell state preparation and measurement. 

## **Quantum scientist agent** 

**Action:** Excellent! The CUDA-Q expert completed the simulation. Let me view the generated plot to verify the quality: 

**Tool used:** repl_tool 

**code:** _Omitting for brevity_ 

S6 

## **Quantum scientist agent** 

**Action:** Task Complete: Bell State Experiment. 

## **Summary:** 

- 2-qubit system initialized in _|_ 00 _⟩_ . 

- Hadamard gate on qubit 0. 

- CNOT with control=0, target=1. 

- Prepared Bell state: _|_ Φ[+] _⟩_ = ( _|_ 00 _⟩_ + _|_ 11 _⟩_ ) _/√_ 2 

**Bell State** _|_ Φ[+] _⟩_ **Measurement Analysis** 

- **Panel 1: Z-Basis Measurements.** The near-equal split between _|_ 00 _⟩_ (51.4%) and _|_ 11 _⟩_ (48.6%) reveals the essence of quantum entanglement. When we measure qubit 0 and find it in state _|_ 0 _⟩_ , qubit 1 is always found in _|_ 0 _⟩_ ; likewise, measuring _|_ 1 _⟩_ on one qubit guarantees _|_ 1 _⟩_ on the other. The complete _|_ 01 _⟩_ and _|_ 10 _⟩_ outcomes demonstrates perfect correlation—the qubits share a definite relationship even though neither has a predetermined individual value. The small deviation from exactly 50/50 is statistical noise from finite sampling (4096 shots). 

- **Panel2: X-BasisMeasurements.** The _∼_ 50/50 split persists when measuring in the X-basis, confirming that correlations exist in multiple measurement bases simultaneously. This is the hallmark of genuine quantum entanglement. A classically correlated state (like a coin flip that sets both qubits identically) would show correlations in Z but appear random in X. The Bell state maintains perfect correlations in both bases—a feat impossible without quantum superposition. This multi-basis correlation is what enables violations of Bell inequalities. 

- **Panel 3: Expectation Values.** 

   - _⟨Z ⊗ Z⟩_ = +1 (perfect correlation in Z-basis), 

   - _⟨X ⊗ X⟩_ = +1 (perfect correlation in X-basis), 

   - _⟨Y ⊗ Y ⟩_ = _−_ 1 (perfect anti-correlation in Y-basis). 

The combination (+1 _,_ +1 _, −_ 1) uniquely identifies _|_ Φ[+] _⟩_ among the four Bell states. 

## **S2.3 Thermal states via imaginary-time evolution** 

**Prompt** Prepare a Gibbs state of a 1D Hubbard model on a classical computer using imaginary-time evolution. Consider a 10-site Hubbard chain with open boundary conditions, hopping _t_ = 1, on-site interaction _U_ = 4, and half filling. Target an inverse temperature 1 _/T_ = 2. Explain how to validate that the resulting state is thermal by checking energies and occupancies. 

S7 

## **Quantum scientist agent** 

**Action:** This is a well-defined finite-temperature quantum many-body simulation task. Let me analyze the problem and propose a plan. 

**Recommended approach:** I recommend using TeNPy with the purification method for imaginary-time evolution. TeNPy has a built-in FermiHubbardModel and excellent support for finite-temperature simulations via Matrix Product Density Operators (MPDO) or purification. 

## **Proposed High-Level Plan:** 

- **Step 1: Setup and Reference Computation.** 

   - Define the 1D Hubbard Hamiltonian in TeNPy with specified parameters. 

- **Step 2: Imaginary-Time Evolution and Validation.** 

   - Prepare initial maximally mixed (infinite-temperature) purified state. 

   - Perform imaginary-time TEBD evolution from _β_ = 0 to _β_ = 2. 

   - Measure thermal observables: 

      - ∗Total energy _⟨H⟩_ . 

      - ∗Site occupancies _⟨ni ↑⟩_ , _⟨ni ↓⟩_ 

      - ∗Double occupancy _⟨ni ↑ ni ↓⟩_ 

      - ∗Von Neumann entropy S. 

## **Would you like me to proceed with this 2-step plan?** 

## **User:** Yes 

## **Quantum scientist agent** 

**Action:** Proceeding with the plan. I’ll delegate this to the TeNPy expert who specializes in tensor network simulations of strongly correlated systems. 

**Tool used:** tenpy expert 

message2agent: _Omitting for brevity_ 

## **Tenpy expert agent** 

**Action:** I need to search the TeNPy manual first to ensure I use the correct API for the Hubbard model and purification-based imaginary-time evolution. 

**Tool used:** tenpy deepsearch 

query: FermiHubbardModel purification imaginary time evolution thermal state TEBD 

query: PurificationMPS from_infiniteT charge_sector canonical_ensemble particle number conservation expectation_value 

## **Tenpy expert agent** 

**Action:** Now I have all the information needed. Let me create a minimal working version first to test the approach: 

**Tool used:** submit_python_slurm 

code: _Omitting for brevity_ 

S8 

## **Tenpy expert agent** 

**Action:** The exact diagonalization failed due to size issues. Let me fix this by using sparse diagonalization and properly setting max_size: 

**Tool used:** submit_python_slurm code: _Omitting for brevity_ 

## **Tenpy expert agent** 

**Action:** The exact diagonalization failed due to size issues. Let me fix this by using sparse diagonalization and properly setting max_size: 

**Tool used:** submit_python_slurm 

code: _Omitting for brevity_ 

## **Tenpy expert agent** 

**Action:** I see several issues: 

- The charge sector extraction from ED is incorrect (found only 1 state). 

- The from_infiniteT_canonical API is different. 

- The TEBD is not evolving (bond dim stays at 1). 

Let me search for the correct API and fix these issues: 

**Tool used:** tenpy deepsearch 

query: PurificationTEBD run_imaginary imaginary time evolution bond dimension not growing 

query: PurificationTEBD options parameters TEBD order dt trunc_params initialization 

## **Tenpy expert agent** 

**Action:** Now I understand the issues. Let me fix the code with proper TEBD options and correct ED charge sector extraction: 

**Tool used:** submit_python_slurm 

code: _Omitting for brevity_ 

## **Tenpy expert agent** 

**Action:** The simulation completed successfully. Let me now delegate the visualization and analysis to the quantum scientist. 

**message2agent:** _Omitting for brevity_ 

## **Quantum scientist agent** 

**Action:** I’ll analyze and visualize the Gibbs state preparation results for the 1D Hubbard model. Let me start by loading the data and exploring its structure. 

**Tool used:** repl_tool 

**code:** _Omitting for brevity_ 

S9 

## **Quantum scientist agent** 

**Action:** Analysis Completed. I’ve created all requested visualizations and comprehensive physical interpretations for the Gibbs state preparation of the 10-site Hubbard chain at _β_ = 2. 

## **Physical Insights** 

- **Panel (a), energy vs 1/T.** As temperature decreases, the Boltzmann distribution favors lower-energy states, so the average energy drops monotonically toward the ground state. 

- **Panel (b), site occupancy.** The canonical ensemble at fixed _N_ = 10 electrons maintains exactly one electron per site on average, as expected for half-filling. 

- **Panel (c), Double occupancy.** The strong on-site repulsion _U_ = 4 suppresses double occupancy by 64%. This is the hallmark of Hubbard physics—electrons avoid sharing sites due to Coulomb repulsion. 

- **Panel (d), entanglement entropy.** Von Neumann entropy S at each bond cutting the chain. The purification MPS has entanglement from both quantum correlations and thermal mixing. Higher entropy at the center is typical for finite systems with open boundaries. 

## **S2.4 Trotter decomposition** 

## **Prompt** 

Read the CUDA-Q manual and implement a simulation of the transverse-field Ising model for a 10-qubit chain with open boundary conditions. Compute the dynamics of the magnetization _⟨Z⟩_ for two parameter regimes, _J_ coup = 10 _J_ with _h_ = 0 _._ 1 _J_ , and _J_ coup = 0 _._ 1 _J_ with _h_ = 10 _J_ . Start the evolution from a Haar-random initial state and simulate the dynamics over a total time of 10 seconds using a second-order product formula with 1000 time steps. Generate a heatmap where the x-axis corresponds to qubit position, the y-axis to time, and the color scale to the _Z_ -magnetization, for each of these two phases. Analyze the resulting magnetization dynamics between the two parameter choices. 

## **Quantum scientist agent** 

**Action:** I’ll help you simulate the transverse-field Ising model dynamics using CUDA-Q. This is an interesting task that will compare magnetization dynamics in two distinct quantum phases - the ferromagnetic phase (strong coupling) and paramagnetic phase (strong transverse field). Let me first search the CUDA-Q manual to understand the best approach for Hamiltonian simulation with product formulas. 

**Tool used:** cudaq deepsearch 

query: Hamiltonian simulation product formula Trotter time evolution dynamics 

query: state vector simulation expectation value measurement pauli operators spin operators. 

query: cudaq.State from_data numpy array initial state qvector initialization. 

S10 

## **Quantum scientist agent** 

**Action:** Based on my search of the CUDA-Q documentation, I have gathered enough information to propose a high-level plan. Let me outline the key considerations and the proposed workflow. 

## **Proposed Workflow (2 Steps)** 

- **Step 1: Implement and Run Simulations** (Both regimes can run in parallel) 

**–** Implement Trotter-based time evolution for the 10-qubit TFIM with open boundary conditions 

**–** Generate a Haar-random initial state (using NumPy/SciPy unitary sampling, then converted to initial circuit or direct state manipulation) 

- Simulate dynamics for both parameter regimes: 

∗Regime 1: _J_ coup = 10, _h_ = 0 _._ 1 (ferromagnetic) 

∗Regime 2: _J_ coup = 0 _._ 1, _h_ = 10 (paramagnetic) 

**–** Store _⟨Zi_ ( _t_ ) _⟩_ for all 10 qubits at all 1000 time steps 

- **Step 2: Visualization and Analysis** (Depends on Step 1 output) 

   - Generate publication-quality heatmaps for both regimes: 

∗x-axis: qubit position (0–9) 

- ∗y-axis: time (0–10) 

- ∗color: Z-magnetization 

**–** Perform comparative analysis of the magnetization dynamics between the two phases 

- Interpret results in terms of the known physics of TFIM phase behavior 

## **Should I proceed with this plan?** (yes / no / modify) 

## **User:** Yes 

## **Quantum scientist agent** 

**Action:** This is a quantum dynamics simulation task that should be handled by the CUDA-Q expert. Let me delegate this to them with all the specific requirements. 

**Tool used:** cudaq expert. 

**message2agent:** _Omitting for brevity_ 

## **Cudaq expert agent** 

**Action:** I’ll first search the CUDA-Q manual to understand the proper way to implement quantum dynamics simulations with Trotter decomposition. 

**Tool used:** cudaq deepsearch 

query: quantum dynamics simulation Trotter decomposition product formula time evolution 

query: exp_pauli cudaq second order Trotter Suzuki decomposition time step 

query: cudaq observe expectation value spin operator get_state random initial state 

S11 

## **Cudaq expert agent** 

**Action:** Now I have all the information needed. Let me create a complete CUDA-Q simulation for the transverse field Ising model dynamics using second-order Trotter decomposition. 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Cudaq expert agent** 

**Action:** I see the issue - the exp_pauli function needs to be called differently within kernels. Let me search for the correct syntax 

**Tool used:** cudaq deepsearch 

query: exp_pauli kernel syntax pauli_word cudaq.kernel decorator 

## **Cudaq expert agent** 

**Action:** I see the issue - inside a @cudaq.kernel, you call exp_pauli directly without the cudaq. prefix. Let me fix the code: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Cudaq expert agent** 

**Action:** The simulation completed successfully. Let me now delegate to the postprocessing expert to analyze the results and provide enhanced visualizations. 

**message2agent:** _Omitting for brevity_ 

## **Quantum scientist agent** 

**Action:** I’ll analyze the CUDA-Q simulation results for the transverse field Ising model dynamics. Let me load the data and create comprehensive visualizations 

**Tool used:** repl_tool 

**code:** _Omitting for brevity_ 

S12 

## **Quantum scientist agent** 

**Action:** Simulation Successfully Executed. The CUDA-Q simulation of the transverse field Ising model dynamics has been completed for both parameter regimes using second-order Trotter-Suzuki decomposition. 

## **Physical Insights** 

## **Left panel, strong coupling (J_coup=10J, h=0.1J).** 

- Slow dynamics with characteristic relaxation time _∼_ 2s 

- Collective behavior dominates with correlations propagating through the chain 

- The system shows slow thermalization toward _⟨Z⟩≈_ 0 

## **Right Panel - Strong Field Regime (J_coup=0.1J, h=10J):** 

- Fast oscillatory dynamics (Rabi-like precession) with period _∼_ 0.06s 

- Each qubit precesses nearly independently due to weak coupling 

- Clear striped pattern from rapid local oscillations 

- Short correlation length between neighboring qubits 

The contrast clearly illustrates the quantum phase transition behavior of the Transverse-field Ising model: the ferromagnetic phase (strong coupling) vs. the paramagnetic phase (strong field). 

## **S2.5 Lindbladian dynamics** 

## **Prompt** 

Read the QuTiP manual and compare the dynamics of a single qubit under unitary evolution and under open system Lindblad evolution using: 

**Hamiltonian:** _H_ = _σx_ +[1] 2 _[σ][z]_[,] **[Initial condition:]**[Use][the][plus][and][minus][eigenstates][of][X.] **[Dissipation:]**[Use][a] collapse operator _C_ = _[√] γσ−_ , with _γ_ = 0.2. **Evolution:** Use a time range from _t_ = [0 _,_ 40] with 400 time steps. **Output:** Plot the expectation value of Z as a function of time for each initial state and compare closed and open dynamics. 

## **Quantum scientist agent** 

**Action:** I’ll help you set up this qubit dynamics comparison using QuTiP. Let me first search the QuTiP manual to ensure we use the correct syntax for both solvers. 

**Tool used:** qutip deepsearch 

query: sesolve mesolve Lindblad master equation qubit evolution collapse operator expectation value 

S13 

## **Quantum scientist agent** 

**Action:** I have the necessary information from the QuTiP manual. This is a well-defined task that can be executed efficiently. Let me propose a high-level plan: 

## **Proposed Plan** 

**Step 1: Single execution step** — Generate QuTiP code that performs all simulations and creates the comparison plot. 

The code will: 

• Define Hamiltonian: _H_ = _σx_ +[1] 2 _[σ][z]_ • Prepare initial states: _|_ + _⟩_ = ~~_√_~~ 12[(] _[|]_[0] _[⟩]_[+] _[ |]_[1] _[⟩]_[)][and] _[|−⟩]_[=] ~~_√_~~ 12[(] _[|]_[0] _[⟩−|]_[1] _[⟩]_[)] • Define collapse operator: _C_ = _√_ 0 _._ 2 _, σ−_ 

- Run 4 simulations in parallel (conceptually): 

   - sesolve (unitary) for _|_ + _⟩_ 

   - sesolve (unitary) for _|−⟩_ 

   - mesolve (Lindblad) for _|_ + _⟩_ 

   - mesolve (Lindblad) for _|−⟩_ 

- Plot _⟨σz⟩_ ( _t_ ) for all 4 cases with clear labels distinguishing closed vs. open dynamics 

## **Should I proceed with this plan?** (yes / no / modify) 

**User:** Yes 

## **Quantum scientist agent** 

**Action:** I’ll delegate this task to the QuTiP expert now. 

**Tool used:** qutip expert. 

**message2agent:** _Omitting for brevity_ 

## **Qutip expert agent** 

**Action:** II’ll search the QuTiP 5.2 manual first to ensure I use the correct API for sesolve and mesolve. 

**Tool used:** qutip deepsearch 

query: sesolve mesolve Lindblad dynamics expectation values collapse operators QuTiP 5.2 

## **Qutip expert agent** 

**Action:** Now I have the correct QuTiP 5.2 API information. Let me generate the code and execute it: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Qutip expert agent** 

**Action:** Task Completed Successfully. 

**message2agent:** I generated and executed QuTiP 5.2 code comparing unitary vs Lindblad dynamics for a single qubit. 

S14 

## **Quantum scientist agent** 

**Action:** Task Complete. Here’s the summary: 

## **Figure Description:** 

- **Panel (a), Unitary Evolution:** Shows persistent Rabi-like oscillations for both _|_ + _⟩_ (dark blue, solid) and _|−⟩_ (light blue, dashed) initial states with amplitude _∼_ 0.4. 

- **Panel (b), Lindblad Evolution:** Shows damped oscillations converging to a steady state with a horizontal dashed line at _⟨Z⟩≈_ -0.33 

## **Physical interpretation:** 

- The Hamiltonian _H_ = _σx_ +0 _._ 5 _σz_ creates a tilted effective magnetic field causing Rabi-like precession. 

- The collapse operator _C_ = _[√] γσ−_ induces spontaneous emission ( _|_ 1 _⟩→|_ 0 _⟩_ decay). 

- Competition between coherent driving (H) and dissipation ( _γ_ ) produces a non-trivial steady state where _∼_ 67% population is in _|_ 0 _⟩_ . 

- Crucially, the steady state is unique. 

- Both initial states converge to the same value, demonstrating loss of memory of initial conditions (a hallmark of open quantum systems). 

## **S2.6 Hierarchical equations of motion** 

**Prompt** Read QuTiP’s manual and use the HEOM implementation to simulate exciton dynamics in the Fenna–Matthews–Olson (FMO) complex. Use the following parameters: 

**==> picture [366 x 97] intentionally omitted <==**

**----- Start of picture text -----**<br>
|||||||||||||||||||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|240|.|0|−|87|.|7|5|.|5|−|5|.|9|6|.|7|−|13|.|7|−|9|.|9|
|||
||−|87|.|7|315|.|0|30|.|8|8|.|2|0|.|7|11|.|8|4|.|3||
|||
||5|.|5|30|.|8|0|.|0|−|53|.|5|−|2|.|2|−|9|.|6|6|.|0||
|||
|System Hamiltonian|(115;|116;|117) =||−|5|.|9|8|.|2|−|53|.|5|130|.|0|−|70|.|7|−|17|.|0|−|63|.|3|.|
||6|.|7|0|.|7|−|2|.|2|−|70|.|7|285|.|0|81|.|1|−|1|.|3||
|||
||−|13|.|7|11|.|8|−|9|.|6|−|17|.|0|81|.|1|435|.|0|39|.|7||
|−|9|.|9|4|.|3|6|.|0|−|63|.|3|−|1|.|3|39|.|7|245|.|0|
|||

**----- End of picture text -----**<br>


**Bath parameter:** Drude–Lorentz spectral density with reorganization energy _λ_ = 35 cm _[−]_[1] , cutoff time 1 _/γ_ = 50 fs, and temperature _T_ = 300 K and _T_ = 77 K. Hierarchy depth _L_ = 4, number of Matsubara terms _K_ = 2. **Initial condition:** system localized on site 0. **Dynamics:** propagate for 1 ps and record site populations vs. time. **Report:** Plot all site populations as a function of time at the two different temperatures and analyze the results. 

## **Quantum scientist agent** 

**Action:** I’ll help you simulate the exciton dynamics in the FMO complex using QuTiP’s HEOM implementation. This is a classic problem in quantum biology for understanding energy transfer in photosynthetic systems. Let me first search the QuTiP manual to understand the HEOM implementation details and ensure we use the correct API. 

**Tool used:** qutip deepsearch 

query: HEOM hierarchical equations of motion Drude Lorentz spectral density bath solver. 

S15 

## **Quantum scientist agent** 

**Action:** I found detailed information about QuTiP’s HEOM implementation. Now let me formulate a high-level plan for this FMO simulation. 

## **High-Level Plan: FMO Exciton Dynamics with HEOM** 

Key Considerations I’ve Identified: 

- **Multi-bath setup:** The FMO complex has 7 chromophores, each coupled to its **own independent bath** (7 baths total). This is crucial for correct physics. 

- **Unit consistency:** The Hamiltonian is in cm _[−]_[1] , bath parameters need consistent units: 

   - _γ_ = 1/(50 fs) needs conversion to cm _[−]_[1] (using ℏ = 5.309 cm _[−]_[1] _·_ ps) 

   - Temperature needs conversion via _kBT_ in cm _[−]_[1] ( _kB_ = 0.695 cm _[−]_[1] /K) 

- **Coupling operators:** Each site i has coupling operator _Qi_ = _|i⟩⟨i|_ (local site projector) 

- **Computational cost:** 7 baths x K=2 Matsubara terms x L=4 depth can generate a large hierarchy - this is manageable but not trivial. 

## **Proposed Workflow (2 Steps):** 

- **Step 1: Code Generation & Simulation** 

   - Generate QuTiP HEOM simulation code for the 7-site FMO complex 

   - Include both T = 300 K and T = 77 K simulations 

   - Set up proper unit conversions (cm _[−]_[1] throughout) 

   - Use DrudeLorentzBath with proper multi-bath configuration 

   - Run dynamics for 1 ps with initial condition on site 0 

   - Save population data for all 7 sites vs. time 

- **Step 2: Post-Processing & Analysis** 

   - Generate publication-quality plots of site populations vs. time 

   - Create two panels (or two figures): one for 300 K, one for 77 K 

   - Analyze and compare coherence timescales and relaxation behavior at both temperatures 

   - Identify key physical observations (coherent oscillations, thermalization timescales) 

**Do you want me to proceed with this plan?** Also, would you like me to perform a literature search on FMO dynamics benchmarks to validate our results against published simulations? 

**User:** Yes 

## **Quantum scientist agent** 

**Action:** Proceeding with **Step 1:** Delegating to the QuTiP expert to generate the HEOM simulation code for FMO dynamics. 

**Tool used:** qutip expert 

**message2agent:** _Omitting for brevity_ 

S16 

## **Qutip expert agent** 

**Action:** I’ll help you generate QuTiP 5.2 code for simulating exciton dynamics in the FMO complex using the HEOM solver. Let me first search the QuTiP manual to ensure I use the correct API for HEOM in version 5.2. 

**Tool used:** qutip deepsearch 

query: HEOM solver DrudeLorentzBath multi-bath exciton dynamics 

## **Qutip expert agent** 

**Action:** I have the information needed about the QuTiP 5.2 HEOM API. Now let me generate and execute the FMO simulation code. 

**Tool used:** qsubmit_python_slurm 

**code:** _Omitting for brevity_ 

## **Qutip expert agent** 

**Action:** The HEOM simulations completed successfully for both temperatures. The results show interesting physics: 

- T = 300 K: Slower, more thermally-driven dynamics with population spreading across sites 

- T = 77 K: More coherent dynamics with population staying concentrated on fewer sites 

Now let me delegate the visualization and analysis to the quantum scientist 

**message2agent:** _Omitting for brevity_ 

## **Quantum scientist agent** 

**Action:** I’ll create publication-quality visualizations for the FMO complex exciton dynamics. This is a classic quantum biology problem - the FMO complex is a pigment-protein complex that facilitates energy transfer in green sulfur bacteria. Let me start by reading the data and creating the visualizations: 

**Tool used:** repl_tool 

**code:** _Omitting for brevity_ 

## **Quantum scientist agent** 

**Action:** I see the data contains complex number strings. Let me parse them properly and check the actual format: 

**Tool used:** repl_tool 

**code:** _Omitting for brevity_ 

## **Quantum scientist agent** 

**Action:** Now I understand the format - the data contains complex numbers. Let me parse them correctly and extract real population values:: 

**Tool used:** repl_tool 

**code:** _Omitting for brevity_ 

S17 

## **Quantum scientist agent** 

**Action:** Data parsed successfully. Now let me create the publication-quality visualizations: 

**Tool used:** repl_tool 

**code:** _Omitting for brevity_ 

## **Quantum scientist agent** 

**Action:** Simulation Completed Successfully. The HEOM simulation of the Fenna-Matthews-Olson complex has been completed using QuTiP 5.2. Here are the key results: 

- **Left Panel (T = 300 K, Room Temperature):** 

   - The initially excited Site 0 decays smoothly from population 1.0 to about 0.27 with only weak oscillations. 

   - Population spreads broadly across the complex: Sites 1–3 each reach roughly 13–22 percent, and even high-energy Site 5 reaches about 4 percent. 

   - The overall behavior is predominantly incoherent and diffusive. 

## • **Right Panel (T = 77 K, Cryogenic):** 

   - Site 0 undergoes a rapid drop in the first _∼_ 100 fs followed by clear oscillations and partial recovery, retaining about 46 percent population at 1 ps. 

   - Oscillatory features appear across several sites, and population remains concentrated on lower-energy sites (mainly 2 and 3), while higher-energym sites (4–6) stay below 2 percent. 

   - The dynamics are more coherent and wavelike than at room temperature. 

- **Consistency with Literature** 

   - The energy funnel behavior toward Site 3 (BChl 3) is well-documented 

   - Temperature-dependent rates agree with theoretical predictions 

## **S2.7 Quantum optimal control** 

## **Prompt** 

Read the QuTiP manual and solve a quantum control problem for a Lambda-type three-level system (levels _|_ 1 _⟩_ , _|_ 2 _⟩_ , _|_ 3 _⟩_ ). The goal is to transfer population from the ground state _|_ 1 _⟩_ to the target state _|_ 3 _⟩_ while minimizing the occupation of the intermediate state _|_ 2 _⟩_ . 

**Control Hamiltonians:** _Hc_ 1 = ( _|_ 1 _⟩⟨_ 2 _|_ + _|_ 2 _⟩⟨_ 1 _|_ ) (Pump coupling). _Hc_ 2 = _|_ 2 _⟩⟨_ 3 _|_ + _|_ 3 _⟩⟨_ 2 _|_ ) (Stokes coupling). **The Optimization:** Use the GRAPE algorithm. **Duration:** T=40 (arbitrary time units) with time slots = 3000. **Validation:** After optimizing the pulses, run a time-evolution simulation using the generated pulses to verify the dynamics. **Output:** A plot showing the Control Pulses (Amplitude vs Time) and a plot showing the populations vs Time. Print the final fidelity. 

S18 

## **Quantum scientist agent** 

**Action:** I’ll help you with this quantum control problem using QuTiP’s GRAPE algorithm for a Lambdatype three-level system. This is a classic STIRAP-like problem where we want to achieve population transfer while avoiding the intermediate state. Let me first search the QuTiP manual to understand the GRAPE implementation details in QuTiP 5.2 

**Tool used:** qutip deepsearch 

query: GRAPE algorithm quantum control optimization pulse 

query: optimize_pulse state transfer fidelity three level system qutip-qtrl 

## **Quantum scientist agent** 

**Action:** Excellent! I now have comprehensive information about QuTiP’s GRAPE implementation. This is a well-defined Lambda-system quantum control problem (similar to STIRAP). Let me propose a high-level plan. 

## **High-Level Plan** 

**Objective:** Optimize control pulses for population transfer _|_ 1 _⟩→|_ 3 _⟩_ in a Lambda-type three-level system using GRAPE, while minimizing intermediate state _|_ 2 _⟩_ occupation. 

## **Step 1: GRAPE Optimization and Validation (single step - all tasks use same input)** 

- **Task 1a:** Set up the Lambda system Hamiltonians and run GRAPE optimization 

   - Drift Hamiltonian: _H_ 0 = 0 (no detunings specified) 

   - Control Hamiltonians: _Hc_ 1 (pump), _H_ ( _c_ 2) (Stokes) 

   - Initial state: _|_ 1 _⟩_ , Target state: _|_ 3 _⟩_ 

   - Duration T=40, time slots=3000 

- **Task 1b:** After optimization, run time evolution with mesolve using the optimized pulses 

- **Task 1c:** Generate publication-quality plots: 

   - Plot 1: Control pulse amplitudes vs time 

   - Plot 2: Populations of _|_ 1 _⟩_ , _|_ 2 _⟩_ , _|_ 3 _⟩_ vs time (print fidelity) 

## **Should I proceed with this plan? (yes / no / modify)** 

**User:** Yes 

## **Quantum scientist agent** 

**Action:** Proceeding with the plan. I’ll delegate this task to the QuTiP expert with all the necessary specifications. 

**Tool used:** qutip expert 

**message2agent:** _Omitting for brevity_ 

S19 

## **Qutip expert agent** 

**Action:** I’ll help you implement a GRAPE-based quantum control for a Lambda-type three-level system. First, let me search the QuTiP 5.2 documentation to verify the correct API for GRAPE optimization. 

**Tool used:** qutip deepsearch 

query: GRAPE optimize_pulse quantum control qutip-qtrl pulseoptim 

query: GRAPE state transfer fid_type UNIT PSU fidelity optimize_pulse initial target state 

## **Qutip expert agent** 

**Action:** Excellent! Now I have all the information I need. Let me start with a minimal working version to debug the GRAPE optimization, then expand to the full implementation. 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Qutip expert agent** 

**Action:** Good progress! The imports work. Let me fix the numpy import order and run a proper minimal test: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Qutip expert agent** 

**Action:** The minimal test works. Now let me implement the full solution with 3000 time slots, proper plotting, and mesolve validation: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Qutip expert agent** 

**Action:** The coefficient function format has changed in QuTiP 5.2. Let me search for the correct syntax: 

**Tool used:** qutip deepsearch 

query: GRAPE optimize_pulse quantum control qutip-qtrl pulseoptim query: mesolve time-dependent Hamiltonian coefficient function QobjEvo QuTiP 5 

## **Qutip expert agent** 

**Action:** I see the issue. QuTiP 5.2 has a different coefficient signature. Let me fix the code using array coefficients, which are better suited for GRAPE piecewise-constant pulses: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

S20 

## **Qutip expert agent** 

**Action:** I see the issue - the optimization is terminating abnormally and the pulses aren’t working properly. The "LIN" initial guess may be causing problems. Let me try with a random initial guess and add better debugging: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Qutip expert agent** 

**Action:** I found the issue - there’s a discrepancy between GRAPE’s reported fidelity and actual evolution. Let me investigate and fix this: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Qutip expert agent** 

**Action:** Let me fix the Qobj handling: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Qutip expert agent** 

**Action:** Now I understand - GRAPE’s internal evolution is correct (fidelity=1.0) but there’s a mismatch with manual reconstruction. Let me extract the dynamics properly and create the final working solution: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Qutip expert agent** 

**Action:** The optimization achieved perfect fidelity! But there’s an issue with the population dynamics extraction. The fwd_evo contains propagators, not states. Let me fix this properly: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Qutip expert agent** 

**Action:** The population extraction is still showing unphysical values. Let me fix this properly by using sesolve with correct coefficient handling for QuTiP 5.2: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Qutip expert agent** 

**Action:** I need to handle the QuTiP 5.2 return types correctly. Let me fix this: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

S21 

## **Qutip expert agent** 

**Action:** There’s still a discrepancy between GRAPE’s fidelity and my manual propagation. Let me investigate GRAPE’s dynamics generator convention 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Qutip expert agent** 

**Action:** Now I understand the issue. GRAPE uses a linearized propagator internally (for gradient computation), not the full matrix exponential. The optimized pulses ARE correct, but I need to use proper step-by-step unitary evolution matching GRAPE’s time discretization exactly: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Qutip expert agent** 

**Action:** The optimization now works perfectly. Both GRAPE and true unitary evolution show fidelity = 1.0. Let me save the complete final code and organize the files: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Qutip expert agent** 

**Action:** I see there’s a fundamental discrepancy - GRAPE uses linearized dynamics internally. Let me search for the proper way to do GRAPE with exact unitary propagators in QuTiP: 

**Tool used:** qutip deepsearch 

query: qutip-qoc GRAPE optimize exact unitary propagator prop_type DEF dynamics generator matrix exponential 

## **Qutip expert agent** 

**Action:** I found the issue! I need to explicitly specify dyn_type=’UNIT’ to get proper unitary dynamics. Let me fix this: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Qutip expert agent** 

**Action:** The optimization now works perfectly with dyn_type=’UNIT’. Both GRAPE and true unitary evolution show fidelity = 1.0. Let me save the complete final code and organize the files: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

S22 

## **Qutip expert agent** 

**Action:** Task Completed Successfully. The GRAPE quantum control optimization for the Lambdatype three-level system has been successfully implemented and validated. 

## **Critical Implementation Detail** 

The key fix that made GRAPE work correctly was adding dyn_type=’UNIT’ to the optimize_pulse() call. This ensures proper unitary dynamics with exact matrix exponential propagators (exp(-iHt)), rather than linearized approximations. 

## **Quantum scientist agent** 

**Action:** The GRAPE optimization completed successfully with excellent results. 

## **Physics Observations** 

The population dynamics plot shows: 

- **Left panel (Control pulses):** Both pulses are oscillatory and overlap in time. No STIRAP-like counterintuitive order. Amplitudes vary between _±_ 5 units. 

- **Right panel (Populations):** _P_ 1 (blue): Smoothly depletes from 1 _→_ 0. _P_ 2 (orange): Peaks at 83% mid-transfer, return to 0. _P_ 3 (green): build to _∼_ 1 _._ 0 (99.99999% fidelity) 

**Important Note:** The standard GRAPE algorithm optimizes only for final state fidelity, not for minimizing intermediate state occupation during the transfer. The solution found is mathematically optimal for the endpoint but does NOT minimize _|_ 2 _⟩_ occupation during evolution. If minimizing _|_ 2 _⟩_ population is critical, this would require: 

- Adding a penalty term to the cost function for intermediate state population 

- Using STIRAP-like pulse shapes as initial guesses (counter-intuitive ordering: Stokes before Pump) 

Would you like me to re-run the optimization with a modified cost function that penalizes intermediate state occupation? This would yield a solution closer to the adiabatic STIRAP protocol. 

**User:** No 

## **S2.8 Time-dependent product formulas** 

## **Prompt** 

Read CUDA-Q manual and simulate the Floquet dynamics of a periodically kicked Ising chain with 10 qubits and open boundary conditions. The system has nearest-neighbor _ZZ_ interactions with coupling _J_ = 1, and is kicked every _T_ = 1 by a global transverse field in X. Use a strong kick with strength _h_ = 2 _J_ so that the effect of the drive is clearly visible in the dynamics. Initialize the system in a Haar-random state and simulate the evolution for 10 Floquet periods. Plot a heatmap of _⟨Zi_ ( _t_ ) _⟩_ , with qubit index on the x-axis, Floquet step (time) on the y-axis, and color representing the local magnetization. 

## **Quantum scientist agent** 

**Action:** I’ll help you simulate Floquet dynamics of a periodically kicked Ising chain using CUDA-Q. This is an interesting quantum dynamics problem. Let me first search the CUDA-Q manual to understand the best approach for implementing this simulation. 

**Tool used:** cudaq deepsearch 

query: state vector simulation time evolution expectation value measurement spin operators 

query: cudaq get_state evolve simulation circuit state vector apply gate 

S23 

## **Quantum scientist agent** 

**Action:** I now have sufficient information from the CUDA-Q manual. Based on my research, I can formulate a high-level plan for this Floquet dynamics simulation. 

## **High-Level Plan: Floquet Dynamics of Kicked Ising Chain in CUDA-Q Physics Summary** 

- Hamiltonian during evolution: _HZZ_ = _J_[�] _[N] i_ =0 _[−]_[2] _[Z][i][Z][i]_[+1][with] _[J]_[= 1] 

- Kick operator: _U_ kick = exp( _−ih_[�] _i[X][i]_[)][with] _[h]_[ = 2] _[J]_[= 2] 

- Floquet unitary: _UF_ = _U_ kick _· UZZ_ where _UZZ_ = exp( _−iHZZT_ ) 

**Implementation Strategy.** CUDA-Q’s state-in/state-out pattern is well-suited: 

- Generate Haar-random initial state using NumPy 

- Build circuit kernels for ZZ evolution and X-kick 

- Iteratively apply Floquet unitary using cudaq.get_state() 

- Measure _⟨Zi⟩_ after each period 

## **Proposed Workflow (2 Steps)** 

- **Step 1: Simulation** 

   - Generate a Haar-random initial state vector (10 qubits = 1024 amplitudes) 

   - Construct the Floquet unitary as a CUDA-Q kernel: 

      - ∗ZZ evolution: Trotterized with CNOT-RZ-CNOT decomposition for each bond 

      - ∗X-kick: Apply RX(2h) = RX(4) gates globally (since kick = exp(-ihX)) 

   - Simulate 10 Floquet periods, recording _⟨Zi⟩_ after each period 

   - Store the 10×10 matrix of local magnetizations 

- **Step 2: Visualization** 

   - Create publication-quality heatmap: 

      - ∗x-axis: qubit index (0-9) 

      - ∗y-axis: Floquet step (0-10, including initial state) 

      - ∗colormap: local magnetization _⟨Zi_ ( _t_ ) _⟩∈_ [ _−_ 1 _,_ 1] 

**Do you want me to proceed with this plan?** (yes / no / modify) If you’d like, I can also: 

- Modify the number of Floquet periods 

- Add entanglement entropy tracking 

- Include uncertainty estimation by averaging over multiple random initial states 

## **User:** Yes 

## **Quantum scientist agent** 

**Action:** Proceeding with the plan. I’ll delegate the simulation task to the CUDA-Q expert. **Tool used:** cudaq expert 

**message2agent** _Omitting for brevity_ 

S24 

## **Cudaq expert agent** 

**Action:** I’ll first search the CUDA-Q manual to understand the correct API for state initialization and state evolution patterns. 

**Tool used:** cudaq deepsearch 

query: cudaq.State.from_data from_state initialize state numpy array get_state state-in state-out 

query: cudaq.observe spin.z single qubit expectation value measurement 

## **Cudaq expert agent** 

**Action:** Now I have the necessary information about CUDA-Q APIs. Let me implement a minimal test version first (4 qubits, 2 periods) to verify the circuit works correctly. 

**Tool used:** submit_python_slurm 

**Code:** _Omitting for brevity_ 

## **Cudaq expert agent** 

**Action:** The minimal test works correctly. Now let me implement the full simulation with 10 qubits, 10 Floquet periods, including the heatmap visualization. 

**Tool used:** submit_python_slurm 

**Code:** _Omitting for brevity_ 

## **Cudaq expert agent** 

**Action:** The Floquet dynamics simulation completed successfully. Delegating to the quantum scientist for analysis. 

**Message2agent:** _Omitting for brevity_ 

## **Quantum scientist agent** 

**Action:** The simulation executed successfully. We observe irregular red–blue patches fluctuating around white, with all magnetization values remaining very small ( _∥⟨Z⟩∥ <_ 0 _._ 09). There is no discernible spatial pattern or temporal ordering. 

## **Physical interpretation.** 

- **Thermalization:** The near-zero magnetization across the entire space–time grid indicates that the system has effectively thermalized to an infinite-temperature state, as expected for chaotic Floquet dynamics. 

- **Scrambling:** The rapid, sign-changing fluctuations reflect strong information scrambling. The large kicks ( _h_ = 2 _J_ ) drive efficient mixing of quantum states and suppress any coherent structure. 

The featureless, noise-like fluctuations around zero confirm that the kicked Ising chain is deep in the chaotic regime, acting as a quantum thermalizer rather than supporting stable or long-lived coherent dynamics. 

S25 

## **S2.9 Time-evolving block decimation (TEBD)** 

## **Prompt** 

Simulate Floquet dynamics with TD-DMRG for a 1D disordered spin-1/2 chain. Use a periodically driven Hamiltonian with period _T_ = _τ_ 1 + _τ_ 2. During 0 _< t < τ_ 1, evolve under a strong global _x_ -field plus interactions and disorder: _H_ =[�] _i_[Ω] _[x][S] i[x]_[+ ∆] _[i][S] i[z]_[+] _[ J]_[(] _[S] i[x][S] i[x]_ +1[+] _[ S] i[y][S] i[y]_ +1 _[−][S] i[z][S] i[z]_ +1[)][.][During] _[τ]_[1] _[< t < T]_[,] switch to a global _y_ -field, _H_ =[�] _i_[Ω] _[y]_[(1] _[ −][ε]_[)] _[S] i[y]_[+ ∆] _[i][S] i[z]_[+] _[ H][i,i]_[+1][.][Choose][Ω] _[x][τ]_[1] _[≈][π]_[so][each][period] approximately flips the _x_ -polarization. Use the following parameters: system size _L_ = 10 spins, maximum bond dimension _χ_ max = 100, time step _δt_ = 0 _._ 03, evolve for _N_ periods = 50 Floquet periods, average over _N_ disorder = 5 disorder realizations, and scan _ε ∈{_ 0 _,_ 0 _._ 15 _,_ 0 _._ 3 _}_ . Keep the Hamiltonian parameters as before: _J_ = 1, Ω _x_ = Ω _y_ = 4 _J_ , _τ_ 1 = _π/_ (2Ω _x_ ) _≈_ 0 _._ 393, _τ_ 2 = 0 _._ 5, and disorder strength _W_ = 2 _J_ . 

Initialize the system in a product state polarized along + _x_ . Evolve stroboscopically for many periods using TD-DMRG (TEBD or TDVP), keeping truncation errors under control. Use disorder ∆ _i ∈_ ( _−W, W_ ) and average over several realizations. After each Floquet period, measure the bulk _x_ -magnetization and plot it versus the number of periods. Vary _ε_ to identify regimes with long-lived period-doubling (subharmonic 2 _T_ oscillations) versus rapid decay due to heating. Track entanglement growth and discuss how it limits the reachable simulation time. 

S26 

## **Quantum scientist agent** 

**Action:** This is a fascinating Floquet Many-Body Localization / Discrete Time Crystal (DTC) simulation! The physics here involves: 

- Period-doubling oscillations: When _ε ≈_ 0, the system shows robust 2T-periodic response (DTC phase) 

- Heating to infinite temperature: For large _ε_ , the drive heats the system and destroys coherent oscillations 

- Disorder-induced stabilization: Strong disorder (MBL) protects the DTC from thermalization 

This task is well-suited for TenPy’s TEBD implementation. Let me propose a structured plan: 

## **Proposed High-Level Plan** 

- **Step 1: Code Generation & Validation** 

   - Generate TenPy code implementing the two-phase Floquet protocol 

   - Use TEBD for time evolution with the specified Hamiltonians 

   - Initialize _|_ + _x⟩_ product state 

   - Implement disorder sampling and stroboscopic measurement 

- **Step 2: Production Simulations (all parallelizable)** 

   - Run simulations for _ε ∈{_ 0 _,_ 0 _._ 15 _,_ 0 _._ 3 _}_ 

   - Average over 5 disorder realizations per _ε_ 

   - Track x-magnetization and entanglement entropy at each period 

   - Monitor truncation errors 

- **Step 3: Analysis & Visualization** 

   - Plot disorder-averaged magnetization vs. Floquet period for each _ε_ 

   - Plot entanglement entropy growth to assess simulation reliability 

   - Identify DTC regime (persistent oscillations) vs. heating regime (decay) 

   - Discuss bond dimension limitations on simulation time 

## **Would you like me to proceed with this plan?** 

Also, would you like me to perform a brief literature search on Floquet MBL/DTC simulations to ensure we follow best practices for this type of calculation? 

## **User:** Yes 

## **Quantum scientist agent** 

**Action:** I’ll proceed with the plan. Let me delegate the code generation to the TenPy expert. 

**Tool used:** tenpy expert 

**Message2agent:** _Omitting for brevity_ 

S27 

## **Tenpy expert agent** 

**Action:** I’ll help you create a TenPy simulation for Floquet dynamics of a disordered spin-1/2 chain (Discrete Time Crystal / Floquet MBL). Let me first search the TenPy manual to ensure I use the correct API for TEBD time evolution. 

**Tool used:** tenpy deepsearch 

query: TEBD time evolution engine spin chain MPS time-dependent Hamiltonian 

query: SpinHalfChain custom model NearestNeighborModel add_onsite add_coupling disorder random field TEBD trunc_params chi_max 

query: MPS from_product_state x direction Sx expectation value entanglement_entropy measurement 

query: TEBDEngine run real time evolution run_evolution dt N_steps real time not imaginary 

## **Tenpy expert agent** 

**Action:** Now I have all the information needed. Let me create a complete TenPy simulation for the Floquet DTC dynamics. I’ll first run a minimal test to verify the code works, then run the full production simulation. 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Tenpy expert agent** 

**Action:** The minimal test works correctly. The code shows expected DTC behavior with oscillating magnetization. Now let me run the full production simulation with all parameters and generate publication-quality plots. 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Tenpy expert agent** 

**Action:** The simulation completed successfully. Now let me save the Python code file as requested: 

**Tool used:** submit_python_slurm 

**code:** _Omitting for brevity_ 

## **Tenpy expert agent** 

**Action:** I have successfully created and executed a complete TenPy simulation for Floquet dynamics of a 1D disordered spin-1/2 chain (Discrete Time Crystal / MBL). 

S28 

## **Quantum scientist agent** 

**Action:** Excellent! The simulation has completed successfully. Let me view the main results to analyze the DTC dynamics. 

## **Figure Observations:** 

- **Panel(a)-Magnetization:** Stroboscopic _⟨S[x] ⟩_ vs Floquet period with clear period-doubling oscillations. The alternating pattern demonstrates discrete-time crystal behavior, with the decay depending on the imperfection _ε_ . 

- **Panel (b) - Entanglement:** Slow logarithmic growth of entanglement entropy _S_ , confirming MBL protection ( _S ≈_ 2 _._ 0 _<<_ 3 _._ 47 thermal limit). Three curves for _ε ∈_ 0 _,_ 0 _._ 15 _,_ 0 _._ 3 with shaded error bands ( _±_ 1 _σ_ from disorder averaging). 

**Key Physics Observations** This simulation provides direct numerical evidence for the MBL-protected discrete time crystal phase: a driven quantum system that spontaneously oscillates at twice the driving period, protected from thermalization by many-body localization. 

## **S2.10 Phase diagrams of quantum systems** 

**Prompt** Use DMRG to prepare the ground state of the one-dimensional transverse field cluster Hamiltonian over a ring of _N_ qubits (interpolate with cos and sin between these cluster Hamiltonian and the magnetic field). Compute the string-order parameter _ZXIX · · · IXZ_ for multiple strengths of the cluster Hamiltonian over 11, 21, and 41 qubits. Plot the string-order parameter as a function of the cluster Hamiltonian strength for the different system sizes and estimate the critical point. 

S29 

## **Quantum scientist agent** 

**Action:** This is a tensor network simulation task for studying a symmetry-protected topological (SPT) phase transition. Let me outline my understanding and propose a plan. 

## **Problem Understanding** 

- **Hamiltonian:** The transverse field cluster model on a ring: 

**==> picture [198 x 23] intentionally omitted <==**

   - At _θ_ = 0: paramagnetic phase (trivial) 

   - At _θ_ = _π/_ 2: cluster Hamiltonian (SPT phase) 

- **String Order Parameter:** _⟨Z_ 1 _X_ 2 _I_ 3 _X_ 4 _I_ 5 _· · · XN −_ 1 _ZN ⟩_ — this detects the hidden topological order characteristic of the cluster state phase. 

- **Goal:** Map out the phase transition by computing string order vs. _θ_ for N = 11, 21, 41. 

## **Proposed High-Level Plan** 

- **Step 1: DMRG Ground State Calculations + String Order Computation** 

- For each system size (N = 11, 21, 41) and for multiple values of _θ ∈_ [0 _, π/_ 2] (e.g., 20-30 points): 

   - Construct the transverse field cluster Hamiltonian on a ring 

   - Run DMRG to obtain the ground state 

   - Compute the string order parameter _⟨ZXIX · · · IXZ⟩_ 

- **Step 2: Analysis and Visualization** 

   - Plot string order parameter vs. _θ_ for all three system sizes on the same figure 

   - Estimate the critical point from the crossing/transition behavior 

   - Apply finite-size scaling if needed 

## **Key Considerations** 

- Periodic boundary conditions (ring geometry) require careful handling in DMRG — may need to use infinite DMRG or handle the long-range bond appropriately 

- Bond dimension must be sufficient to capture entanglement near criticality 

- String order computation requires measuring a product of non-local operators 

## **Would you like me to proceed with this plan?** 

Also, would you like me to perform a literature search first to: 

- Confirm the known critical point for benchmarking 

- Verify the exact form of the string order parameter used in the literature 

**User:** Yes 

S30 

## **Quantum scientist agent** 

**Action:** I’ll proceed with the plan. Let me first do a quick literature/documentation search to ensure we implement this correctly, then delegate to the TenPy expert. 

**Tool used:** tenpy deepsearch 

query: string order parameter correlation function DMRG cluster state SPT 

query: three-body interaction ZXZ cluster Hamiltonian custom model periodic boundary conditions ring 

## **Quantum scientist agent** 

**Action:** Excellent! I have the necessary information. Let me summarize the key findings: 

## **Literature/Documentation Findings:** 

- Three-body cluster term: Use add_multi_coupling() with (’Sigmaz’, 0, 0), (’Sigmax’, 1, 0), (’Sigmaz’, 2, 0) 

- Periodic boundary conditions: Set bc_x=’periodic’ (note: MPS stays open but couplings wrap around) 

- String order parameter: Use psi.correlation_function() with opstr argument for inserting operators between endpoints 

- Conservation: Must use conserve=’None’ since X terms break Sz conservation 

Now I’ll delegate to the TenPy expert to implement this calculation. 

**Tool used:** tenpy expert 

**Message2agent:** _Omitting for brevity_ 

## **Tenpy expert agent** 

**Action:** I’ll help you implement the DMRG study of the transverse field cluster model. Let me first search the tenpy manual to ensure I use the correct API for tenpy 1.11.2. 

**Tool used:** tenpy deepsearch 

query: CouplingMPOModel add_multi_coupling three-body term periodic boundary conditions 

query: expectation_value_multi_sites string order parameter MPS 

query: SpinHalfSite Sigmax Sigmaz Pauli operators conserve None 

## **Tenpy expert agent** 

**Action:** Now I have all the information I need. Let me first create a minimal debug version to test the implementation: 

**Tool used:** submit_python_slurm 

**Code:** _Omitting for brevity_ 

S31 

## **Tenpy expert agent** 

**Action:** The debug test works correctly. The string order parameter shows the expected behavior: 

   - _θ_ = 0 (trivial phase): string order _≈_ 0 

   - _θ_ = _π/_ 2 (SPT cluster phase): string order = _−_ 1 _._ 0 (fully ordered) 

- **Tool used:** submit_python_slurm 

**Code:** _Omitting for brevity_ 

## **Tenpy expert agent** 

**Action:** The simulation completed successfully. The data shows a clear phase transition in the string order parameter. Now let me delegate the visualization and critical point analysis to the quantum scientist. 

**Message2agent:** _Omitting for brevity_ 

## **Quantum scientist agent** 

**Action:** Analysis Complete. I have created publication-quality plots and analyzed the DMRG results for the transverse field cluster model. 

I implemented DMRG simulations (tolerance 10 _[−]_[5] ) for the transverse field cluster Hamiltonian: 

- **Model:** _H_ ( _θ_ ) = _−_ cos( _θ_ )[�] _i[Z][i][−]_[1] _[X][i][Z][i]_[+1] _[ −]_[sin][(] _[θ]_[)][ �] _i[X][i]_[where] _[θ]_[interpolates][between][the][cluster] symmetry-protected topological (SPT) phase ( _θ_ = 0) and trivial paramagnetic phase ( _θ_ = _π/_ 2). 

## **Physical Interpretation:** 

- SPT Phase ( _θ < θc_ ): String order _O ≈_ 1, indicating symmetry-protected topological order 

- Trivial Phase ( _θ > θc_ ): String order _θ →_ 0, no topological order 

- Critical Point: _θc/π ≈_ 0 _._ 236 (extrapolated), close to theoretical _π/_ 4 = 0 _._ 25 

- The transition sharpens with increasing system size, consistent with a quantum phase transition. 

## **S2.11 Bell-state correlations under depolarizing noise** 

**Prompt** Read the Qiskit manual and prepare the Bell state ( _|_ 00 _⟩_ + _|_ 11 _⟩_ ) _/√_ 2. Start in _|_ 00 _⟩_ , apply a Hadamard gate on qubit 0, and then a CNOT with control qubit 0 and target qubit 1. Add a depolarizing noise channel with probability _p_ to both qubits. Simulate the circuit for _p ∈{_ 0 _,_ 0 _._ 05 _,_ 0 _._ 1 _,_ 0 _._ 2 _,_ 0 _._ 3 _}_ . For each value of _p_ , run 4096 shots in the _Z_ basis, return the measurement counts, and compute _⟨Z ⊗ Z⟩_ . Then insert Hadamard gates on both qubits to measure in the _X_ basis, run 4096 shots, return the measurement counts, and compute _⟨X ⊗ X⟩_ . Plot both correlators as functions of _p_ and comment on how the noise degrades the Bell-state correlations. 

S32 

## **Quantum scientist agent** 

**Action:** I’ll help you prepare a Bell state with depolarizing noise in Qiskit. Let me first search the Qiskit manual to understand how to implement noise channels and measurements. 

**Tool used:** qiskit deepsearch 

query: depolarizing noise channel circuit simulation shots measurement 

query: NoiseModel depolarizing channel probability create add noise gates 

query: ExpectationValue Paulistring Z measurement counts bitstring sampling 

query: Qiskit noise BitFlip DepolarizingError NoiseModel constructor example 

## **Quantum scientist agent** 

**Action:** Based on my search of the qiskit manual, I now have a good understanding of how to implement this task. 

## **Proposed High-Level Plan** 

- **Step 1: Build and simulate Bell state circuit with depolarizing noise** 

   - Create Bell state circuit: H(0) + CNOT(0,1) 

   - For each _p ∈{_ 0 _,_ 0 _._ 05 _,_ 0 _._ 1 _,_ 0 _._ 2 _,_ 0 _._ 3 _}_ : 

      - ∗Apply depolarizing noise (level=2 for after CNOT) to both qubits 

      - ∗Z-basis: Simulate with 4096 shots, collect counts, compute _⟨Z ⊗ Z⟩_ 

      - ∗ X-basis: Add H gates on both qubits, simulate with 4096 shots, collect counts, compute _⟨X ⊗ X⟩_ 

- **Step 2: Plot and analyze results** 

   - Plot _⟨Z ⊗ Z⟩_ and _⟨X ⊗ X⟩_ vs _p_ . 

   - Comment on how noise degrades Bell-state correlations 

**Should I proceed with this plan?** (yes / no / modify) 

**User:** Yes 

## **Quantum scientist agent** 

**Action:** I’ll delegate to the qiskit expert to implement the noisy Bell state simulation. 

**Tool used:** qiskit expert. 

**Message2agent:** _Omitting for brevity_ 

S33 

## **Qiskit expert agent** 

**Action:** Let me first search the Qiskit manual to understand the correct syntax for noise models and measurements. 

**Tool used:** qiskit deepsearch 

query: depolarizing noise channel simulation measurement samples shots 

query: NoiseModel depolarizing add_noise circuit gates qiskit create noise model 

query: qiskit circuit noise BitFlip DepolarizingError create noise probability qubit 

query: qiskit gates H Hadamard CNOT X controlled gate circuit construction 

## **Qiskit expert agent** 

**Action:** Now I have enough information to create the simulation. Let me write a comprehensive Python script that handles all the requirements 

**Tool used:** submit_python_slurm 

**Code:** _Omitting for brevity_ 

## **Qiskit expert agent** 

**Action:** I see the issue - there’s a qiskit version compatibility problem (qiskit 2.2.3 has breaking changes). Let me implement a solution using Qiskit Aer directly for proper noisy simulation: 

**Tool used:** submit_python_slurm 

**Code:** _Omitting for brevity_ 

## **Qiskit expert agent** 

**Action:** Excellent! The simulation worked perfectly! The results show clear noise degradation. Now let me delegate the plotting to the quantum scientist: 

**Tool used:** submit_python_slurm 

**Code:** _Omitting for brevity_ 

## **Quantum scientist agent** 

**Action:** The simulation executed successfully. I prepared a Bell state simulation with depolarizing noise and analyzed the degradation of quantum correlations. Here are the key results: 

- Ideal Bell state produces only correlated outcomes ( _|_ 00 _⟩_ , _|_ 00 _⟩_ ) 

- Depolarizing noise introduces anti-correlated outcomes ( _|_ 01 _⟩_ , _|_ 10 _⟩_ ) 

- High noise limit: Distribution approaches uniform (maximally mixed state) 

- X-basis degradation is 2-3x faster due to additional Hadamard gates also experiencing noise. 

This demonstrates why the choice of measurement basis matters in noisy quantum systems. More gates equal more accumulated errors. 

S34 

## **Quantum scientist agent** 

**Action:** I’ll proceed with Step 1 - constructing the Hamiltonian and preparing for resource estimation. Let me delegate this to the PennyLane expert. 

**Tool used:** pennylane expert. 

**Message2agent:** _Omitting for brevity_ 

## **S2.12 Estimating qubit requirements for quantum simulation** 

**Prompt** Read the PennyLane manual and construct the second-quantized electronic Hamiltonian of water in the STO-3G basis. Use the Jordan-Wigner transformation to map the Hamiltonian to a qubit representation. Then build a logical (non–fault-tolerant) quantum phase estimation (QPE) circuit that would estimate the ground-state energy of water within chemical accuracy, and use PennyLane’s resource-estimation tools to approximate: (1) the number of logical qubits required and (2) the number of non-Clifford (e.g., _T_ ) gates arising from the Hamiltonian-simulation segments of the QPE routine. Report and discuss these logical-level resource estimates. 

## **Quantum scientist agent** 

**Action:** I’ll analyze this task and develop a high-level plan. This involves quantum chemistry Hamiltonian construction and quantum resource estimation using PennyLane. Let me first search the PennyLane manual to understand the available tools for molecular Hamiltonians, QPE, and resource estimation. 

**Tool used:** pennylane deepsearch 

query: molecular Hamiltonian second quantized Jordan Wigner transformation water H2O STO-3G basis 

query: quantum phase estimation QPE resource estimation T gates non-Clifford gates logical qubits 

query: DoubleFactorization error chemical accuracy precision target_error one_body two_body electron integrals 

S35 

## **Quantum scientist agent** 

**Action:** Excellent! I now have comprehensive information to formulate a plan. Based on my search of the PennyLane documentation, here’s my analysis: 

## **Task Analysis** 

- **Objective:** Estimate logical-level QPE resources for the water molecule (H2O) in STO-3G basis using PennyLane. 

- **Key technical aspects:** 

   - **H** 2 **O in STO-3G:** 10 electrons, 7 spatial orbitals _→_ 14 spin-orbitals _→_ 14 qubits under JordanWigner 

   - **Chemical accuracy:** 0.0016 Hartree ( _∼_ 1 kcal/mol), which is PennyLane’s default for resource estimation 

   - **Resource estimation approach:** PennyLane provides qml.resource.DoubleFactorization which estimates Toffoli gates and logical qubits for QPE using the double-factorized Hamiltonian representation (state-of-the-art for second-quantized molecular simulation) 

   - **T-gate conversion:** Each Toffoli gate decomposes into _∼_ 7 T gates (standard Clifford+T decomposition) 

## **Proposed High-Level Plan** 

- **Step 1** 

   - Construct H2O molecule in STO-3G basis 

   - Generate second-quantized fermionic Hamiltonian 

   - Apply Jordan-Wigner transformation _→_ qubit Hamiltonian 

   - Extract one- and two-electron integrals for resource estimation 

## • **Step 2** 

- Use qml.resource.DoubleFactorization with error=0.0016 (chemical accuracy) to estimate logical qubits and Toffoli gates 

- Convert Toffoli count to approximate T-gate count 

- Report and discuss results (qubit count, gate cost, implications for near-term/fault-tolerant hardware) 

**Would you like me to proceed with this plan?** Also, do you want me to perform a brief literature search on QPE resource estimation methodologies before execution, or shall I proceed directly with the PennyLane implementation? 

## **Pennylane expert agent** 

**Action:** Let me first search the PennyLane manual to understand the correct API for molecular Hamiltonians, QPE, and resource estimation tools. 

**Tool used:** pennylane deepsearch 

query: molecular Hamiltonian water qchem Jordan-Wigner second quantization STO-3G basis 

query: quantum phase estimation QPE circuit resource estimation logical qubits T gates non-Clifford 

query: DoubleFactorization electron_integrals QPE gate cost qubit cost Hamiltonian simulation Toffoli 

S36 

## **Pennylane expert agent** 

**Action:** Now I have comprehensive information. Let me search for more details about inspecting the Hamiltonian and any additional resource estimation details. 

**Tool used:** pennylane deepsearch 

> query: Hamiltonian coefficients terms pauli words print inspect number terms Jordan Wigner fermionic 

## **Pennylane expert agent** 

**Action:** Excellent! I now have all the information needed. Let me create a comprehensive script that: 

   - Constructs water’s molecular Hamiltonian in STO-3G basis with Jordan-Wigner mapping 

   - Analyzes the Hamiltonian structure 

- Uses DoubleFactorization for QPE resource estimation (logical qubits and non-Clifford gates) 

- **Tool used:** submit_python_slurm 

**Code:** _Omitting for brevity_ 

## **Pennylane expert agent** 

**Action:** Let me fix the electron integrals handling and re-run the script: 

**Tool used:** submit_python_slurm 

**Code:** _Omitting for brevity_ 

## **Pennylane expert agent** 

**Action:** Excellent! The simulation completed successfully. Let me now delegate the visualization and detailed interpretation to the quantum scientist. 

**Message2agent** _Omitting for brevity_ 

## **Quantum scientist agent** 

**Action:** Excellent! Task Complete: Water QPE Resource Estimation 

## **Summary Report** 

I have successfully constructed the second-quantized electronic Hamiltonian of water (H2O) in STO-3G basis, applied the Jordan-Wigner transformation, and estimated the logical-level resources for quantum phase estimation (QPE). 

## **Figure Content:** 

- **(a) Left panel, qubit breakdown.** 14 system (4.8%) vs 276 ancilla (95.2%) = 290 total. 

- **(b) Right panel, required Toffoli gates.** Toffoli gates vs error (log-scale), showing _O_ (1 _/ϵ_ ) scaling with chemical accuracy marked in green. 

The resource estimates demonstrate that even for a small molecule like water, fault-tolerant QPE requires significant quantum resources, highlighting the importance of algorithmic optimizations (double factorization) and the path toward utility-scale quantum chemistry. 

**Key takeaway:** For water QPE at chemical accuracy _→_ 290 logical qubits and _∼_ 112M Toffoli gates ( _∼_ 447M T-gates). 

S37 

## **S2.13 Quantum Error Correction** 

**Prompt** Implement and run a surface-code logical memory experiment in the Z basis with the Stim. Use the following parameters: 

**Distances:** d = 3, 5, 7. **Rounds:** R = d stabilizer-measurement rounds. **Shots:** N = 3000000 per distance **State:** prepare logical _|_ 0 _L⟩_ (Z-basis memory). **Noise:** apply two-qubit depolarizing noise with probability p = 0.003 on every CX (CNOT) gate only. **Sampling:** for each shot, sample Stim detector events and final data-qubit Z measurements. **Logical observable:** compute measured _ZL_ as the parity of the final data-qubit Z outcomes along the chosen logical _ZL_ string. **Decoding:** build the Stim-generated detector error model (DEM) and decode using PyMatching (MWPM). **Plots:** report a single plot of d vs logic error gate for the data with and without the decoder, and add theoretical estimation. 

## **Quantum scientist agent** 

**Action:** This is a quantum error correction (QEC) task involving surface code simulation with CUDA-Q QEC and the Stim backend. Let me first search the CUDA-Q documentation to understand the QEC capabilities and Stim integration before proposing a plan. 

**Tool used:** cudaq deepsearch 

query: CUDA-Q QEC surface code Stim backend quantum error correction logical memory experiment 

query: PyMatching decoder MWPM Stim detector error model two-qubit depolarizing noise CNOT gate 

## **Quantum scientist agent** 

**Action:** Based on my searches, I have a comprehensive understanding of the task. 

## **Proposed High-Level Plan** 

## • **Step 1** 

- builds rotated surface code memory circuits for d=3,5,7 with R=d rounds 

- applies DEPOLARIZE p=0.003 only on CX gates 

- samples 3M shots per distance 

- decodes with PyMatching 

- computes raw vs decoded logical error rates 

## • **Step 2:** 

- Execute code 

- Collect results 

- produce publication-quality plot: d vs logical error rate (raw, decoded, theoretical) 

## **Should I proceed with this plan?** 

## **User:** Yes 

## **Quantum scientist agent** 

**Action:** I’ll proceed with the plan. Let me delegate to the CUDA-Q expert to implement the surface code memory experiment using Stim + PyMatching. 

**Tool used:** cudaq expert 

**Message2agent:** _Omitting for brevity_ 

S38 

## **Cudaq expert agent** 

**Action:** Let me implement the surface-code logical memory experiment with: 

   - Stim for circuit generation and sampling 

   - PyMatching for MWPM decoding 

   - Two-qubit depolarizing noise on CNOT gates only 

- **Tool used:** submit_python_slurm 

**Code:** _Omitting for brevity_ 

## **Cudaq expert agent** 

**Action:** The simulation completed successfully with excellent results. Now let me delegate the visualization to the quantum scientist expert to create the requested plot. 

**Message2agent:** _Omitting for brevity_ 

## **Quantum scientist agent** 

**Action:** Task completed. Publication-quality plot created successfully for the surface code logical memory experiment. 

## **Plot Overview** 

The plot displays logical error rate vs. code distance for a Z-basis surface code memory experiment with three curves: 

- Red(raw): Error rate without decoder. Increases with distance 

- Blue (decoder): Error rate with MWPM decoder. Decreases with distance 

- Green (Theory): Threshold model: _pL ∼ A_ ( _p/pth_ )[(] _[d]_[+1)] _[/]_[2] . Decreases with distance 

## **Physical Interpretation** 

- **Why Raw Error INCREASES with Distance** 

   - More physical qubits _→_ more CNOT gates _→_ more noise opportunities 

   - Without correction, errors simply accumulate: _praw ∝_ (number of CNOTs) _× p_ 

   - Scales roughly as _∼ d_[2] _· d_ = _d_[3] (qubits × rounds) 

- **Why Decoded Error DECREASES with Distance** 

   - Surface code can correct up to _⌊_ ( _d −_ 1) _/_ 2 _⌋_ errors 

   - Below threshold, probability of _≥ d/_ 2 correlated errors is exponentially small 

   - **Exponential suppression:** _pL ∼_ ( _p/pth_ )[(] _[d]_[+1)] _[/]_[2] 

- **Below-Threshold Regime** 

   - Physical error: _p_ = 0 _._ 003 

   - Threshold: _pth ≈_ 0 _._ 01 (for depolarizing noise on surface code) 

   - Ratio: _p/pth_ = 0 _._ 3 — **well below threshold** 

   - This is the regime where QEC provides exponential benefit 

The plot demonstrates the central promise of quantum error correction: below the threshold, increasing code distance exponentially suppresses logical errors despite linearly increasing physical resources. At _p_ = 0 _._ 003, the surface code is firmly in the fault-tolerant regime. 

S39 

## **S3 Evaluation Rubrics** 

The benchmark task was graded on a 100-point scale using three fixed criteria. The benchmark covers five representative quantum-simulation problems: variational quantum eigensolver (VQE), Bell-state preparation, transverse-field Ising dynamics, open-system Lindblad dynamics, and hierarchical equations of motion (HEOM). Criterion A (30 points) evaluates the correctness of the technical implementation, including proper construction of the model and correct use of the target software framework. Criterion B (30 points) assesses the correctness and validation of the computed results, including appropriate observables, numerical consistency, and comparisons where required. In turn, criterion C (40 points) evaluates the clarity and quality of the final outputs, including figures, analysis, and physical interpretation. For each criterion, Tables S2–S6 provide explicit point assignments that define full, partial, and zero credit. 

**Table S2** Grading rubric for the VQE benchmark (H2). 

|**Criterion**|**Points**|**Description**|
|---|---|---|
|A|30|Correct Hamiltonian, ansatz, optimizer, and bond-distance sweep.|
||20|Minor setup issues but VQE runs correctly.|
||10|Incomplete or poorly confgured VQE.|
||0|No working VQE.|
|B|30|Exact reference included and correctly compared.|
||20|Comparison shown but weakly justifed.|
||10|Partial or unclear comparison.|
||0|No comparison to exact result.|
|C|40|Clear dissociation curve with correct physical interpretation.|
||30|Correct plot with limited physical insight.|
||20|Plot present but interpretation weak.|
||0–10|Missing or incorrect plot.|



S40 

**Table S3** Grading rubric for the Bell-state preparation benchmark. 

|**Criterion**|**Points**|**Description**|
|---|---|---|
|A|30|Correct Bell-state circuit, measurement bases, and shot count.|
||20|Minor circuit or basis issues with correct intent.|
||10|Circuit mostly correct but measurements fawed.|
||0|Incorrect circuit or missing measurements.|
|B|30|Correct computation of _⟨Z⊗Z⟩_and _⟨X⊗X⟩_.|
||20|Correct method with numerical or normalization errors.|
||10|Partial or unclear computation.|
||0|Observables not computed.|
|C|40|Clear plots with correct interpretation.|
||30|Correct plots with superfcial analysis.|
||20|Poorly explained or hard-to-read plots.|
||0–10|No meaningful plot or analysis.|



**Table S4** Grading rubric for the transverse-field Ising dynamics benchmark. 

|**Criterion**|**Points**|**Description**|
|---|---|---|
|A|30|Correct Hamiltonian, evolution method, parameters, and initialization.|
||20|Minor errors with sensible dynamics.|
||10|Signifcant issues in implementation.|
||0|Incorrect time evolution.|
|B|30|Correct extraction of _⟨Z⟩_for all qubits.|
||20|Partial or noisy measurements.|
||10|Incorrect observable handling.|
||0|No meaningful measurement.|
|C|40|Clear heatmaps with insightful regime comparison.|
||30|Correct heatmaps with brief analysis.|
||20|Poor visualization.|
||0–10|Missing or unreadable plots.|



S41 

**Table S5** Grading rubric for the Lindblad dynamics benchmark. 

|**Criterion**|**Points**|**Description**|
|---|---|---|
|A|30|Correct Hamiltonian, collapse operators, and solver confguration.|
||20|Minor implementation issues.|
||10|Incomplete setup.|
||0|Incorrect dynamics.|
|B|30|Correct _⟨Z_(_t_)_⟩_for both initial states.|
||20|Partial or noisy results.|
||10|Incorrect observables.|
||0|Missing data.|
|C|40|Clear comparison with correct physical explanation.|
||30|Mostly correct explanation.|
||20|Limited insight.|
||0–10|No meaningful discussion.|



**Table S6** Grading rubric for the HEOM benchmark. 

|**Criterion**|**Points**|**Description**|
|---|---|---|
|A|30|Correct Hamiltonian, bath parameters, hierarchy, and time grid.|
||20|Minor setup or parameter issues.|
||10|Incomplete setup.|
||0|Incorrect formulation.|
|B|30|Stable propagation with physically consistent populations.|
||20|Partial or weak validation.|
||10|Unclear or poorly validated dynamics.|
||0|No validation or unstable evolution.|
|C|40|Clear population plots at both temperatures with correct physical interpretation.|
||30|Correct results with limited clarity or depth.|
||20|Poor visualization or weak interpretation.|
||0–10|Missing or incorrect outputs.|



S42 

