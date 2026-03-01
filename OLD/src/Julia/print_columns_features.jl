function print_columns_features(df)
    columns = names(df)
    for i in 1:length(columns)
        println(",\"", columns[i] , "\"")
    end
    return columns
end