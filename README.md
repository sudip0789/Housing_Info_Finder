# Property Information Viewer Application

A comprehensive tool for viewing property information, integrating real-time APIs and AI for a seamless experience.


## Steps to Run the Application

### 1. Python Requirements
Ensure Python 3.8 or above is installed on your system. [Download Python](https://www.python.org/).

### 2. Clone the repository
```bash
git clone https://github.com/sudip0789/Property_Info_Finder_App
cd Property_Info_Finder_App
```

### 3. Install Dependencies
Run the following command in your terminal to install the required Python libraries:
```bash
pip install -r requirements.txt
```

### 4. Access Key Tokens
- **HomeSage.AI Access Key:** Create an access key token from [HomeSage.AI](https://developers.homesage.ai/products/lists/new-search). A 14-day free trial is available.
- **OpenAI Access Key:** Generate an OpenAI access key token. More details can be found in the [OpenAI API Reference](https://platform.openai.com/docs/overview).

### 5. OpenAI Model Selection
This application uses the gpt-4o-mini model, which offers a cost-effective pricing structure. More information on model selection can be found in the [OpenAI Models Guide](https://platform.openai.com/docs/models/). (It costed me 1 cent to test the overall application with gpt-4o-mini model.)

### 6. Update .env file
After creating your access tokens, include the access keys in the .env file.

### 7. Run the application
```bash
streamlit run streamlit_ui.py
```

Open the URL displayed in your terminal to access the application in your browser.
