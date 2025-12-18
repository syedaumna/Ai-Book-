# Documentation Restructuring Rules and Contracts

This document formalizes the rules and expectations governing the documentation restructuring process for "The Physical Human Robotic AI" project. It serves as a contract ensuring the integrity, consistency, and usability of the documentation throughout and after the reorganization.

## 1. Folder Structure Contract

### 1.1 New Parent Folder

-   **Contract**: A single top-level parent folder MUST be created directly under `docs/` named "The Physical Human Robotic AI".
-   **Enforcement**: All restructured chapter content MUST reside within this folder.

### 1.2 Chapter Folder Naming

-   **Contract**: Chapter folders MUST be named consistently using the pattern "Chapter-X", where X is a sequential integer (e.g., "Chapter-1", "Chapter-2").
-   **Mapping**: There MUST be a clear, one-to-one mapping from original Module folders to new Chapter folders.

## 2. File Integrity Contract

### 2.1 Content Preservation

-   **Contract**: The content of all documentation files (`.md`, `.mdx`) and associated asset files MUST be preserved exactly as they were before the move. No content alteration is permitted.
-   **Enforcement**: File hashes (e.g., MD5, SHA256) MAY be used to verify content integrity before and after moving.

### 2.2 No Data Loss/Deletion

-   **Contract**: No documentation files or assets present in the original module structure MUST be lost or inadvertently deleted.
-   **Enforcement**: A comprehensive pre-restructuring manifest of all files and their paths MUST be compared against a post-restructuring manifest.

### 2.3 No Empty Files

-   **Contract**: After restructuring, no documentation file within any of the new chapter folders MUST be empty (i.e., contain no meaningful content).
-   **Enforcement**: A check for non-empty content after moving. If a file would become empty due to some unforeseen edge case, a reasonable default professional markdown section MUST be generated.

## 3. Link Consistency Contract

### 3.1 Internal Relative Link Updates

-   **Contract**: All internal relative links within `.md` and `.mdx` files MUST be updated to correctly point to their new targets after files have been moved.
-   **Scope**: This includes links to other documentation files, images, and other assets that have been relocated.
-   **Enforcement**: Automated regex-based parsing and path recalculation will be performed. Manual spot-checking and Docusaurus build verification will confirm correctness.

### 3.2 External Link Preservation

-   **Contract**: External links (e.g., to `https://docs.ros.org/`) and absolute links (`/assets/image.png` if it resolves to a root asset) MUST remain unchanged.
-   **Enforcement**: Parsing logic must distinguish internal relative links from external/absolute ones.

## 4. Docusaurus Compatibility Contract

### 4.1 Build Success

-   **Contract**: The Docusaurus website MUST build successfully with the new documentation structure.
-   **Enforcement**: Running `npm run build` (or equivalent) for the Docusaurus project.

### 4.2 Navigation Integration

-   **Contract**: The new chapter structure MUST be correctly integrated into `sidebars.ts` to reflect the updated documentation hierarchy in the website's navigation.
-   **Enforcement**: Verification of `sidebars.ts` content and visual inspection of the running Docusaurus development server.

## 5. Scripting and Automation Contract

### 5.1 Idempotency

-   **Contract**: Any scripts used for the restructuring SHOULD be idempotent where feasible, meaning running them multiple times yields the same result without unintended side effects.
-   **Rationale**: Facilitates debugging and recovery.

### 5.2 Logging

-   **Contract**: Scripts SHOULD log actions performed, files moved, and links updated for auditability and debugging.

This contract provides a clear framework for ensuring a successful and verifiable documentation restructuring process.
