import asyncio
import websockets
import requests
import time
import serial
import datetime
import sqlite3

previous_data = ""  # global variable
current_data = ""  # global variable


previous_alarm = ""
current_alarm = ""

CheckSum_Error_Boolean = False
Uncaught_Error_Boolean = False



def CheckSum(input_data):
    my_array = []
    my_hex_array = []
    first_character_list = []
    second_character_list = []


    for i in range(len(input_data)):
        my_array.append(input_data[i])
        my_hex_array.append(bytes(input_data[i],"utf-8").hex())
    
    #print(my_array)
    #print(my_hex_array)

    for string in my_hex_array:
        first_digit = string[0]
        first_character_list.append(int(first_digit))

    for string in my_hex_array:
        first_digit = string[1]
        second_character_list.append(int(first_digit))

    #print("First Row (Hex)" + str(first_character_list))
    #print("Second Row (Hex)" + str(second_character_list))

    first_binary_list = [bin(num)[2:].zfill(4) for num in first_character_list]
    #print("First Row (Binary): " + str(first_binary_list))

    second_binary_list = [bin(num)[2:].zfill(4) for num in second_character_list]
    #print("Second Row (Binary): "  + str(second_binary_list))

    ###############################3

    result = int(first_binary_list[0], 2)  # convert first element to int
    for i in range(1, len(first_binary_list)):
        num = int(first_binary_list[i], 2)  # convert next element to int
        result ^= num  # perform XOR operation

    binary_result = bin(result)[2:].zfill(len(first_binary_list[0]))  # convert result back to binary
    #print(binary_result)  # output: 0010 1110 1110 0011
    decimal_value = int(binary_result, 2)
    #print(decimal_value)  # Output: 42

    ###############################33
    result_2 = int(second_binary_list[0], 2)  # convert first element to int
    for i in range(1, len(second_binary_list)):
        num_2 = int(second_binary_list[i], 2)  # convert next element to int
        result_2 ^= num_2  # perform XOR operation

    binary_result_2 = bin(result_2)[2:].zfill(len(second_binary_list[0]))  # convert result back to binary
    #print(binary_result_2)  # output: 0010 1110 1110 0011

    decimal_value_2 = int(binary_result_2, 2)
    #print(decimal_value_2)  # Output: 42

    #print("Check Sum: " + str(decimal_value) + str(decimal_value_2))
    if(decimal_value == 10):
        decimal_value = "A"
    elif(decimal_value == 11):
        decimal_value = "B"
    elif(decimal_value == 12):
        decimal_value = "C"
    elif(decimal_value == 13):
        decimal_value = "D"
    elif(decimal_value == 14):
        decimal_value = "D"
    elif(decimal_value == 15):
        decimal_value = "F"
    else:
        decimal_value = decimal_value

    if(decimal_value_2 == 10):
        decimal_value_2 = "A"
    elif(decimal_value_2 == 11):
        decimal_value_2 = "B"
    elif(decimal_value_2 == 12):
        decimal_value_2 = "C"
    elif(decimal_value_2== 13):
        decimal_value_2 = "D"
    elif(decimal_value_2 == 14):
        decimal_value_2 = "D"
    elif(decimal_value_2 == 15):
        decimal_value_2 = "F"
    else:
        decimal_value_2 = decimal_value_2

    #print("Final C-Command: " + input_data + str(decimal_value) + str(decimal_value_2) + "*")
    return str(decimal_value) + str(decimal_value_2)

    ###################################



connected_clients = set()

async def server(websocket, path):
    # Register client
    connected_clients.add(websocket)

    try:
        while True:
            #for num in range(1, 11):
            #    data = str(num)
            #    print("Sending:", data)

                # Send data to the client
            #    await websocket.send(data)

                # Wait for a short interval between sending each number
            #    await asyncio.sleep(1)
            try:
                ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600,   bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_TWO, timeout=1)
                current_time = datetime.datetime.now()

                data = str("PLC- Raspberry PI USB Connection Successfully, Time: " + str(current_time) + "\n")
                #print("Current time:", current_time)
                PLC_data = ser.readline()

                ####
    
                if PLC_data:
                    
                    global previous_data
                    global current_data
                    current_data = PLC_data

                    data_removed = PLC_data[5:]
                    s_str = PLC_data.decode('utf-8') # @10RR0000000000000041*
                    with open('response.txt', 'w') as file:
                        file.write(s_str)
                    print("PLC response : " + s_str)
                    data_removed_byte = data_removed.decode('utf-8')
                    #print("After removed: " + data_removed_byte) 
                    # Response CheckSum 
                    #print("______________________________________")
                    return_checksum = data_removed_byte[len(data_removed_byte)-4:len(data_removed_byte)-2]
 
                    print("Response Check Sum: " + return_checksum)
                    #Calculation CheckSum
                    #print("line 152")
                    calculation_checksum = s_str[:len(s_str)-4]
                    print("The input for checksum : " + str(calculation_checksum))
                    CheckSum_Result = CheckSum(calculation_checksum)
                    print("CheckSum : " + CheckSum_Result)
                    ########################################
                    #Compare the received checksum and calculated checksum
                    global CheckSum_Error_Boolean

                    if(return_checksum == CheckSum_Result):
                        print("PLC -> Raspberry Pi. No CheckSum Error. Can proceed")

                        CheckSum_Error_Boolean = False

                    else:
                        print("PLC -> Raspberry Pi. There is checksum error")
                        CheckSum_Error_Boolean = True


                    #####################################Check Data to prevent spam
                    response_code = PLC_data[5:7].decode('utf-8')
                    print("___________________________________________")
                    print("Response Code : " + response_code)
                    mode = PLC_data[3:5].decode('utf-8')
                    print("Data mode : " + mode)
                    global Uncaught_Error_Boolean

                    if response_code != "00":
                        Uncaught_Error_Boolean = True
                    else:
                        Uncaught_Error_Boolean = False
                    #############################
                    ####Three Coditons
                    # 1. Previous PLC response not same as Current 
                    # 2. CheckSum no error
                    # 3. Uncaught error is not caughted
                    if(previous_data != current_data and CheckSum_Error_Boolean != True and Uncaught_Error_Boolean != True):
                        previous_data = current_data
                        current_time = datetime.datetime.now().time()

                        update_text = "Updated " + str(current_time) 
                        bot_token = ''
                        chat_id = ''


                        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
                        params = {
                            'chat_id': chat_id,
                            'text': update_text
                        }

                        response = requests.post(url, params=params)
                        print(response.json())

                        #first_line = "@00RR0100000140*"
                        #print("Sending C-command: " + first_line)
                        #address_called = first_line[5:9]
                        #number_start_address = int(address_called)
                        #print("Address is called start from :" + str(number_start_address))
                        #print(CheckSum("@10RR00040008"))
                        #print("Byte Data Replied from PLC: " + data)

                        
                 
                        ########################################
                       
                        if response_code == "00":
                            print("Response: Normal Completion")
            
                            if(mode == "RR"):
                                print("CIO AREA READ")

                                    ############################## Do the address operation
                                Address_Operation = calculation_checksum[7:]
                                print(Address_Operation)
                                print("Total Length address returned : " + str(len(Address_Operation)))
                                print("Total Bits " + str(len(Address_Operation) * 4))
                                number_channel = len(Address_Operation) / 4
                                print("1 Channel = 4. That's reason why N address / 4 = N channel: " + str(number_channel))
                                #data += str(number_channel)

                                ##############################
                                binary_list = []
                                for hex_char in Address_Operation:
                                    binary_string = bin(int(hex_char, 16))[2:].zfill(4)
                                    binary_list.append(binary_string)

                                #print(binary_list[0])
                                # Assuming binary_list is a two-dimensional array

                                count = 0
                                # Connect to the SQLite database
                                conn = sqlite3.connect('../Frontend_DB/data.db')

                                # Create a cursor object to execute SQL queries
                                cursor = conn.cursor()

                                # Execute a SELECT query
                                cursor.execute('SELECT * FROM PLC')

                                # Fetch all rows from the result set
                                rows = cursor.fetchall()
                                result_array = []

                                # Process the rows
                                for row in rows:
                                    result_array.append(row)

                                #print(result_array[0][1])
                                # Convert tuples to string arrays
                                #result_string_arrays = [list(map(str, row)) for row in result_array]

                                # Print the result string arrays
                                #for row in result_string_arrays:
                                #    print(row)

                                # Print the result_array
                                #print(result_string_arrays[0][1])
                                # Print the result array
                                #(1, 'Lithium', 'Nitrogen ', 'Hydrogen Gas', 'Neon', 'Magnesium', 'Sodium', 'Aluminium', 'Potassium', '', 'Uranium', '', '', '', '', 'Titanium', 'Xenon')
                                #for row in result_array:
                                #    print(row)



                                #print(result_array)
                                # Close the cursor and the database connection
                                cursor.close()
                                conn.close()
                                
                                # Third Party Alert
                                message_text = ''

                                #Main Core Idea 
                                for i in range(len(binary_list) - 1, -1, -1):
                                    for j in range(len(binary_list[i]) - 1, -1, -1):
                                        print("When i is " + str(i) + " " + " When j is " + str(j)+ "   This is the element " + str(count)+ " value"+ binary_list[i][j])
                                        if(binary_list[i][j] == "1"):
                                            print("trigger alarm " + str(count))
                                            # Read SQLite DB to identify alarm message
                                            print(result_array[0][count+1])
                                            current_time = datetime.datetime.now().time()

                                            message_text += str(current_time) +  "  : "  + result_array[0][count+1] + " \n"


                                            ###API Third Party




                                            ###Socket Message
                                            data += str(result_array[0][count+1]) + " "

                                            
                                        count += 1
                                
                                global current_alarm, previous_alarm
                                current_alarm = message_text
                                
                                if(message_text != '' or current_alarm != previous_alarm):
   

                                    bot_token = ''
                                    chat_id = ''


                                    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
                                    params = {
                                        'chat_id': chat_id,
                                        'text': message_text
                                    }

                                    response = requests.post(url, params=params)
                                    print(response.json())

                                    data += "third Party response (important it will affect the third party alert): "  + str(response.json())
                                    previous_alarm != current_alarm


                                current_data = str(binary_list)
                                data += str(binary_list)
                                # One group = One channel = 15 bytes
                                #grouped_list = [binary_list[i:i+4] for i in range(0, len(binary_list), 4)]

                                #print(grouped_list)
                                #grouped_list_len = len(grouped_list)
                                #print("Group list element : " + str(len(grouped_list)))

                                #result_dict = {}
                                #key = number_start_address

                                #for lst in grouped_list:
                                #    result_dict[key] = lst
                                #    key += 1

                                #print(result_dict)
                                #result_dict[5][2] = "0100"
                                #result_dict[5][1] = "1100"
                                #print(result_dict[4][0])
                                #print(result_dict[4][0][0])


                                # Supposingly there is one way to detect PLC pulse 010101010101010
                                #
                                # However the scenario is the PLC could be locked by the client or the scenario where we dont likely to
                                # modify their PLC code therefore prompt from raspberry pi should be more better
                                # This is the way to detect one state

                                #if(result_dict[4][0][0] == "0"):
                                #    print("ALERT TRIGGERING!!!!!!!!!!!!!!!!!!!!!!!!!")
                                #    with open('error.txt', 'w') as file:
                                #        file.write(str(1))

                        
                            else:
                                print("Uncaught Error")
                                global Uncaught_Error_Boolean
                                Uncaught_Error_Boolean = True

                        else:
                            data += "No realtime data getting from PLC \n"

                    





                        ######
                        print("Sending:" + data)

                        ###




                                    
                        await websocket.send(data)
                        await asyncio.sleep(3)

                    else:
                        await asyncio.sleep(3)

                   
                

                

            except Exception as  e:
                data = str(e)
                print("Sending:", data)
                await websocket.send(data)
                await asyncio.sleep(3)

    except websockets.exceptions.ConnectionClosedOK:
        print("Client connection closed gracefully")
    except websockets.exceptions.ConnectionClosedError:
        print("Client connection closed with an error")
    finally:
        # Keep the client socket registered
        pass




# Start the WebSocket server
start_server = websockets.serve(server, "localhost", "8005")



# Run the server indefinitely
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
