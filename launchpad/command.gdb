set confirm off

# Connect to GDB proxy
target remote localhost:2000


#break log_measure
#commands
#printf "Temperature = %d", tempAverage
#continue
#end

#disable 1



break delay_millis



# Run program as debugging session starts
# continue
