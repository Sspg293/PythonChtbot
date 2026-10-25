# Local AI Chatbot (FLAN-T5 Small)

This project runs a lightweight open-source model through Streamlit.

## Windows setup

1. Extract this ZIP file.
2. Open Command Prompt or PowerShell in the extracted folder.
3. (Recommended) Create a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt and run:
   `.venv\Scripts\activate.bat`

4. Install the packages:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Launch:

   ```powershell
   streamlit run app.py
   ```

6. Open the local URL shown in the terminal, usually http://localhost:8501.

## Important notes
- The first launch requires internet to download `google/flan-t5-small`.
- Once downloaded, it can run without external AI APIs; offline operation depends on model files and packages already being cached/installed.
- FLAN-T5 Small is lightweight but less capable than larger chat-specific language models.
