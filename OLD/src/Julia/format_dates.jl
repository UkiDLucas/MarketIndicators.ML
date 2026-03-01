using Dates
function format_dates(dates, date_format="yy/mdd")
    # dates Array{String,1} or Array{Dates,1}
    columns = length(dates)
    results = Array{String, 1}(undef, columns) # define array to hold x-axis values

    for i in 1:columns
        current_date = dates[i]

        if typeof(current_date) == String
            current_date = Date(current_date)
        end
        
        results[i] = convert(String, Dates.format( current_date, date_format ) )
    end

    return results
end