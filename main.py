##########
##########
##########

import aerial.aerial as aero
import server.server as serve


def main():
    
    # run data gathering function of test system and lidar captures
    aero.gather()
    # CSV file created with data

    # vehicle metrics, data analytics, path finding, data connection
    serve.main()
    # this sends commands to vehicle

main()
    

