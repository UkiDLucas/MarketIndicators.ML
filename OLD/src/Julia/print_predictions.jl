function print_predictions(data_to_predict, prediction_results, symbol_to_predict::String)

    open( "../DATA/predictions.csv", "a") do file_handle # a for append
        local finem  = size(data_original)[1] -0  # ignoring last element, it is usually =0
        for id in 1:finem # iterate thru the whole set
            dict = get(data_to_predict, id) # get a dictionary of data from the predicted SFrame
            prediction_date = dict["Date"] # e.g. "2020-10-20"

            if Date(prediction_date) > today() - Dates.Day(7) # Start showing X days ago
                original = dict[ column_to_predict ]
                original = round(original, digits=0) # Float64
                predicted = get(prediction_results, id) # Float64
                predicted = round(predicted, digits=0)
                difference = round(predicted-original, digits=3)
                date = convert(String, Dates.format( Date(prediction_date), "e, yyyy-mm-dd" ) )
                if Date(prediction_date) <= today() # Past dates
                    println( date, "\t predicted ", predicted , 
                    "\t, but actual value was \t", original , 
                    "\t difference is ",  difference  ) 
                
                else # future dates
                    println( date, "\t predicted ", predicted  ) # 
                    txt_to_save =  
                        convert(String, Dates.format( today(), "yyyy-mm-dd" ) ) *","* 
                        convert(String, symbol_to_predict) *","* 
                        prediction_date *","* 
                        string(predicted) * "\n"
                    write(file_handle, txt_to_save )
                end # if
            end #if 
        end # for
    end # open file
end # function