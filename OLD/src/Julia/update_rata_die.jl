function update_rata_die!(df, days_column=1, date_column=2)
    rows = size(df)[1] # first part of the returned tupple

    for row = 1:rows
        df[row, days_column] = Dates.datetime2rata( Date(df[row, date_column]) ) 
    end
    return df
end