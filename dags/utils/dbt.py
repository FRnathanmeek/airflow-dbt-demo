

def manifest_parsing(model_tag='staged'):
    import pandas as pd
    import os
    DBT_PROJECT_DIR = "/opt/airflow/dbt"
    manifest_path = os.path.join(DBT_PROJECT_DIR, "target/manifest.json")
    manifest_df = pd.read_json(manifest_path)
    manifest_df.dropna(subset=['nodes'], inplace=True)

    models = []

    for node in manifest_df['nodes']:
        if node != 'NA':
            print('===============')
            print(f"Model ID: {node['unique_id']}")
            if model_tag in node['tags']:
                models.append(node['unique_id'])
                print(f"! Model added ! --> {node['name']}")

    return models
