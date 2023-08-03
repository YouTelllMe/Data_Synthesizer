import pandas as pd
import config
import os
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata

"""
DOCS: 
https://docs.sdv.dev/sdv/single-table-data/data-preparation
- fit: https://dai.lids.mit.edu/wp-content/uploads/2018/03/SDV.pdf 
"""

def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load raw data into a pd.DataFrame
    """
    sample_df = pd.read_excel(config.DATA_PATH, config.TARGET_SHEET)

    # explore data set 
    # print(sample_df.head())

    # take out variance
    variance = sample_df["Var_X"]
    sample_df.drop(columns = ["Var_X"], inplace=True)

    return(sample_df, variance)


def create_metadata(data: pd.DataFrame) -> SingleTableMetadata:
    """
    Metadata methods:
    1. to_dict(): convert to Python dict
    2. validate(): check if metadata is valid
    3. update_column(column_name, sdtype, ...): sdtype is the data type, other kargs based on data type
        - functionalities: set data as sensitive, dates, ID (so no affect on fit)

    Param: 
    data: data to fit into synthesizer
    """
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(data=data)
    return(metadata)


def create_gaussian_synthesizer(metadata: SingleTableMetadata) -> GaussianCopulaSynthesizer:
    """
    Hyperparams (Optional)
    1. enforce_min_max_values: bounded upper lower?
    2. enforce_rounding: same decimal as data?
    3. locales: 
    4. numerical_distributions: for sampling (give a type); dict[col_name, type]
    5. default_distribution: set default distribution

    Synthesizer methods: 
    1. get_parameters(): get hyperparams
    2. get_metadata()
    3. fit(data)
    4. sample(num_rows=10)
    5. get_learned_distributions(): dict[col_name, dict[params/distrib, fit_param]]
    """
    synthesizer = GaussianCopulaSynthesizer(metadata)
    return(synthesizer)


if __name__ == "__main__":

    sample_data = load_data()[0]
    if os.path.isfile(config.SAVE_META_PATH):
        # load
        sample_metadata = SingleTableMetadata.load_from_json(filepath=config.SAVE_META_PATH)
        sample_metadata.validate()
    else:
        sample_metadata = create_metadata(sample_data)
        sample_metadata.update_column("ID", sdtype='id')
        sample_metadata.set_primary_key(column_name='ID')
        sample_metadata.validate()

        # save
        sample_metadata.save_to_json(filepath=config.SAVE_META_PATH)

    if os.path.isfile(config.SAVE_SYNTH_PATH):
        # load
        sample_synthesizer = GaussianCopulaSynthesizer.load(
            filepath=config.SAVE_SYNTH_PATH
        )
    else: 
        sample_synthesizer = create_gaussian_synthesizer(sample_metadata)
        sample_synthesizer.fit(sample_data)
        # save
        sample_synthesizer.save(config.SAVE_SYNTH_PATH)
    
    synthetic_data = sample_synthesizer.sample(num_rows=10)
    print(synthetic_data.head())
    print(len(synthetic_data))
    print(sample_synthesizer.get_learned_distributions())
