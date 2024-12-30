import os
from typing import List
import pandas as pd
from dagster import op, In, Optional

import os

@op(required_resource_keys={"s3"})
def download_csv_from_s3(context, bucket_name: str, prefix: str, local_folder: str):
    """
    Download all files from a specified S3 bucket and prefix to a local folder, 
    skipping files that already exist locally with the same size.

    Args:
        context: Dagster context with access to S3 resource.
        bucket_name (str): Name of the S3 bucket.
        prefix (str): Prefix in the S3 bucket to filter objects.
        local_folder (str): Local folder to store the downloaded files. Defaults to 'data/raw'.

    Returns:
        List[str]: A list of local file paths for the downloaded files.
    """
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    s3 = context.resources.s3

    # List all objects in the S3 bucket with the specified prefix
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if "Contents" not in response:
        context.log.info(f"No files found in bucket '{bucket_name}' with prefix '{prefix}'.")
        return []

    files = [obj for obj in response["Contents"]]
    local_files = []

    for obj in files:
        file_key = obj["Key"]
        s3_file_size = obj["Size"]
        local_file_path = os.path.join(local_folder, os.path.basename(file_key))

        # Check if file exists locally and sizes match
        if os.path.exists(local_file_path):
            local_file_size = os.path.getsize(local_file_path)
            if local_file_size == s3_file_size:
                context.log.info(f"Skipped {file_key} (already downloaded and size matches).")
                local_files.append(local_file_path)
                continue

        # Download the file if not already downloaded or size doesn't match
        try:
            context.log.info(f"Downloading {file_key}...")
            s3.download_file(bucket_name, file_key, local_file_path)
            context.log.info(f"Downloaded {file_key} to {local_file_path}")
            local_files.append(local_file_path)
        except Exception as e:
            context.log.error(f"Failed to download {file_key}: {e}")

    context.log.info(f"Downloaded {len(local_files)} files to {local_folder}.")
    return local_files

@op(required_resource_keys={"s3"})
def upload_folder_to_s3(context, folder_path: str, bucket_name: str, s3_prefix: str = "") -> None:
    s3_client = context.resources.s3  # Access the S3 client from the resource

    # List all files in the folder
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # Define S3 key (path in the bucket)
            relative_path = os.path.relpath(file_path, folder_path)
            s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")  # Normalize path for S3

            try:
                # Upload file to S3
                s3_client.upload_file(file_path, bucket_name, s3_key)
                context.log.info(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")
            except Exception as e:
                context.log.error(f"Failed to upload {file_path}: {e}")

@op(required_resource_keys={"s3"})
def convert_csv_to_parquet_gz(
    context, 
    input_folder: str, 
    output_folder: str, 
    chunksize: int = 50000, 
    skip_existing: bool = True
) -> List[str]:
    import chardet

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    csv_files = [
        os.path.join(input_folder, file)
        for file in os.listdir(input_folder)
        if file.endswith(".csv")
    ]

    if not csv_files:
        context.log.warning("No CSV files found in the input folder.")
        return []

    parquet_files = []
    for csv_file in csv_files:
        parquet_file = os.path.join(output_folder, os.path.basename(csv_file).replace(".csv", ".parquet.gz"))

        # Skip the file if it already exists and skip_existing is True
        if skip_existing and os.path.exists(parquet_file):
            context.log.info(f"Skipping {csv_file} as {parquet_file} already exists.")
            parquet_files.append(parquet_file)
            continue

        with open(csv_file, 'rb') as file:
            raw_data = file.read(10000)
            detected_encoding = chardet.detect(raw_data)['encoding']

        try:
            for chunk in pd.read_csv(csv_file, chunksize=chunksize, encoding=detected_encoding):
                chunk.to_parquet(parquet_file, compression="gzip", index=False)
            context.log.info(f"Converted {csv_file} to {parquet_file}")
            parquet_files.append(parquet_file)
        except Exception as e:
            context.log.error(f"Failed to process {csv_file}: {e}")

    return parquet_files

@op
def load_data_files(input_folder: str, columns_description_file: str, main_file: str):
    # Load column descriptions
    hccd = pd.read_csv(os.path.join(input_folder, columns_description_file), encoding="ISO-8859-1")
    hccd.rename(columns={"Table": "DataFrame Name"}, inplace=True)

    # Load the main file containing the target column
    main_df = pd.read_csv(os.path.join(input_folder, main_file))

    return {"hccd": hccd, "main_df": main_df}

@op
def analyze_missing_values(data_chunk, filename: str):
    # Create a table with the number and percentage of missing values
    mis_val = data_chunk.isnull().sum()
    mis_val_percent = 100 * data_chunk.isnull().sum() / len(data_chunk)
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
    mis_val_table.columns = ["Missing Values", "% of Total Values"]
    mis_val_table["DataFrame Name"] = filename
    return mis_val_table.reset_index().rename(columns={"index": "Row"})


@op(ins={"target_column": In(Optional[str])})
def generate_column_metadata(data_chunk, filename: str, target_column: Optional[str] = None):
    # Generate metadata for each column
    metadata = []
    for col in data_chunk.columns:
        corr = None
        if target_column and col != target_column:
            try:
                corr = data_chunk[col].corr(data_chunk[target_column])
            except Exception:
                pass

        metadata.append({
            "Row": col,
            "Corr_Target_Before_Cleaning": corr,
            "Data_Type": data_chunk[col].dtype,
            "Unique_Values": data_chunk[col].nunique(),
            "DataFrame Name": filename
        })
    return pd.DataFrame(metadata)


@op
def save_results(hccd, missing_values, metadata, output_folder: str, compression_type: str = "gzip"):
    # Merge results
    result_all_columns = pd.merge(hccd, missing_values, on=["Row", "DataFrame Name"], how="inner")
    result_all_columns = pd.merge(result_all_columns, metadata, on=["Row", "DataFrame Name"], how="inner")

    # Save to output
    output_path = os.path.join(output_folder, "hccd_and_missing_values_all_dfs.csv")
    if compression_type == "gzip":
        result_all_columns.to_csv(output_path + ".gz", index=False, compression="gzip")
    else:
        result_all_columns.to_csv(output_path, index=False)
    return f"Results saved at {output_path}"


@op(required_resource_keys={"s3"})
def upload_results_to_s3(context, results: dict, bucket_name: str, output_prefix: str):
    s3 = context.resources.s3
    output_missing_values = os.path.join(output_prefix, "missing_values.parquet.gz")
    output_metadata = os.path.join(output_prefix, "metadata.parquet.gz")

    # Save results locally
    results["missing_values"].to_parquet("missing_values.parquet.gz", compression="gzip", index=False)
    results["metadata"].to_parquet("metadata.parquet.gz", compression="gzip", index=False)

    # Upload to S3
    s3.upload_file("missing_values.parquet.gz", bucket_name, output_missing_values)
    s3.upload_file("metadata.parquet.gz", bucket_name, output_metadata)

    context.log.info(f"Uploaded missing values to s3://{bucket_name}/{output_missing_values}")
    context.log.info(f"Uploaded metadata to s3://{bucket_name}/{output_metadata}")