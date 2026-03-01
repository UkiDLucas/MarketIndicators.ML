## uncomment for the first run
# import Pkg
# Pkg.add("PyCall")
# Pkg.add("Conda")
# ENV["PYTHON"] = "/opt/anaconda3/envs/turi/bin/python"
# /opt/anaconda3/envs/turi/lib/python3.6/site-packages/
# Pkg.build("PyCall")


#symbol_to_predict = "AAPL" ## Comment OUT when running as include Julia file

println("symbol_to_predict ", symbol_to_predict )

## Read feature names (columns) from the text file 
features_to_analyze = readlines("../DATA/features_to_analyze.txt") # returns Array{String,1}

include("../Julia/functions.jl") 
include("../Julia/format_dates.jl")

data_path="../DATA/processed/uber_training.csv"
#column_to_predict = symbol_to_predict * "_Original"
column_to_predict = symbol_to_predict * "_Avg005"

## Remove column to predict from features
typeof(features_to_analyze)

filter!(e->e≠ column_to_predict , features_to_analyze)
println(features_to_analyze)

## Fetch Data (SFrame) from Uber CSV

using PyCall
tc = pyimport("turicreate")
data = tc.SFrame(data_path)
println()

# Make a train-test split
train_data, test_data = data.random_split(0.9)

println( "train_data size = ", size(train_data) )
println( "test_data size = ", size(test_data)  )

## Train the Model
model = tc.regression.create( 
    train_data, 
    target = column_to_predict, 
    features = features_to_analyze, 
    validation_set="auto", 
    verbose=true
)

## Evaluate the model and save the results into a dictionary
## TODO: write this in a loop to select the best model
results = model.evaluate( test_data ) #test_data[0:2531]

rmse = results["rmse"]
rmse = round(rmse, digits=2)

max_error = results["max_error"]
max_error = round(max_error, digits=2)

println( "MODEL EVALUTATION max_error: ", max_error, ", rmse: ", rmse )

## Export to Core ML
model_path = "../DATA/models/" * symbol_to_predict * ".mlmodel"
println("Saved model to ", model_path)
model.export_coreml(model_path)

## Read UBER predictions CSV
data_path="../DATA/processed/uber_prediction.csv"
data_to_predict = tc.SFrame(data_path)

## Save predictions to an SArray
prediction_results = model.predict(data_to_predict) # get(predictions, 1)

println()

## Explore the SFrame

#record_count = size(data_to_predict)[1]
#row = get(data_to_predict, record_count-1)

#feature_number = row.count
#day = row["Rata_Die"]
#date = row["Date"] # "2020-10-20"
#original = row["DJIA_Original"]

#println( "record_count data ", record_count )
#println( "record_count prediction_results ", size(prediction_results)[1] )

#println( "feature_number ", feature_number )
#println( "Rata Die ", day )
#println( "date ", date )
#println( "original ", original )

using Dates
today_rata = Dates.datetime2rata( today() )

## Determine dataset size

initio = 1                                              # latin: start
finem  = size(prediction_results)[1] -1                 # latin: end
#gradus = convert(Int64, round( finem/20, digits=0)  )  # latin: step

#println("PREDICTION dataset size: ", finem, ", step ", gradus)


## Declare variables
x_axis_dates      = Vector{Date}() # results in Array{Date,1}
y_axis_original   = Vector{Float64}()
y_axis_predicted  = Vector{Float64}()

#println(symbol_to_predict, " ", finem, " ", typeof(x_axis_dates))

today_id  = 0 # not set yet

## step thru each prediction
for id in initio:finem
    row = get(data_to_predict, id) # get a dictionary of data from the SFrame
    
    date_string = row["Date"] # e.g. "2020-10-20"
    date = Date(date_string) # 2020-09-07 Date
    if date == today()
        println("found today's date ", date)
        today_id = id
    end 
    
    if date <= today() + Dates.Day(7) # graph few days of predictions
    
        #date = Dates.format(date, "u.d,yy" )
        #println("date ", date, " ", typeof(date))
        push!(x_axis_dates, date)

        predicted = get(prediction_results, id) # Float64
        predicted = round(predicted, digits=0)
        #println("predicted ", predicted, " ", typeof(predicted))
        append!(y_axis_predicted, predicted)


        original = row[ column_to_predict ]
        original = round(original, digits=0) # Float64
        #println("original ", original, " ", typeof(original)) 
        append!(y_axis_original, original)
    end #if
end

## Format Dates for plotting
x_axis_dates = format_dates(x_axis_dates, "u.d,yy") # Trim any spaces, spaces may cause "segmentation error"



t = today()# Date
t = format_dates([t], "u. d, yyyy") # Array{String,1}
t = t[1] # String
#println("t = ", t, " - ", typeof(t))
println()

## Draw Plot

using Plots 

gr()
plot(            x_axis_dates,
               [ y_axis_original   y_axis_predicted ], # y-axis
    label    = [ symbol_to_predict "predicted"  "" ],
    legend   =:topleft, 
              # :right, :left, :top, :bottom, :inside, :best, :legend, :topright, :topleft, :bottomleft, :bottomright
    xlabel   = "date",
    ylabel   = "value",
    size     = (980, 400), # width, height
    layout = (1, 1), # number of graphs: vertically, horizontally
    )

## Add veritical today line

plot!([today_id], seriestype="vline", label=[ "Today "*t "" ],)

## Save plot graph

path_to_save = "../images/predictions_" * symbol_to_predict * ".png"
println("Saving plot image to ", path_to_save)
savefig(path_to_save)

## print prediction comparisons

println(symbol_to_predict, " ", today())

data_original = y_axis_original
data_predicted = y_axis_predicted
data_all_predicitons = data_to_predict

include("../Julia/print_predictions.jl")
print_predictions(data_to_predict,prediction_results, symbol_to_predict)


