#column_to_predict = "DJIA_Original"
column_to_predict = "AAPL_Original"
# column_to_predict = "VIX_Original"
# column_to_predict = "NIO_Original"
# column_to_predict = "NVDA_Original"

## uncomment for the first run
# import Pkg
# Pkg.add("PyCall")
# Pkg.add("Conda")
# ENV["PYTHON"] = "/opt/anaconda3/envs/turi/bin/python"
# /opt/anaconda3/envs/turi/lib/python3.6/site-packages/
# Pkg.build("PyCall")

include("../Julia/functions.jl") 

using PyCall
tc = pyimport("turicreate")

data_path="../DATA/processed/uber_training.csv"
data = tc.SFrame(data_path)
println()

# Make a train-test split
train_data, test_data = data.random_split(0.8)
println()

println( size(train_data) )
println( size(test_data)  )



model = tc.regression.create( 
    train_data, 
    target = column_to_predict, 
    features = [

    #"VIX_Quantized"
    "VIX_Avg030"
    ,"VIX_Avg060"
    ,"VIX_Avg090"
    ,"VIX_Avg120"
    ,"VIX_Avg180"
    ,"VIX_Avg365"
        
    ,"US_ISM_MFC_PMI_Quantized"
    ,"US_ISM_MFC_PMI_Avg030"
    ,"US_ISM_MFC_PMI_Avg060"
    ,"US_ISM_MFC_PMI_Avg090"
    ,"US_ISM_MFC_PMI_Avg180"
    ,"US_ISM_MFC_PMI_Avg365"
        

    ,"DJIA_Quantized"
    ,"DJIA_Avg005"
    ,"DJIA_Avg030"
    ,"DJIA_Avg060"
    ,"DJIA_Avg090"
    ,"DJIA_Avg120"
    ,"DJIA_Avg180"
       
    #,"AAPL_Quantized"
    ,"AAPL_Avg005"
    ,"AAPL_Avg030"
    ,"AAPL_Avg060"
    ,"AAPL_Avg090"
    ,"AAPL_Avg120"
    ,"AAPL_Avg180"

    ,"US_ISM_MFC_EMP_Quantized"
    ,"US_ISM_MFC_EMP_Avg030"
    ,"US_ISM_MFC_EMP_Avg060"
    ,"US_ISM_MFC_EMP_Avg090"
    ,"US_ISM_MFC_EMP_Avg120"
    ,"US_ISM_MFC_EMP_Avg180"
    ,"US_ISM_MFC_EMP_Avg365"
        
    ,"US_INIT_JOBLESS_Quantized"
    ,"US_INIT_JOBLESS_Avg005"
    ,"US_INIT_JOBLESS_Avg030"
    ,"US_INIT_JOBLESS_Avg060"
    ,"US_INIT_JOBLESS_Avg090"
    ,"US_INIT_JOBLESS_Avg120"
    ,"US_INIT_JOBLESS_Avg180"
        
    ,"US_GDP_Q_Quantized"
    ,"US_GDP_Q_Avg005"
    ,"US_GDP_Q_Avg030"
    ,"US_GDP_Q_Avg060"
    ,"US_GDP_Q_Avg090"
    ,"US_GDP_Q_Avg120"
    ,"US_GDP_Q_Avg180"
        

    ,"NIO_Quantized"
    ,"NIO_Avg005"
    ,"NIO_Avg030"
    ,"NIO_Avg060"
    ,"NIO_Avg090"
    ,"NIO_Avg120"
    ,"NIO_Avg180"
        

    ,"NVDA_Quantized"
    ,"NVDA_Avg005"
    ,"NVDA_Avg030"
    ,"NVDA_Avg060"
    ,"NVDA_Avg090"
    ,"NVDA_Avg120"
    ,"NVDA_Avg180"
        

    ,"US_HOUS_STRT_M_Quantized"
    ,"US_HOUS_STRT_M_Avg005"
    ,"US_HOUS_STRT_M_Avg030"
    ,"US_HOUS_STRT_M_Avg060"
    ,"US_HOUS_STRT_M_Avg090"
    ,"US_HOUS_STRT_M_Avg120"
    ,"US_HOUS_STRT_M_Avg180"
    
        ], 
    validation_set="auto", 
    verbose=true
)

#TODO: write this in a loop to select the best model
# Evaluate the model and save the results into a dictionary
results = model.evaluate( test_data ) #test_data[0:2531]
results

rmse = results["rmse"]
rmse = round(rmse, digits=2)

max_error = results["max_error"]
max_error = round(max_error, digits=2)

println( "max_error: ", max_error, ", rmse: ", rmse )
# max_error: 1069.27, rmse: 184.6
# max_error: 65.35, rmse: 32.6            predict: ^DJIA added: US_INIT_JOBLESS
# max_error: 1875.39, rmse: 443.59        predict: ^DJIA commented out: "DJIA_Quantized"
# max_error: 1339.76, rmse: 373.94        predict: ^DJIA commented out: "DJIA_Quantized"
# max_error: 916.19, rmse: 231.24       predict: ^DJIA with "DJIA_Avg005"

# Export to Core ML
model.export_coreml("../DATA/models/^DJI.mlmodel")

data_path="../DATA/processed/uber_prediction.csv"
data_predictions = tc.SFrame(data_path)
println()

## Save predictions to an SArray
predictions = model.predict(data_predictions)
get(predictions, 1)

record_count = size(data_predictions)[1]
row = get(data_predictions, record_count-1)

feature_number = row.count
day = row["Rata_Die"]
date = row["Date"] # "2020-10-20"
original = row["DJIA_Original"]

println( "record_count data ", record_count )
println( "record_count predictions ", size(predictions)[1] )

println( "feature_number ", feature_number )
println( "Rata Die ", day )
println( "date ", date )
println( "original ", original )

using Dates
today_rata = Dates.datetime2rata( today() )

## Determine dataset size

initio = 1                                              # latin: start
finem  = size(predictions)[1] -1                        # latin: end
gradus = convert(Int64, round( finem/20, digits=0)  )   # latin: step

println("preditions set size: ", finem, ", step ", gradus)

using Dates

## Declare variables
x_axis_dates      = Vector{Date}() # results in Array{Date,1}
y_axis_original   = Vector{Float64}()
y_axis_predicted  = Vector{Float64}()

println(column_to_predict, " ", finem, " ", typeof(x_axis_dates))

today_id  = 50 # not set yet

## step thru each prediction
for id in initio:finem
    row = get(data_predictions, id) # get a dictionary of data from the SFrame
    
    date_string = row["Date"] # e.g. "2020-10-20"
    date = Date(date_string) # 2020-09-07 Date
    if date == today()
        today_id = id
    end 
    #date = Dates.format(date, "u.d,yy" )
    #println("date ", date, " ", typeof(date))
    push!(x_axis_dates, date)
    
    predicted = get(predictions, id) # Float64
    predicted = round(predicted, digits=0)
    #println("predicted ", predicted, " ", typeof(predicted))
    append!(y_axis_predicted, predicted)
    
    
    original = row[ column_to_predict ]
    original = round(original, digits=0) # Float64
    #println("original ", original, " ", typeof(original)) 
    append!(y_axis_original, original)
end

## Format Dates for plotting
include("../Julia/function_format_dates.jl")
x_axis_dates = format_dates(x_axis_dates, "u.d,yy")
println()

t = today()# Date
t = format_dates([t], "u.d,yy") # Array{String,1}
t = t[1] # String
println("t ", t, " ", typeof(t))

using Plots

#dates = format_dates( df[rows,2] , "m/d/yy")

gr()
plot(    x_axis_dates,
        [  y_axis_original y_axis_predicted 
        ], # y-axis
    label    = 
        [ column_to_predict "preditions"  "" ],
    legend   =:bottomright, 
              # :right, :left, :top, :bottom, :inside, :best, :legend, :topright, :topleft, :bottomleft, :bottomright
    xlabel   = "time",
    ylabel   = "value",
    size     = (980, 400), # width, height
    layout = (1, 1), # number of graphs: vertically, horizontally
    )
## Add veritical today line
plot!([today_id], seriestype="vline", label=[ "today "*t "" ],)

savefig("../../predictions.png")
savefig("../../predictions_" * column_to_predict * ".png")

## print prediction comparisons
#println(today_id)

for id in finem-35:finem
    if id < today_id + 3
        row = get(data_predictions, id) # get a dictionary of data from the SFrame
        date_string = row["Date"] # e.g. "2020-10-20"
        
        a = y_axis_predicted[id]
        b = y_axis_original[id]
        d = round(b-a, digits=3)
        date = convert(String, Dates.format( Date(date_string), "e, u. dd, yyyy" ) )
        if id < today_id
            println( date, "\t predicted ", a , "\t, but actual value was \t", b , "\t difference is ",  d  ) # di
        else
            println( date, "\t predicted ", a  ) # di
        end # if
    end #if 
end


