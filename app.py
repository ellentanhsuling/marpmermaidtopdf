import streamlit as st
import markdown
import os
import tempfile
import base64
from bs4 import BeautifulSoup
from weasyprint import HTML
import subprocess
import json
from streamlit_ace import st_ace

# Set page config
st.set_page_config(
    page_title="Markdown, MARP & Mermaid Renderer",
    page_icon="📝",
    layout="wide"
)

# CSS for styling
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    .preview-container {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 1rem;
        background-color: white;
    }
    .mermaid {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("Markdown, MARP & Mermaid Renderer")

# Sidebar options
st.sidebar.header("Options")
render_type = st.sidebar.selectbox(
    "Render Type",
    ["Markdown", "MARP", "Mermaid"]
)

# Function to render markdown
def render_markdown(md_text):
    # Add extensions for math and code highlighting
    extensions = [
        'pymdownx.superfences',
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
        'pymdownx.arithmatex',
        'tables',
        'fenced_code',
        'codehilite'
    ]
    
    html = markdown.markdown(md_text, extensions=extensions)
    
    # Add MathJax support
    html = f"""
    <html>
    <head>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    </head>
    <body>
        {html}
    </body>
    </html>
    """
    return html

# Function to render MARP
def render_marp(md_text):
    # MARP uses standard markdown with special directives
    # For simplicity, we'll use the same markdown renderer with some CSS for slides
    html = render_markdown(md_text)
    
    # Add MARP-like styling
    html = f"""
    <html>
    <head>
        <style>
            .slide {{
                border: 1px solid #ddd;
                padding: 20px;
                margin-bottom: 20px;
                page-break-after: always;
                min-height: 400px;
                position: relative;
            }}
            h1 {{
                font-size: 2em;
            }}
            h2 {{
                font-size: 1.5em;
            }}
        </style>
    </head>
    <body>
    """
    
    # Split by "---" which is the slide separator in MARP
    slides = md_text.split("---")
    
    for slide in slides:
        slide_html = markdown.markdown(slide, extensions=['tables', 'fenced_code'])
        html += f'<div class="slide">{slide_html}</div>'
    
    html += "</body></html>"
    return html

# Function to render Mermaid
def render_mermaid(mermaid_code):
    # Create a temporary file for the Mermaid diagram
    with tempfile.NamedTemporaryFile(suffix='.mmd', delete=False) as tmp:
        tmp.write(mermaid_code.encode('utf-8'))
        tmp_path = tmp.name
    
    # Create a temporary file for the output SVG
    svg_path = tmp_path + '.svg'
    
    try:
        # Use mermaid-cli to render the diagram
        subprocess.run(['mmdc', '-i', tmp_path, '-o', svg_path], check=True)
        
        # Read the SVG content
        with open(svg_path, 'r') as f:
            svg_content = f.read()
        
        # Clean up temporary files
        os.unlink(tmp_path)
        os.unlink(svg_path)
        
        return f"""
        <html>
        <body>
            {svg_content}
        </body>
        </html>
        """
    except Exception as e:
        # If mermaid-cli fails, provide a fallback using mermaid.js
        os.unlink(tmp_path)
        if os.path.exists(svg_path):
            os.unlink(svg_path)
        
        return f"""
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script>
                mermaid.initialize({{ startOnLoad: true }});
            </script>
        </head>
        <body>
            <div class="mermaid">
                {mermaid_code}
            </div>
        </body>
        </html>
        """

# Function to create PDF
def create_pdf(html_content):
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp:
        tmp.write(html_content.encode('utf-8'))
        tmp_path = tmp.name
    
    # Create PDF using WeasyPrint
    pdf_path = tmp_path + '.pdf'
    HTML(tmp_path).write_pdf(pdf_path)
    
    # Read the PDF content
    with open(pdf_path, 'rb') as f:
        pdf_content = f.read()
    
    # Clean up temporary files
    os.unlink(tmp_path)
    os.unlink(pdf_path)
    
    return pdf_content

# Function to create download link
def get_download_link(content, filename, text):
    b64 = base64.b64encode(content).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Main content area
st.subheader("Editor")

# Code editor with empty content
content = st_ace(
    value="",
    language="markdown" if render_type != "Mermaid" else "text",
    theme="github",
    height=500,
    key=f"editor_{render_type}"
)

# Render based on type (but don't display preview)
if render_type == "Markdown":
    html_content = render_markdown(content)
elif render_type == "MARP":
    html_content = render_marp(content)
else:  # Mermaid
    html_content = render_mermaid(content)

# PDF download button
if st.button("Generate PDF"):
    pdf_content = create_pdf(html_content)
    st.markdown(
        get_download_link(
            pdf_content, 
            f"{render_type.lower()}_output.pdf", 
            f"📥 Download {render_type} as PDF"
        ),
        unsafe_allow_html=True
    )

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")