using DataFrames, Statistics

function calculate_average(df::DataFrame, average_days=90, column_to_average= :Quantized)
    record_count = size(df)[1]
    averages = zeros(Float64, record_count) # empty array
    
    for i in average_days:record_count
        day_this = df[i,1] # rata die 
        previous_interval_values = df[i-average_days+1:i, column_to_average]
        avg = round( mean(previous_interval_values) , digits=2) 
        averages[i] = avg
    end
    return averages
end