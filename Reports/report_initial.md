

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