# Marchiver Architecture Documentation

This directory contains comprehensive architecture documentation for the Marchiver application, a personal knowledge archiving and retrieval system.

## Documentation Files

1. **[Architecture Summary](marchiver_architecture_summary.md)**: A comprehensive overview of the entire system architecture
2. **[Block Diagram](marchiver_architecture.md)**: High-level components and their relationships
3. **[Data Flow Diagram](marchiver_data_flow.md)**: Detailed illustration of how data moves through the system
4. **[Component Architecture](marchiver_component_architecture.md)**: Internal structure of each major component

## Viewing the Diagrams

The architecture documentation uses Mermaid diagrams, which can be viewed in several ways:

### Option 1: GitHub Rendering

If you push these files to a GitHub repository, GitHub will automatically render the Mermaid diagrams in the markdown files.

### Option 2: VS Code Extension

Install the "Markdown Preview Mermaid Support" extension in VS Code:
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Markdown Preview Mermaid Support"
4. Install the extension
5. Open any of the markdown files
6. Click the "Open Preview" button in the top-right corner of the editor

### Option 3: Mermaid Live Editor

1. Copy the Mermaid diagram code (the content between the \`\`\`mermaid and \`\`\` tags)
2. Go to [Mermaid Live Editor](https://mermaid.live/)
3. Paste the code into the editor
4. View the rendered diagram

### Option 4: Browser Extensions

Several browser extensions can render Mermaid diagrams in markdown files:
- Chrome: "Markdown Diagrams"
- Firefox: "Markdown Viewer Webext"

## Understanding the Architecture

The documentation is structured to provide multiple perspectives on the system:

1. **Block Diagram**: Start here for a high-level overview of the main components and how they interact.

2. **Data Flow Diagram**: This shows how information moves through the system during key operations like saving a page, searching, or viewing a document.

3. **Component Architecture**: Dive deeper into the internal structure of each component, showing classes, methods, and relationships.

4. **Architecture Summary**: Ties everything together with textual descriptions and explanations.

## Modifying the Diagrams

If you need to update the diagrams:

1. Edit the corresponding markdown file
2. Modify the Mermaid diagram code between the \`\`\`mermaid and \`\`\` tags
3. Use one of the viewing options above to preview your changes

## Additional Resources

- [Mermaid Documentation](https://mermaid-js.github.io/mermaid/#/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Chrome Extension Development](https://developer.chrome.com/docs/extensions/)
