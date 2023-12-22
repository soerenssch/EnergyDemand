# Streamlit App Installation

0. Configuration:

Before running the app, make sure to replace the placeholder API key in `.streamlit/secrets.toml` with the actual API key:

[api_key](https://bscdocs.elexon.co.uk/guidance-notes/bmrs-api-and-data-push-user-guide)

[weather_key](https://openweathermap.org/api)

1. Create a virtual environment:

    ```bash
    python -m venv .venv
    ```

2. Activate the virtual environment:

    - On Windows:

        ```bash
        .venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source .venv/bin/activate
        ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
    
4. Run the Streamlit App:

    ```bash
    streamlit run UK_Energy_Demand.py
    ```