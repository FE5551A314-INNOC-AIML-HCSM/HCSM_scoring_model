from dagster import op
import pandas as pd

from dagster import op, Out, Output, Config
import os
import pandas as pd
import sweetviz as sv
from tqdm import tqdm

class GenericDataFrameAnalyseConfig(Config):
    input_folder: str
    output_folder: str
    analyze_columns: list = None
    extract_columns: list = None
    testing: bool = False
    max_lines: int = 1000
    exclude_files: list = None
    testing_output_subfolder: str = "testing_data"
    columns_description_file: str = None
    main_file: str = None
    files_with_target: list = None
    target_column: str = None
    chunksize: int = 50000

@op(
    config_schema=GenericDataFrameAnalyseConfig.to_dict(),
    out=Out(description="Path to the combined analysis parquet.gz file"),
    description="Processes parquet.gz files and generates Sweetviz reports along with combined analysis."
)
def generic_dataframe_analyse(context):
    config = GenericDataFrameAnalyseConfig(**context.op_config)

    # Ensure output directories exist
    final_output_folder = config.output_folder
    if config.testing:
        final_output_folder = os.path.join(config.output_folder, config.testing_output_subfolder)
    os.makedirs(final_output_folder, exist_ok=True)

    # List all Parquet files
    parquet_files = [f for f in os.listdir(config.input_folder) if f.endswith('.parquet.gz')]
    if config.exclude_files:
        parquet_files = [f for f in parquet_files if f not in config.exclude_files]

    # Initialize lists for missing values and metadata
    missing_values_list = []
    metadata_list = []

    # Load the column description file if provided
    hccd = None
    if config.columns_description_file:
        hccd = pd.read_csv(os.path.join(config.input_folder, config.columns_description_file), encoding="ISO-8859-1")
        hccd.rename(columns={'Table': 'DataFrame Name'}, inplace=True)

    # Load the main file containing the target column
    main_df = pd.read_csv(os.path.join(config.input_folder, config.main_file)) if config.main_file else None

    # Process each Parquet file
    for filename in tqdm(parquet_files, desc="Processing Parquet files", unit="file"):
        file_path = os.path.join(config.input_folder, filename)
        context.log.info(f"Processing file: {file_path}...")

        # Load the file in chunks
        chunk_iter = pd.read_parquet(file_path, engine='pyarrow', chunksize=config.chunksize)

        for chunk in chunk_iter:
            # Apply testing limits
            if config.testing:
                chunk = chunk.head(config.max_lines)

            # Extract specific columns
            if config.extract_columns:
                chunk = chunk[config.extract_columns]

            # Merge with the target column if applicable
            if main_df is not None and config.target_column in main_df.columns:
                if 'SK_ID_CURR' in chunk.columns:
                    chunk = chunk.merge(main_df[['SK_ID_CURR', config.target_column]], on='SK_ID_CURR', how='left')

            # Generate Sweetviz reports
            report = sv.analyze(chunk[config.analyze_columns]) if config.analyze_columns else sv.analyze(chunk)
            report_path = os.path.join(final_output_folder, f"{os.path.splitext(filename)[0]}_sweetviz_report.html")
            report.show_html(report_path, open_browser=False)
            context.log.info(f"Sweetviz report saved to {report_path}")

            # Analyze missing values
            missing_values = chunk.isnull().sum().reset_index()
            missing_values.columns = ['Column', 'MissingValues']
            missing_values['Percentage'] = 100 * missing_values['MissingValues'] / len(chunk)
            missing_values['DataFrame Name'] = filename
            missing_values_list.append(missing_values)

            # Generate metadata
            metadata = {
                'Column': chunk.columns,
                'UniqueValues': [chunk[col].nunique() for col in chunk.columns],
                'DataType': [chunk[col].dtype for col in chunk.columns],
                'DataFrame Name': filename
            }
            metadata_df = pd.DataFrame(metadata)
            metadata_list.append(metadata_df)

    # Combine and save missing values and metadata
    combined_missing_values = pd.concat(missing_values_list, axis=0)
    combined_metadata = pd.concat(metadata_list, axis=0)

    if hccd is not None:
        combined_missing_values = combined_missing_values.merge(hccd, on='Column', how='left')
        combined_metadata = combined_metadata.merge(hccd, on='Column', how='left')

    # Save combined analysis as .parquet.gz
    combined_analysis = pd.concat([combined_missing_values, combined_metadata], axis=1)
    combined_analysis_file = os.path.join(final_output_folder, "combined_analysis.parquet.gz")
    combined_analysis.to_parquet(combined_analysis_file, compression='gzip')
    context.log.info(f"Combined analysis saved to {combined_analysis_file}")

    return Output(combined_analysis_file, description="Path to the combined analysis parquet.gz file")
