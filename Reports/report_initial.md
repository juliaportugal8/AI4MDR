

# Initial Literature Review

## 1. Introduction

his report documents the initial phase of theoretical and regulatory study undertaken within the scope of the AI4MDR project. Its purpose is to consolidate and critically structure the main regulatory, normative, and engineering concepts identified in the literature reviewed during this stage.

Beyond summarising standards and regulations, this review clarifies the systemic interdependencies between regulatory qualification, lifecycle governance, safety classification, risk management obligations, documentation requirements, and engineering practices. In the medical device domain, compliance is not achieved through isolated technical artefacts but through demonstrable process integrity across the entire lifecycle.


## 2. Regulatory Qualification of Medical Device Software
### 2.1 Legal Definition under MDR
The regulatory qualification of software constitutes the first essential step before applying any lifecycle or safety standard. In the European Union, the determination of whether software qualifies as a Medical Device Software (MDSW) is governed by Regulation (EU) 2017/745 (MDR), Regulation (EU) 2017/746 (IVDR), and further clarified by MDCG 2019-11 guidance.

According to Article 2(1) MDR, a medical device is any instrument, apparatus, appliance, software, implant, reagent, material or other article intended by the manufacturer to be used for specific medical purposes, including diagnosis, prevention, monitoring, prediction, prognosis, treatment or alleviation of disease. 
A fundamental interpretative principle is that qualification depends primarily on the intended purpose defined by the manufacturer. Software does not become a medical device merely because it operates in a healthcare environment; it qualifies only if its intended purpose falls within the medical objectives defined in the Regulation.
Additionally, Recital 19 MDR explicitly clarifies that software specifically intended for medical purposes qualifies as a medical device, whereas software for general purposes, even when used in healthcare settings, does not.

### 2.2 MDCG 2019-11 Decision Framework
Further clarification is provided by the MDCG guidance document “Is your software a Medical Device?” (MDCG 2019-11).
The guidance establishes a structured decision framework based on three cumulative criteria:

Software Qualification
The product must qualify as software according to MDCG 2019-11 and perform actions beyond mere storage, archival, communication, or simple search.

Medical Data Processing
The software must generate, transform, analyse, or interpret medical data. Software that merely stores or transmits data does not qualify as MDSW.

Medical Purpose for Individual Patients
The intended benefit must relate to specific medical objectives for individual patients. Administrative, lifestyle, or general well-being applications fall outside MDR scope.
If these criteria are satisfied, the software qualifies as Medical Device Software (MDSW) and falls under MDR or IVDR, depending on whether it relates to general medical devices or in vitro diagnostic applications.

### 2.3 Borderline Cases and Regulatory Delimitation

MDR emphasises that borderline qualification decisions may arise when software interfaces with medicinal products, in vitro diagnostics, or non-medical functionalities.

The Regulation also establishes that:

- Devices combining medicinal products and software must be assessed based on the principal mode of action.

- Software driving or influencing a medical device inherits regulatory relevance.

- Devices without a medical intended purpose but similar risk profiles (Annex XVI) may also fall under MDR through Common Specifications.

This regulatory delimitation ensures legal clarity while preventing unjustified expansion of scope.

### 2.4 Transitional Provision and Legacy Devices
Article 120 MDR establishes transitional provisions for so-called “legacy devices”, meaning devices previously certified under the MDD or AIMDD frameworks.

The transitional regime defines strict conditions under which such devices may continue to be placed on the market. Key requirements include:

- Continued compliance with previous directives.

- Absence of significant changes in intended purpose or design.

- Implementation of an MDR-compliant Quality Management System (Article 10(9)).

- Timely application for conformity assessment under MDR.

- Formal agreement with a Notified Body within defined deadlines.

The extended transitional deadlines (up to 2027 or 2028 depending on classification) are conditional and subject to explicit regulatory criteria.

This transitional structure demonstrates that regulatory compliance is not static but lifecycle-dependent, reinforcing the importance of continuous conformity.              

## 3. Regulatory and Process Foundations for Medical Device Software

### 3.1 Lifecycle-Oriented Regulatory Framework

Medical device software operates within a highly regulated environment in which safety and effectiveness must be demonstrated through structured and documented processes.
 IEC 62304 establishes a lifecycle-based framework defining processes, activities, and tasks required for the development and maintenance of medical device software (IEC 62304:2006).

The standard is built on the premise that software safety cannot be assured solely through final testing. Instead, safety must emerge from controlled lifecycle processes covering planning, requirements definition, architecture, implementation, verification, release, maintenance, configuration management, and problem resolution.

Development is presumed to occur within a Quality Management System (QMS) and in coordination with a Risk Management System, typically aligned with ISO 14971. This integration highlights that software development is embedded within a broader regulatory and quality ecosystem rather than functioning as an isolated engineering activity.

### 3.2 Software Safety Classification and Risk Assumptions

A core structural element of the standard is software safety classification. Software is categorised according to the potential consequences of failure on patients, operators, or other users:

- Class A – no possible injury or damage to health  
- Class B – no possible serious injury  
- Class C – possible death or serious injury  

Classification directly determines the level of process rigor required throughout development (IEC 62304:2006).

A critical principle states that when a hazard may arise from software malfunction, the probability of failure must be assumed to be 100%. This prevents unjustified reduction of risk assumptions based solely on presumed reliability.

The assigned safety class must be documented within the Risk Management File and may only be reduced if risk is demonstrably mitigated (e.g., through hardware risk control measures), with appropriate justification.

### 3.3 Traceability and Documentation Requirements

Traceability constitutes one of the central structural pillars of medical device software compliance. It ensures that every implemented software element can be linked back to a defined requirement and, where applicable, to an identified risk control measure. This bidirectional linkage allows reconstruction of the logical chain from hazard identification to implementation and verification.

In regulated environments, traceability serves multiple purposes. It supports auditability during conformity assessment, enables impact analysis when changes occur, and facilitates investigation of post-market incidents. Without structured traceability, it becomes impossible to demonstrate that identified risks have been systematically addressed.

Documentation requirements are therefore not bureaucratic formalities but structural safety mechanisms. Requirements must be uniquely identifiable, consistent, verifiable, and linked to corresponding test evidence. Architectural components must be connected to the requirements they fulfil. Verification results must demonstrate correct implementation. When lifecycle tasks are considered “not applicable” or implemented “as appropriate,” formal justification is mandatory. Regulatory flexibility does not imply discretionary omission; it requires reasoned justification.

Traceability thus functions as both a compliance instrument and an engineering discipline, reinforcing coherence between specification, implementation, and verification.

### 3.4 Maintenance, Change Control and Post-Market Governance

Unlike in conventional software engineering contexts, maintenance in medical device software is a formally regulated lifecycle process. Once software is released, the manufacturer remains responsible for monitoring its behaviour, evaluating field feedback, and assessing potential safety implications of observed anomalies.

Any modification must follow structured change control procedures. This includes impact analysis on safety and performance, evaluation of whether the modification affects safety classification, re-verification of affected components, and appropriate updates to documentation and risk management records. Historical configurations must remain recoverable to ensure reproducibility and auditability.

Problem resolution processes require formal recording of detected defects, systematic root cause analysis, and verification that corrective actions do not introduce new hazards. Where safety is impacted, updates to the Risk Management File are required. This ensures that safety governance continues throughout the operational lifecycle rather than being confined to initial market placement.

The regulatory treatment of maintenance illustrates a broader principle: compliance is continuous, not event-based. Market placement does not conclude regulatory responsibility; instead, it marks the transition to ongoing post-market surveillance and lifecycle control.

### 3.5 Systemic Integration within the Regulatory Architecture 

IEC 62304 operates within a network of harmonised standards and regulatory instruments. Its lifecycle requirements are closely interlinked with ISO 13485, which governs organisational quality management, and ISO 14971, which governs systematic risk management. These standards collectively support conformity with Regulation (EU) 2017/745 (MDR).

This integration demonstrates that medical device software compliance is inherently multi-layered. Legal conformity under MDR establishes overarching obligations. Process conformity under IEC 62304 structures development activities. Risk governance under ISO 14971 ensures systematic hazard control. Organisational governance under ISO 13485 ensures that responsibilities, documentation, and quality oversight are institutionally embedded.

Medical device software development must therefore be understood as part of a cohesive compliance architecture rather than as a standalone technical activity. Safety, quality, and regulatory conformity are structurally intertwined across the entire lifecycle.

## 4. Software Engineering – A Quantitative Approach  

The regulatory framework presented in the previous chapter defines *what* must be ensured in medical device software development. However, it does not fully describe *how* engineering practices should be structured to achieve quality in a measurable and sustainable manner.  

The book *Software Engineering – A Quantitative Approach* provides a structured workflow that frames software development as an engineering discipline grounded in measurable quality, controlled processes, and continuous feedback. Rather than treating development as a purely creative activity, it positions it as a systematic process driven by explicit requirements, architectural decisions, automation, and empirical metrics.

This section summarises the key engineering principles most relevant to regulated medical software contexts.


### 4.1 Requirements as the Primary Quality Driver  

The book emphasises that requirements determine the fate of a software project. They drive development, define architecture, influence planning, and ultimately serve as the criteria for evaluating product quality. 

A structured requirements process includes:

- Understanding and formalising the problem.
- Surveying existing solutions.
- Eliciting requirements from stakeholders.
- Documenting functional and non-functional requirements.
- Converting problem-domain requirements into solution-domain specifications.
- Validating them through acceptance testing.

The critical insight is that requirements lie at the intersection between the problem domain and the solution domain. Poorly defined requirements propagate ambiguity into architecture and implementation.

The book also highlights the growing role of LLMs in supporting requirement specification and validation, particularly for checking consistency, unambiguity, and structural correctness. However, it cautions that LLMs cannot replace disciplined engineering judgment.

This emphasis on requirement clarity aligns directly with regulatory traceability expectations under IEC 62304.


### 4.2 Architecture Driven by Quality Attributes  

Software architecture is described as the high-level structural blueprint of a system. Its importance lies not only in organizing code but in enabling emergent system properties.

The book distinguishes three main requirement categories at system level:

- Functional requirements;
- Quality attributes;
- Constraints.

Quality attributes such as availability, maintainability, usability, performance, and security are not properties of isolated code fragments but emergent properties of the system architecture.  

For example, high availability cannot be attributed to a specific function; it results from architectural strategies such as redundancy, failover mechanisms, and load balancing.

Architecturally Significant Requirements (ASRs) are those functional requirements that have broad structural implications. These must be identified early, as they heavily constrain architectural design.

This architectural perspective is especially relevant in safety-critical systems, where quality attributes are often regulatory obligations rather than optional enhancements.


### 4.3 Construction, Testing, and the V-Model  

The book structures development around the V-model, where the left side focuses on specification and design, and the right side on verification and validation.

Construction is described as the pivot stage: it transforms architectural design into executable code while embedding quality assurance practices such as Test-Driven Development (TDD).

Testing is not treated as a final activity but as a continuous practice across multiple levels:

- Unit testing (code-level verification)
- Integration testing (component interaction)
- System testing (end-to-end validation)
- Acceptance testing (validation of client requirements)

Functional system tests are extracted directly from product requirements and executed in environments that mimic real-world usage conditions.

The book also highlights the synergy between Behaviour-Driven Development (BDD) and TDD, linking requirements to executable tests. This reinforces the feedback loop between specification and implementation.

In regulated environments, this structured testing hierarchy naturally supports traceability and verification evidence generation.



### 4.4 Automation and Continuous Integration  

Automation is presented as a core enabling practice to increase productivity, consistency, and defect detection.

Rather than manually executing repetitive tasks, automation scripts orchestrate:

- Test execution  
- Static code analysis  
- Security checks  
- Complexity measurement  
- Deployment  

Continuous Integration (CI) pipelines embed these automated checks into every commit. This increases the probability of detecting defects immediately after introduction.

Automation extends beyond testing to Infrastructure as Code (IaC), enabling reproducible environments and controlled deployments.

From a quantitative perspective, automation transforms quality assurance into a measurable and repeatable process rather than a subjective evaluation.


### 4.5 DevOps and Quantitative Metrics  

The DevOps philosophy closes the development loop by incorporating monitoring and feedback from production environments.

Mature DevOps teams adopt measurable performance indicators, notably the DORA metrics:

- Deployment Frequency (DF)
- Lead Time for Changes (LT)
- Change Failure Rate (CFR)
- Mean Time to Restore (MTTR)

These metrics quantify delivery performance, stability, and resilience.

The quantitative approach emphasises that quality cannot be assumed; it must be measured. Metrics enable objective reflection on process performance and continuous improvement.



### 4.6 Roles, Accountability, and Quality Governance  

Engineering discipline is also organisational. The book defines explicit roles such as Product Quality Manager, Tester, and Developer, each with defined responsibilities for quality assurance and defect management.

Clear accountability structures reduce ambiguity and prevent quality degradation caused by role overlap or lack of ownership.

This structured responsibility mapping is particularly relevant in regulated environments where independence of verification activities may be required.


### 4.7 Synthesis  

The quantitative approach to software engineering frames development as:

- A feedback-driven process  
- A measurable quality system  
- An architecture-centered discipline  
- A continuously improving workflow  

In safety-critical and regulated domains such as medical device software, these principles align naturally with regulatory expectations. Quantification, automation, structured verification, and documented accountability provide the engineering foundation upon which regulatory compliance can reliably be built.