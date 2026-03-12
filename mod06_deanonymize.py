import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    com_cols = list(set(anon_df.columns) & set(aux_df.columns))
    com_cols.remove('anon_id')
    merge_df = pd.merge(
        anon_df, 
        aux_df, 
        on=com_cols, 
        how='inner', 
        suffixes=('_anon', '_aux')
    )
    match_counts = merge_df['anon_id'].value_counts()
    unique_id = match_counts[match_counts == 1].index
    final_matches = merge_df[merge_df['anon_id'].isin(unique_id)]
    return final_matches[['anon_id', 'matched_name']]


    #raise NotImplementedError


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    if len(matches_df) == 0 or len(anon_df) == 0:
        return 0
    tot_recs = len(anon_df)
    unique_recs = len(matches_df)
    return unique_recs/tot_recs
    #raise NotImplementedError
