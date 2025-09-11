def toggle_reset(conn, rts, toggle): 
    if (toggle == "none"): 
        print("--- toggle none") 
    if (toggle == "rts"):   
        print("--- toggle reset line (RTS)") 
        conn.rts = not conn.rts 
        sleep(0.02) 
        conn.rts = not conn.rts     
    if (toggle == "dtr"):   
        print("--- toggle reset line (DTR)") 
        conn.dtr = not conn.dtr 
        sleep(0.02) 
        conn.dtr = not conn.dtr

serial_instance.open() 
toggle_reset(serial_instance, options["rts"], options["toggle"])

#https://github.com/pyserial/pyserial/issues/756