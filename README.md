# Markdown, MARP & Mermaid Renderer

A powerful web application built with Streamlit that allows you to render and convert Markdown, MARP slides, and Mermaid diagrams to PDF.

![App Screenshot](screenshot.png)

## Features

- **Markdown Rendering**: Write and preview standard Markdown with support for:
  - Math equations (MathJax)
  - Code highlighting
  - Tables
  - Fenced code blocks

- **MARP Slides**: Create presentation slides using MARP syntax
  - Slide separation with `---`
  - Styled slide layout
  - Export to PDF

- **Mermaid Diagrams**: Create and visualize:
  - Flowcharts
  - Sequence diagrams
  - Gantt charts
  - Class diagrams
  - And more!

- **PDF Export**: Convert any rendered content to downloadable PDF files

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/markdown-marp-mermaid-renderer.git
   cd markdown-marp-mermaid-renderer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Mermaid CLI (required for Mermaid diagram rendering):
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. Select your desired render type from the sidebar:
   - Markdown
   - MARP
   - Mermaid

4. Write or paste your content in the editor

5. Click "Generate PDF" to create and download a PDF of your rendered content

## Example Content

### Markdown Example
```markdown
# Hello Markdown

This is a **bold** statement and this is *italic*.

## Math Example
$E = mc^2$

## Code Example
```python
def hello_world():
    print("Hello, World!")
```

### MARP Example
```markdown
# Slide 1

This is the first slide

---

# Slide 2

This is the second slide with a list:
- Item 1
- Item 2
```

### Mermaid Example
```
graph TD
    A[Start] --> B{Is it working?}
    B -->|Yes| C[Great!]
    B -->|No| D[Debug]
    D --> B
```

## Requirements

- Python 3.7+
- Streamlit
- WeasyPrint
- BeautifulSoup4
- Markdown
- Streamlit-ace
- Node.js (for Mermaid CLI)

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
```

This README provides a comprehensive overview of the application, including its features, installation instructions, usage guide, example content for each render type, and other essential information for users.
