import streamlit as st
from src.utils import *
from src.cortex_functions import *
from src.query_result_builder import *
from src.notification import *
import asyncio
import threading
import json


config_path = Path("src/settings_config.json")
with open(config_path, "r") as f:
    config = json.load(f)

def display_rag(session):
    st.title("Retrieval-Augmented Generation (RAG)")
    st.subheader("Use Your Documents As Context To Answer Questions")

    # Display "Create or Use Knowledge Source" dropdown
    create_or_use = st.selectbox("Select Action", ("Create Knowledge Source", "Use Knowledge Source"), key="create_or_use")

    if create_or_use == "Create Knowledge Source":

        # Row 1: Database and Schema Selection
        col1, col2 = st.columns(2)
        with col1:
            selected_db = st.selectbox("Select Database", list_databases(session))
        with col2:
            selected_schema = st.selectbox("Select Schema", list_schemas(session, selected_db))

        # Row 2: Stage Selection and File Upload
        col1, col2 = st.columns(2)
        with col1:
            stages = list_stages(session, selected_db, selected_schema)
            selected_stage = st.selectbox("Select Stage", stages or [])
        with col2:
            if selected_stage:
                uploaded_file = st.file_uploader("Upload File", type=["pdf", "txt"], help="Upload a PDF or TXT file (Max: 5MB)")
                if uploaded_file:
                    try:
                        upload_file_to_stage(session, selected_db, selected_schema, selected_stage, uploaded_file)
                        st.success(f"File '{uploaded_file.name}' uploaded successfully.")
                    except Exception as e:
                        st.error(f"Failed to upload file: {e}")
                        add_log_entry(session, "Upload File", str(e))

        # List files in the stage
        if selected_stage:
            try:
                file_details = list_file_details_in_stage(session, selected_db, selected_schema, selected_stage)
                st.info(f"Number of files in stage '{selected_stage}': {len(file_details)}")
                if file_details:
                    import pandas as pd
                    file_df = pd.DataFrame(file_details)
                    st.table(file_df)
                else:
                    st.warning(f"No files found in stage '{selected_stage}'.")
            except Exception as e:
                st.error(f"Failed to list files in stage: {e}")
                add_log_entry(session, "List Files in Stage", str(e))

        # Embedding Options
        col1, col2 = st.columns(2)
        with col1:
            embedding_type = st.selectbox("Select Embeddings", config["default_settings"]["embeddings"].keys())
        with col2:
            embedding_model = st.selectbox("Select Model", config["default_settings"]["embeddings"][embedding_type])
        # Output Table
        output_table_name = st.text_input("Enter Output Table Name")
        print(output_table_name)

        # Create Embedding
        if st.button("Create Vector Embedding"):
            # Add notification for process tracking
            details = f"Creating vector embeddings in table {output_table_name}"
            print("coming to notification")
            notification_id = add_notification_entry(session, "Create Embedding", "In-Progress", details)
            print("added to notification")
            try:
                # Trigger async embedding creation
                trigger_async_rag_process(
                    session, selected_db, selected_schema, selected_stage, embedding_type,embedding_model, output_table_name, notification_id
                )
                st.success("Embedding creation initiated. Check notifications for updates.")
            except Exception as e:
                # Update notification to Failed and log the error
                update_notification_entry(session, notification_id, "Failed")
                add_log_entry(session, "Create Embedding", str(e))
                st.error(f"Failed to initiate embedding creation: {e}")



    elif create_or_use == "Use Knowledge Source":
        st.subheader("Use Knowledge Source")

        # Database and Schema Selection
        col1, col2 = st.columns(2)
        with col1:
            selected_db = st.selectbox("Select Database", list_databases(session))
        with col2:
            selected_schema = st.selectbox("Select Schema", list_schemas(session, selected_db))

        # Table and Column Selection
        col1, col2 = st.columns(2)
        with col1:
            selected_table = st.selectbox("Select Table", list_tables(session, selected_db, selected_schema) or [] )
        with col2:
            if selected_table:
                required_columns = ["Vector_Embeddings"]
                missing_cols = validate_table_columns(session, selected_db, selected_schema, selected_table, required_columns)
                if missing_cols:
                    print('missing_cols',missing_cols)
                    st.info("The table is missing vector_embeddings column. Please use the appropriate table.")
                else:
                    selected_column = st.selectbox("Select Column", ["Vector_Embeddings"])
        #st.subheader("Select Model, Embedding Type and Emdedding Model")
        st.info("For optimal results, use the same embedding type and model consistently when creating embeddings.")
        col1,col2,col3 =  st.columns(3)
        with col1:
            selected_model = st.selectbox("Select Model", config["default_settings"]["model"])
        with col2:
            embedding_type = st.selectbox("Select Embeddings", config["default_settings"]["embeddings"].keys())
        with col3:
            embedding_model = st.selectbox("Select Model", config["default_settings"]["embeddings"][embedding_type])
        
        question = st.text_input("Enter question", placeholder="Type your question here...")
        rag = st.checkbox("Use your own documents as context?")

        if st.button("Generate"):
            if question:
                try:
                    # Create the prompt
                    prompt = create_prompt_for_rag(session, question, rag, selected_column, selected_db, selected_schema, selected_table,embedding_type,embedding_model)
                    if prompt:
                        prompt = prompt.replace("'", "\\'")
                    # Execute the query and get the result
                    result = execute_query_and_get_result(session, prompt, selected_model, "Generate RAG Response")

                    # Format and display the result
                    format_and_display_result(result, question)
                except Exception as e:
                    # Log the error and show an error message
                    add_log_entry(session, "Generate RAG Response", str(e))
                    st.error("An error occurred while generating the response. Please check the logs for details.")
            else:
                st.error("Please enter a question.")



def trigger_async_rag_process(session, db, schema, stage, embedding_type,embedding_model, output_table, notification_id):
    """Triggers the async RAG embedding creation process with error handling and logging."""
    async def async_rag_process():
        try:
            # Simulate asynchronous processing
            await asyncio.sleep(1)
            
            # Create the embeddings (move this logic to the query_result_builder if necessary)
            create_vector_embedding_from_stage(session, db, schema, stage, embedding_type,embedding_model, output_table)
            
            # Update notification status to Success
            update_notification_entry(session, notification_id, "Success")
            st.success(f"Vector embeddings created successfully in '{output_table}'.")
        except Exception as e:
            # Log the error and update notification status to Failed
            update_notification_entry(session, notification_id, "Failed")
            add_log_entry(session, "Create Vector Embedding", str(e))
            st.error(f"An error occurred: {e}")
            raise e

    # Trigger async process using threading
    thread = threading.Thread(target=asyncio.run, args=(async_rag_process(),))
    thread.start()

