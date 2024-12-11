# Final_IOT_Project_Instructions_Aline_Orrantia


Welcome to IOT Project.

## File Structure

Maintaining an organized folder structure is crucial to project efficiency. Organize your files as follows:

- **`Input` Folder**: 
  - In case of not having the .env in Config folder, we are going to use sample real data.

- **`Config` Folder**: api keys.
    - `.env` file, with api keys.

- **`Output` Folder**: 
  - Output data we load locally

Make sure to download all relevant files and place them in the appropriate folders as above.

## Environment Configuration and Dependencies

To configure your environment and ensure that all necessary dependencies are installed, follow these steps:

1. **Download Anaconda**: Download the latest version of Anaconda from your [official website](https://www.anaconda.com/products/distribution). 

2. **Open Anaconda Prompt**: Once Anaconda is installed, start Anaconda Prompt from your start menu.

3. **Create a New Environment with Python 3.12**: In Anaconda Prompt, create a new environment called `IOT_project_env` with Python 3.12 using the following command:
   ```bash
   conda create --name IOT_project_env python=3.12

4. **Activate the Environment**: Activate the newly created environment with the command:
   ```bash
   conda activate IOT_project_env
   
5. **Switch to Repository Directory**: Navigate to the directory where the repository is cloned using the cd command. For example:
    ```bash
    cd /Users/alineorrs/Desktop/Msc/IOT/IOT_Project_AOV
  
    
6. **Install PDM**: Within the activated environment, install PDM using pip with the following command:
    ```bash
    pip install pdm
    
7. **Install Dependencies with PDM**: Run pdm install to install all project dependencies defined in the pyproject.toml file. Use the following command:
    ```bash
    pdm install

8. **Open Anaconda Navigator**: Finally, since the latest versions of Anaconda Navigator have had problems installing Spyder from Home, the ideal
It will be to open spyder from the "root" Environment and then, go to the spyder navigation bar, then to tools, then to preferences, then to Python Interpreter
and then, we select the option "Use the following Python interpreter" and then we select the icon on the right side to search for the environment, once selected, click Apply and then Ok. Finally, returning to the screen
normal spyder, we restart the console and we will see that a legend will appear that tells us to use conda or pip to install the kernel, then we copy and paste
the pip command that the spyder console gives us and we paste it into the anaconda prompt and run it, this with the activated environment that we did previously, called
IOT_project_env

9. **Run app.py**: Finally, run app.py.
