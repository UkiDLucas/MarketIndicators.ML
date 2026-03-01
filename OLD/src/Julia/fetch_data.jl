function fetch_data(file_path, date_format="yyyy-mm-dd")
    isfile(file_path) || # does file exist locally?
        download( string("https://raw.githubusercontent.com/UkiDLucas/MarketIndicators.jl/master/", 
            file_path), # URL
        file_path) # save it as name
    
    return CSV.read(        # returns DataFrame
        file_path, 
        dateformat="$date_format"
        )
end