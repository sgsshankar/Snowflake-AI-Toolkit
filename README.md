# Snowflake AI Toolkit
Snowflake AI Toolkit is an AI Accelerator and Playground for enabling AI in Snowflake. It is an Plug and Play Streamlit based Native App that can be used to explore, learn and build rapid prototypes of AI Solutions in Snowflake powered by the Snowflake's Cortex and AI Functions. 

# Features

### Playground
An interactive environment where users can experiment with Snowflake Cortex functions, test prompts, and and play around with cortex functions.

### Build
A dedicated section for constructing and deploying data pipelines and workflows using Snowflake Cortex's powerful AI capabilities, enabling seamless integration with your Snowflake databases and tables
- Text completion and generation using the COMPLETE function
- Retrieval-Augmented Generation (RAG) for question answering with your own data
- Fine-tuning large language models on your custom datasets

![Snowflake Cortex Demo](assets/demo.gif)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Snowflake Account**: An active Snowflake account with Cortex functionalities enabled.
- **Role Permissions**: ACCOUNTADMIN or equivalent role with permissions to create:
  - Stages
  - Databases
  - Other resources
- **Python**: Version 3.7 or higher.
- **Streamlit**: Installed on your local machine.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sgsshankar/Snowflake-AI-Toolkit.git
   cd snowflake-ai-toolkit
   ```

2. Install dependencies (only required for local development):
   ```bash
   pip install -r requirements.txt
   ```
   
   All necessary libraries are listed in `requirements.txt`.

## Setup

The application will automatically handle:
- Database creation
- Stage setup
- Required resource initialization

Make sure your Snowflake role has the necessary privileges for these operations.

To configure the application mode, update the `mode` parameter in `src/settings_config.json`:
- Set to `"debug"` for local development and editing.
- Set to `"native"` for running natively in Snowflake.

## Running the App

### Locally

Launch the application locally using:
   ```bash
   streamlit run streamlit_app.py
   ```

### Natively on Snowflake
To configure the application mode, update the `mode` parameter in `src/settings_config.json
Set to `"native"` for running natively in Snowflake.

Install snowflake-cli
   ```bash
      pip install snowflake-cli
   ```


To deploy the application natively in Snowflake, use the following command:
   ```bash
   snow streamlit deploy --account "<your_account>" --user "<your_username>" --password "<your_password>" --role "<your_role>" --warehouse "<your_warehouse>" --database "<your_database>" --replace
   ```

Replace the placeholders (`<your_account>`, `<your_username>`, etc.) with your actual Snowflake account details. When running natively in Snowflake, installing dependencies from `requirements.txt` is not needed.

## Project Structure

| File/Directory                      | Description                                      |
|-------------------------------------|--------------------------------------------------|
| [src/](src/)                        | Source code for setup and styling                |
| [src/setup.py](src/setup.py)        | Setup and initialization code                    |
| [src/styles.css](src/styles.css)    | Custom styling                                   |
| [src/build.py](src/build.py)        | Build mode functionality                         |
| [src/cortex_functions.py](src/cortex_functions.py) | Core functions for Cortex operations      |
| [src/query_result_builder.py](src/query_result_builder.py) | Query result handling and display      |
| [src/playground.py](src/playground.py) | Playground mode functionality                  |
| [src/rag.py](src/rag.py) | RAG mode functionality                  |
| [src/fine_tune.py](src/fine_tune.py) | Fine-tuning functionality                  |
| [.gitignore](.gitignore)            | Git ignore file                                  |
| [requirements.txt](requirements.txt)| Project dependencies                             |
| [streamlit_app.py](streamlit_app.py)| Main application entry point                     |


## Troubleshooting

Common issues and solutions:

1. **Snowflake Permission Errors**
   - Verify role privileges for database and stage creation
   - Ensure Cortex functionalities are enabled

2. **Dependency Issues**
   - If pandas/pyarrow installation fails:
     ```bash
     pip install pandas pyarrow
     ```

3. **Connection Issues**
   - Verify Snowflake account credentials
   - Check network connectivity
   - Ensure proper role assignments

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

For assistance:
- Open an issue in the GitHub repository
- Contact project maintainers
- Check documentation for common solutions


## Warranty

The Software is provided as Open Source. This software is provided “as is” and any express or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed. In no event shall the owner or contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.

## Legal

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this tool except in compliance with the License. You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

This is an Open Source repository and not an official Snowflake offering. This tool is not endorsed by Snowflake or any of the previous or current employers of the developers.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. SNOWFLAKE is a trademark of Snowflake Computing, Inc in the United States and/or other countries. Any use of third-party trademarks or logos are subject to those third-party's policies.

