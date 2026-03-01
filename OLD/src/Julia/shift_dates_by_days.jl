function shift_dates_by_days!(df::DataFrame, shift_days::Int64=-1, date_column::Int64=1)
    rows = size(df)[1]
    
    for row in 1:rows
        original = Date(df[row, date_column]) 
        shifted = original + Dates.Day(shift_days)
        # println("original ", original, " ", shift_days, " shift ", shifted)
        df[row, date_column] = shifted
    end
    return df
end