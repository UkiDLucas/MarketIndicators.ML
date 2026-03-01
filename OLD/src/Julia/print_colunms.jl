function print_colunms(df)
    columns = names(df)
    for i in 1:length(columns)
        println(i, " ", columns[i])
    end
    return columns
end