# Quickstart Guide for Documentation Restructuring

This guide provides a quick overview of how to initiate the documentation restructuring process and verify its successful completion. It's intended for a project maintainer or a developer tasked with executing the structural changes.

## 1. Initiate Documentation Restructuring

The documentation restructuring is managed by a dedicated script or a series of commands designed to handle file movements and link updates.

### 1.1 Preparing the Environment

Before initiating, ensure you are on the correct feature branch (`007-doc-restructure` or similar) and that your repository is in a clean state (no uncommitted changes).

```bash
git checkout 007-doc-restructure
git pull origin 007-doc-restructure # Ensure up-to-date
```

### 1.2 Running the Restructuring Script

The restructuring process will typically be encapsulated within a script. (For this example, we assume such a script `restructure_docs.py` or similar will be implemented as part of the tasks).

```bash
# Example: Running a Python script for restructuring
python scripts/restructure_docs.py --mapping-config config/doc_mapping.yaml
```

**Note**: The actual command might vary based on the implementation of the restructuring tasks. It will perform the following steps:
-   Create new parent and chapter folders.
-   Move files from old module paths to new chapter paths.
-   Update internal links within markdown files.
-   Ensure file integrity and non-emptiness.

## 2. Verify Restructuring Outcome

After the restructuring script has completed, it's crucial to verify that all changes were applied correctly and that the documentation remains functional and accurate.

### 2.1 Inspect New Folder Structure

Manually check the `docs/` directory to confirm the creation of "The Physical Human Robotic AI" parent folder and the "Chapter-X" subfolders.

```bash
ls -R docs/The\ Physical\ Human\ Robotic\ AI/
```

### 2.2 Validate File Integrity and Content

Spot-check a few files in each new chapter folder to ensure their content is preserved and no files are unexpectedly empty.

```bash
cat docs/The\ Physical\ Human\ Robotic\ AI/Chapter-1/some_file.md
```

### 2.3 Verify Internal Links (Manual Spot Check)

Open a few restructured markdown files and visually check if internal links (especially to images or other markdown files) are still working or have been correctly updated.

### 2.4 Run Docusaurus Build

The most important verification step is to ensure that Docusaurus can still build the documentation website successfully. This will catch any broken links, invalid file paths, or other structural issues that might prevent the site from rendering.

```bash
npm install # Ensure dependencies are installed
npm run build # Or `yarn build`
```

If the build completes without errors, it's a strong indication of a successful restructuring.

### 2.5 Preview the Documentation Website

After a successful build, serve the Docusaurus site locally to visually inspect the navigation (sidebar) and ensure all chapters and their content are accessible and render correctly.

```bash
npm run start # Or `yarn start`
```

By following these quickstart steps, you can confidently initiate and verify the documentation restructuring, ensuring a smooth transition to the new, organized content hierarchy.
