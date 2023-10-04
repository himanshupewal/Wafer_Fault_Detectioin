## use of exception --- we have two type of exception run time and compile time exceptoin.

#we are handeling compile time exception while giving code to cumputer




from logger import logging

import os,sys

def error_message_details(error,error_details:sys):
    _,_,exc_tb = error_details.exc_info()   ## exc_info  give message in exception class
    file_name = exc_tb.tb_frame.f_code.co_filename  ## collect message,line,name
    error_message = "Error occured python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error)
    )

    return error_message




class CustomException(Exception):

    def __init__(self,error_message,error_details:sys):

        """
        :param error_message: error message in string format
        """

        super().__init__(error_message)  ## calling parent class cunstructor.

        self.error_messsage = error_message_details(
            error_message,error_details = error_details
                            )

def __str__(self):   ## to print  error message from customexception class
    return self.error_message