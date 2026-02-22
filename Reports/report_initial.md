

# Initial Literature Review

## 1. Introduction

This report documents the initial phase of theoretical and regulatory study undertaken within the scope of the AI4MDR project.
Its purpose is to consolidate the main concepts, definitions, and normative requirements identified in the literature reviewed during this stage, with particular emphasis on medical device software lifecycle processes, safety classification, risk-related obligations, and documentation and traceability expectations. The content presented here supports the subsequent structuring of the state-of-the-art review and provides a grounded basis for later methodological and technical decisions.

## 2. Regulatory Qualification of Medical Device Software
The regulatory qualification of software constitutes the first essential step before applying any lifecycle or safety standard. In the European Union, the determination of whether software qualifies as a Medical Device Software (MDSW) is governed by Regulation (EU) 2017/745 (MDR), Regulation (EU) 2017/746 (IVDR), and further clarified by MDCG 2019-11 guidance.

A medical device is  any instrument, apparatus, appliance, software, implant, reagent, material or other article intended by the manufacturer to be used for specific medical purposes, including diagnosis, prevention, monitoring, prediction, prognosis, treatment or alleviation of disease. Therefore, qualification depends primarily on the intended purpose defined by the manufacturer.
The European Commission guidance “Is your software a Medical Device?” provides a structured decision process to determine whether software qualifies as Medical Device Software (MDSW). The assessment focuses on three main criteria.

First, the product must qualify as software under MDCG 2019-11 and perform actions on data beyond mere storage, communication, or basic search functions. Software that only stores or transfers data does not qualify as MDSW.

Second, the software must generate or transform medical information, such as through analysis, interpretation, or calculation supporting clinical decisions.

Third, the intended benefit must relate to individual patients and medical objectives. Software used solely for administrative, regulatory, or general purposes does not meet the definition.

If these conditions are satisfied, the software qualifies as Medical Device Software and falls under MDR or IVDR, depending on its intended purpose.
## 3. Regulatory and Process Foundations for Medical Device Software

### 3.1 Lifecycle-Oriented Regulatory Framework

Medical device software operates within a highly regulated environment in which safety and effectiveness must be demonstrated through structured and documented processes. IEC 62304 establishes a lifecycle-based framework defining processes, activities, and tasks required for the development and maintenance of medical device software (IEC 62304:2006).

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

Traceability emerges as a recurring and structurally central requirement. Requirements must be uniquely identifiable, testable, consistent, and linked to system requirements and risk control measures. Verification activities must demonstrate correct implementation of requirements, and test results must be formally documented (IEC 62304:2006).

Traceability is not limited to requirements and tests. It extends across architectural elements, configuration items, change requests, problem reports, and safety classifications. The ability to reconstruct links between artefacts is essential for demonstrating regulatory compliance and supporting audit processes.

The standard allows flexibility in implementation methods; however, when requirements are deemed “not applicable” or “as appropriate,” documented justification is required.

### 3.4 Maintenance, Configuration Management and Problem Resolution

Maintenance is treated as a formal lifecycle process rather than a secondary phase. Post-release feedback must be monitored and evaluated for safety impact. Any modification must follow structured change control procedures, including impact assessment and verification before re-release.

Configuration management requires that all software items be uniquely identified and version-controlled. Changes must originate from approved change requests, and historical configurations must be recoverable to ensure auditability and reproducibility.

Problem resolution requires formal problem reports, classification of severity, investigation of root causes, evaluation of safety implications, and verification that corrective actions do not introduce new defects. Where relevant, updates must be reflected in the Risk Management File.

### 2.5 Contextual and Normative Integration

The informative annexes of IEC 62304 provide interpretative guidance and clarify the relationship between lifecycle requirements and other standards. In particular, Annex C highlights the integration of IEC 62304 with ISO 13485 (Quality Management Systems) and ISO 14971 (Risk Management), reinforcing that software lifecycle control operates within a broader regulatory structure.

This contextual integration confirms that compliance with IEC 62304 is not isolated but interconnected with overarching quality and safety management frameworks.
|