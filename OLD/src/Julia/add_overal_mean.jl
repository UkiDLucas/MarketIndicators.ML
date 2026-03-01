

using Statistics
function add_overal_mean!(df)
    record_count = size(df)[1]
    column_count = size(df)[2]
    
    insert!(df, column_count+1, zeros(Float64, record_count), :Mean)
    mean_actual = round(mean(df1[3]), digits=1) 
    #a = zeros(record_count)
    for row in 1:record_count
        df[row, column_count+1]= mean_actual
    end
end