using DataFrames, CSV

function fetch_local_CSV_as_DataFrame(
        file_name="TPLGX.csv", 
        date_format="yyyy-mm-dd", # my preferred default
        dir="../DATA/original/"
    )

    file_path = dir * file_name

    df = CSV.read(file_path, DataFrame, dateformat=date_format)
    

    ## Note: sort does not work at this point because column names vary
    # df = sort(df, [ :Date ]);
    # df = sort(df, [ :"Date       "] ); # spaces in the string

    #println("Fetched ", file_path, ", record count ", size(df)[1])
    
    return df # DataFrame
end