# https://github.com/UkiDLucas/MarketIndicators.jl/blob/master/src/notebooks/normalize%20the%20data.ipynb
# https://www.tensorflow.org/lite/performance/quantization_spec?hl=fi
# https://en.wikipedia.org/wiki/Standard_score
# https://www.wikihow.com/Calculate-Standard-Deviation
# http://www.differencebetween.net/science/difference-between-average-and-mean/

# Fit dataset in range [-128, 127]
function quantize_column!(df::DataFrame, column_number::Int64)
    original = df[:, column_number] # Array{Float64,1}
 
    min = minimum(original)
    max = maximum(original)
    
    println("original max-min = ", max-min )
    println("original standard_deviation = ", std(original) )
    println("original population_mean = ", mean(original) )

    #bias = (0 - min)/(max-min)
    records_count = length(original)
    
    for i in 1:records_count
        value = (original[i] - min)/( max-min )   # normalization formula to range 0.0 to 1.0
        #value = value + bias
        value = value * 255                    # 0.0 to 255
        value = value - 128                    # -128 to 127
        value = round(value, digits=0)         # 0.00 
        df[i, column_number] = value
    end
    # println("Normalization was performend using formula y=(((x-min)/(max-min))*255)-128 ") 
end


