# Streamlit Local AI Chatbot — Fixed dependencies

## Fix for the screenshot error

The app uses Google's `google/flan-t5-small` model with the
`text2text-generation` pipeline. The screenshot indicates the installed
Transformers version no longer supports that task. This project pins
`transformers==4.44.2`, which supports the pipeline.

## Redeploy on Streamlit Community Cloud

1. Replace your repository's `app.py` with the included `app.py`.
2. Replace `requirements.txt` with the included `requirements.txt`.
3. Commit and push both files to the GitHub repository connected to Streamlit.
4. In Streamlit Cloud, open **Manage app** and reboot/redeploy the app.
5. If the old dependencies remain cached, use the app's reboot/redeploy option
   or clear/rebuild the environment if available.

Do not upload this ZIP to the app URL itself; update the connected GitHub repo.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

The first run needs internet access to download model weights.
