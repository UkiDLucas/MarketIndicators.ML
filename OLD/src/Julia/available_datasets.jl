function available_datasets()
    file_name="_DataSets.csv"
    date_format="yyyy-mm-dd"
    df = CSV.read( file_name, dateformat=date_format)

    return df[:,[1,2]]
end