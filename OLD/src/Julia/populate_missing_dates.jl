function populate_missing_dates!(df::DataFrame )
    # Assuming:
    # Rata_Die        is column #1
    # Data            is column #2
    # value quantized is column #3
    # original value  is column #4

    count = size(df)[1]

    for i in 1:count-1
        day_this = df[i   ,1] # current row, "Rata_Die" column
        day_next = df[i+1 ,1] # next row   , "Rata_Die" column

        original = df[i,3] # Original  value
        value    = df[i,4] # Quantized value

        # Assuming that this last known value should be propagated until next update 
        # loop thru all days you need to insert  day_this [...] day_next
        # if there is no gap, nothing will happen
        days_to_fill = day_this+1:day_next-1

        for day in days_to_fill
            date = rata2datetime(day) #  Dates.format(rata2datetime(day), "yyyy-mm-dd")
            push!(df, [ day date original value  ])
        end

    end

    # sort by Day (Rata Die)
    df = sort(df, [:Rata_Die]);

    return df # Not strictly necessary as df is already changed
end