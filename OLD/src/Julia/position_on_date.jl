function position_on_date(df, date_string="2020-09-25")
    date = Date(date_string, "yyyy-mm-dd") # typeof Date
    found_items = df[df.Date .== date, 3] # Array{Float64,1}, find all rows for given date, and get value from column 3  

    record_count = size(df)[1]    # number of rows in the whole dataset
    position = zeros(Float64, record_count) # zero-fill array

    position .= found_items[1]

    # if length(found_items) > 0
    #     for i in 1:record_count
    #         position[i] = found_items[1]
    #     end
    # end

    return position
end