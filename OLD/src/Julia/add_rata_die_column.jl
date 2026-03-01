
function add_rata_die_column!(df)
    rows = size(df)[1] # first number of the tuple
    # https://stackoverflow.com/a/63731422/6312771
    insertcols!(df, 1,  :Rata_Die => 1:rows, makeunique=true) # insert as column 1, populate with 1,2,3,..
    #insert!(df, 1, zeros(Int64, rows), :Rata_Die)

    update_rata_die!(df, 1, 2) # Rata_Die column, Date column
    columns = preview_data(df)
end